#!/usr/bin/env python3

import ROOT

from python.HistProducer import pyhist_factory, selected_data,event_weight_calc, data_with_weight
from python.DAToutput import DATOut_Init, DATOut_Write, DATMgr, DATFormat_fitValue
from python.JsonIOMgr import JsonIO
# from python.UseEffLumi import Entry_UseEffLumi as EntryDef
# from python.UseXSweight import Entry_UseXSweight as EntryDef
from python.UseXSweight import Entry_UseXSweight_WithPtCut as EntryDef
from python.HistMergeMethod import HistMerger_SumUp as HistMerger

import sys
import uproot4 as uproot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

showinfo = True


def INFO(*args):
    if showinfo:
        print('[mergeMG5Result-INFO] ', *args)



class BinnedHists:
    pho,l,c,b = (None,None,None,None)
def BinnedMainFunction(pETAbin, jETAbin, xAXIS, inTREE):
    newhist = lambda name, label : ROOT.TH1F(name, f'cross section {label}', len(xAXIS)-1, xAXIS)
    h_xs_pho = newhist(f'pho_XS_{pETAbin}{jETAbin}', 'overall #gamma+jet')
    h_xs_l = newhist(f'l_jet_XS_{pETAbin}{jETAbin}', 'light jet')
    h_xs_c = newhist(f'c_jet_XS_{pETAbin}{jETAbin}', 'c jet')
    h_xs_b = newhist(f'b_jet_XS_{pETAbin}{jETAbin}', 'b jet')


    def phosel(pETAbin):
        if pETAbin == 0:
            return 'fabs(Particle_Eta[phoIdx])<1.4442'
        if pETAbin == 1:
            cut_endcapPho1 = 'fabs(Particle_Eta[phoIdx])>1.566'
            cut_endcapPho2 = 'fabs(Particle_Eta[phoIdx])<2.5'
            return f'{cut_endcapPho1} && {cut_endcapPho2}'

    def jetsel(jETAbin):
        if jETAbin == 0:
            return 'fabs(Particle_Eta[jetIdx])<1.5'
        if jETAbin == 1:
            cut_endcapJet1 = 'fabs(Particle_Eta[jetIdx])>1.5'
            cut_endcapJet2 = 'fabs(Particle_Eta[jetIdx])<2.4'
            return f'{cut_endcapJet1} && {cut_endcapJet2}'

    basic_cut = f'{phosel(pETAbin)} && {jetsel(jETAbin)}'


    def fillcontent(histNAME, additionalSELECTION):
        drawopt1 = f'Particle_PT[phoIdx] >> {histNAME}'
        drawopt2 = f'mcweight * ( {additionalSELECTION} && {basic_cut} )' # original version asfd
        #drawopt2 = f' ( {additionalSELECTION} && {basic_cut} )' # test version
        print(f'\n\n-----\n[BinnedMainFunction-LOG] intree.Draw("{drawopt1}","{drawopt2}")')
        inTREE.Draw( drawopt1, drawopt2 )

    fillcontent(h_xs_pho.GetName(), '1')
    fillcontent(h_xs_l  .GetName(), 'fabs(Particle_PID[jetIdx])!=5 && fabs(Particle_PID[jetIdx])!=4')
    fillcontent(h_xs_c  .GetName(), '                                 fabs(Particle_PID[jetIdx])==4')
    fillcontent(h_xs_b  .GetName(), 'fabs(Particle_PID[jetIdx])==5                                 ')

    out = BinnedHists()
    out.pho, out.l, out.c, out.b = (h_xs_pho,h_xs_l,h_xs_c,h_xs_b)

    return out
class CSVWriter:
    def __init__(self, outNAME:str):
        self.ofile = outNAME
        self.content = []
    def Record(self, pETAbin:int,jETAbin:int, binnedHISTs:BinnedHists):
        rec_pho = CSVWriter.yield_and_error(binnedHISTs.pho)
        rec_l   = CSVWriter.yield_and_error(binnedHISTs.l)
        rec_c   = CSVWriter.yield_and_error(binnedHISTs.c)
        rec_b   = CSVWriter.yield_and_error(binnedHISTs.b)
        for pptbin, (vPho,vL,vC,vB) in enumerate( zip(rec_pho,rec_l,rec_c,rec_b) ):
            self.content.append( {
                'pEtaBin': pETAbin,
                'jEtaBin': jETAbin,
                'pPtBin': pptbin,
                'crossSection': vPho[0],
                'crossSectionError': vPho[1],
                'crossSectionL': vL[0],
                'crossSectionLError': vL[1],
                'crossSectionC': vC[0],
                'crossSectionCError': vC[1],
                'crossSectionB': vB[0],
                'crossSectionBError': vB[1],
            } )
    def Write(self):
        with open(self.ofile, 'w') as newfile:
            csvwritter = csv.DictWriter(newfile, fieldnames=self.content[0].keys())
            csvwritter.writeheader()
            csvwritter.writerows(self.content)


    @classmethod
    def yield_and_error(cls, theTH1:ROOT.TH1F):
        max_pt_bin = theTH1.GetNbinsX() # from 0 to max-1
        vals = [ theTH1.GetBinContent(ptbin+1) for ptbin in range(max_pt_bin) ]
        errs = [ theTH1.GetBinError  (ptbin+1) for ptbin in range(max_pt_bin) ]
        return [ (val,err) for val,err in zip(vals,errs) ]

if __name__ == "__main__":
    import sys
    infilename,pEtaBin,jEtaBin,pPtBin,varType = ROOT.TFile.Open(sys.argv[1:])
    #infilename = 'gjet_NLO_loop_sm_no_b_mass_NNPDF3p1nnlo.root'
    # varType : pho, l, c, b
    infile = ROOT.TFile.Open(infilename)
    INFO(f'input file : {infile.GetName()}')
    intree = infile.Get('LHEF')

    canv = ROOT.TCanvas('c1','',500,400)


    from py_pt_ranges_definition import PhoPtBinning
    from array import array
    dataEra = 'UL2016'
    bin_phopt = array('d',PhoPtBinning(dataEra))

    hhh00 = BinnedMainFunction(0,0, bin_phopt, intree)
    hhh01 = BinnedMainFunction(0,1, bin_phopt, intree)
    hhh10 = BinnedMainFunction(1,0, bin_phopt, intree)
    hhh11 = BinnedMainFunction(1,1, bin_phopt, intree)
    hhh00.pho.Draw('hist')
    canv.SetLogy()
    canv.SaveAs("hi.png")

    import csv
    outputname = '.'.join( infile.GetName().split('.')[:-1] ) + '.csv'
    INFO(f'output CSV file is {outputname}')
    csv_out = CSVWriter(outputname)
    csv_out.Record(0,0,hhh00)
    csv_out.Record(0,1,hhh10)
    csv_out.Record(1,0,hhh01)
    csv_out.Record(1,1,hhh11)
    csv_out.Write()
