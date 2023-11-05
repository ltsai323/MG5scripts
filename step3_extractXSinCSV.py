#!/usr/bin/env python3

import ROOT
from step3_tools import CSVWriter, phosel, jetsel


showinfo = True


def INFO(*args):
    if showinfo:
        print('[step3_extractYieldinCSV.noWeightForStatistics.py-INFO] ', *args)



class BinnedHists:
    pho,l,c,b = (None,None,None,None)
def BinnedMainFunction(pETAbin, jETAbin, xAXIS, inTREE) ->BinnedHists:
    newhist = lambda name, label : ROOT.TH1F(name, f'cross section {label}', len(xAXIS)-1, xAXIS)
    h_xs_pho = newhist(f'pho_XS_{pETAbin}{jETAbin}', 'overall #gamma+jet')
    h_xs_l = newhist(f'l_jet_XS_{pETAbin}{jETAbin}', 'light jet')
    h_xs_c = newhist(f'c_jet_XS_{pETAbin}{jETAbin}', 'c jet')
    h_xs_b = newhist(f'b_jet_XS_{pETAbin}{jETAbin}', 'b jet')

    from step3_tools import phosel, jetsel
    basic_cut = f'{phosel(pETAbin)} && {jetsel(jETAbin)}'


    def fillcontent(histNAME, additionalSELECTION) -> None:
        drawopt1 = f'Particle_PT[phoIdx] >> {histNAME}'
        drawopt2 = f'mcweight * ( {additionalSELECTION} && {basic_cut} )' # original version
        #drawopt2 = f' ( {additionalSELECTION} && {basic_cut} )' # no mc weight version
        print(f'\n\n-----\n[BinnedMainFunction-LOG] intree.Draw("{drawopt1}","{drawopt2}")')
        inTREE.Draw( drawopt1, drawopt2 )

    fillcontent(h_xs_pho.GetName(), '1')
    fillcontent(h_xs_l  .GetName(), 'fabs(Particle_PID[jetIdx])!=5 && fabs(Particle_PID[jetIdx])!=4'.strip())
    fillcontent(h_xs_c  .GetName(), '                                 fabs(Particle_PID[jetIdx])==4'.strip())
    fillcontent(h_xs_b  .GetName(), 'fabs(Particle_PID[jetIdx])==5                                 '.strip())

    ## no bin width needed in this code
    def crosssection_to_differential_crosssection(pETAbin,jETAbin, hiST) -> None:
        etabin_width = 1.
        if pETAbin == 0: etabin_width *= 1.4442*2.
        if pETAbin == 1: etabin_width *= (1.566-1.4442)*2.


        for ptbin in range(1,hiST.GetNbinsX()+1):
            evt_weight = 1./( hiST.GetBinWidth(ptbin) * etabin_width )
            hiST.SetBinContent( ptbin, hiST.GetBinContent(ptbin) * evt_weight )
            hiST.SetBinError  ( ptbin, hiST.GetBinError  (ptbin) * evt_weight )
    crosssection_to_differential_crosssection(pETAbin,jETAbin, h_xs_pho)
    crosssection_to_differential_crosssection(pETAbin,jETAbin, h_xs_l  )
    crosssection_to_differential_crosssection(pETAbin,jETAbin, h_xs_c  )
    crosssection_to_differential_crosssection(pETAbin,jETAbin, h_xs_b  )

    out = BinnedHists()
    out.pho, out.l, out.c, out.b = (h_xs_pho,h_xs_l,h_xs_c,h_xs_b)

    return out

def Record(csvCONTENT:CSVWriter, pETAbin:int,jETAbin:int, binnedHISTs:BinnedHists):
    rec_pho = CSVWriter.yield_and_error(binnedHISTs.pho)
    rec_l   = CSVWriter.yield_and_error(binnedHISTs.l)
    rec_c   = CSVWriter.yield_and_error(binnedHISTs.c)
    rec_b   = CSVWriter.yield_and_error(binnedHISTs.b)
    for pptbin, (vPho,vL,vC,vB) in enumerate( zip(rec_pho,rec_l,rec_c,rec_b) ):
        csvCONTENT.append_data( {
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

if __name__ == "__main__":
    import sys
    infile = ROOT.TFile.Open(sys.argv[1])
    #infile = ROOT.TFile.Open('gjet_NLO_loop_sm_no_b_mass_NNPDF3p1nnlo.root')
    INFO(f'input file : {infile.GetName()}')
    intree = infile.Get('LHEF')


    from py_pt_ranges_definition import PhoPtBinning
    from array import array
    dataEra = 'UL2016PreVFP'
    bin_phopt = array('d',PhoPtBinning(dataEra))

    hhh00 = BinnedMainFunction(0,0, bin_phopt, intree)
    hhh01 = BinnedMainFunction(0,1, bin_phopt, intree)
    hhh10 = BinnedMainFunction(1,0, bin_phopt, intree)
    hhh11 = BinnedMainFunction(1,1, bin_phopt, intree)

    import csv
    outputname = '.'.join( infile.GetName().split('.')[:-1] ) + '.csv'
    INFO(f'output CSV file is {outputname}')
    csv_out = CSVWriter(outputname)
    Record(csv_out,0,0,hhh00)
    Record(csv_out,0,1,hhh10)
    Record(csv_out,1,0,hhh01)
    Record(csv_out,1,1,hhh11)
    csv_out.Write()
