#!/usr/bin/env python3

import ROOT
from step3_tools import CSVWriter, phosel, jetsel




def INFO(*args):
    print('[step3_extractXSinCSVsep.py-INFO] ', *args)



class BinnedHists:
    pho,l,c,b = (None,None,None,None)
    mcPredicted_l, mcPredicted_c, mcPredicted_b = (None,None,None)
    mcPredicted_leading_l, mcPredicted_leading_c, mcPredicted_leading_b = (None,None,None)
def BinnedMainFunction(pETAbin, jETAbin, xAXIS, inTREE) ->BinnedHists:
    newhist = lambda name, label : ROOT.TH1F(name, f'cross section {label}', len(xAXIS)-1, xAXIS)
    h_xs_pho = newhist(f'pho_XS_{pETAbin}{jETAbin}', 'overall #gamma+jet')
    h_xs_l = newhist(f'l_jet_XS_{pETAbin}{jETAbin}', 'light jet')
    h_xs_c = newhist(f'c_jet_XS_{pETAbin}{jETAbin}', 'c jet')
    h_xs_b = newhist(f'b_jet_XS_{pETAbin}{jETAbin}', 'b jet')

    h_pred_l = newhist(f'mc_predicted_l_{pETAbin}{jETAbin}', 'predicted L')
    h_pred_c = newhist(f'mc_predicted_c_{pETAbin}{jETAbin}', 'predicted C')
    h_pred_b = newhist(f'mc_predicted_b_{pETAbin}{jETAbin}', 'predicted B')
    h_pred_leading_l = newhist(f'mc_predicted_leading_l_{pETAbin}{jETAbin}', 'predicted leading L')
    h_pred_leading_c = newhist(f'mc_predicted_leading_c_{pETAbin}{jETAbin}', 'predicted leading C')
    h_pred_leading_b = newhist(f'mc_predicted_leading_b_{pETAbin}{jETAbin}', 'predicted leading B')

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


    # 2 is index of MC generated parton
    # denominator of match eff
    fillcontent(h_pred_l  .GetName(), 'fabs(Particle_PID[2])!=5 && fabs(Particle_PID[2])!=4'.strip())
    fillcontent(h_pred_c  .GetName(), '                            fabs(Particle_PID[2])==4'.strip())
    fillcontent(h_pred_b  .GetName(), 'fabs(Particle_PID[2])==5                            '.strip())

    # numerator of match eff
    fillcontent(h_pred_leading_l.GetName(), 'fabs(Particle_PID[2])!=5 && fabs(Particle_PID[2])!=4 && jetIdx==2'.strip())
    fillcontent(h_pred_leading_c.GetName(), '                            fabs(Particle_PID[2])==4 && jetIdx==2'.strip())
    fillcontent(h_pred_leading_b.GetName(), 'fabs(Particle_PID[2])==5                             && jetIdx==2'.strip())



    out = BinnedHists()
    out.pho, out.l, out.c, out.b = (h_xs_pho,h_xs_l,h_xs_c,h_xs_b)
    out.mcPredicted_l, out.mcPredicted_c, out.mcPredicted_b = ( h_pred_l, h_pred_c, h_pred_b)
    out.mcPredicted_leading_l, out.mcPredicted_leading_c, out.mcPredicted_leading_b = (h_pred_leading_l, h_pred_leading_c, h_pred_leading_b)
    return out

def RecordSingle_(csvCONTENT:CSVWriter, inBIN:tuple, recHIST:ROOT.TH1F):
    pETAbin = inBIN[0]
    jETAbin = inBIN[1]
    rec = CSVWriter.yield_and_error(recHIST)
    for pptbin, val in enumerate(rec):
        csvCONTENT.append_data( {
            'pEtaBin': pETAbin,
            'jEtaBin': jETAbin,
            'pPtBin': pptbin,
            'value': val[0],
            'error': val[1],
        } )
def RecordSingle(csvCONTENT:CSVWriter, inBIN:tuple, recHIST:ROOT.TH1F):
    pETAbin = inBIN[0]
    jETAbin = inBIN[1]
    rec = CSVWriter.yield_and_error(recHIST)
    for pptbin, val in enumerate(rec):
        csvCONTENT.append_data( {
            'pEtaBin': pETAbin,
            'jEtaBin': jETAbin,
            'pPtBin': pptbin,
            'crossSection': val[0],
            'crossSectionError': val[1],
        } )

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
    #INFO(f'output CSV file is {outputname}')
    csv_out = CSVWriter(outputname)
    Record(csv_out,0,0,hhh00)
    Record(csv_out,0,1,hhh10)
    Record(csv_out,1,0,hhh01)
    Record(csv_out,1,1,hhh11)
    csv_out.Write()

    outputtemplate = '.'.join( infile.GetName().split('.')[:-1] ) + '_{tag}.csv'

    outHISTs = [
            ( (0,0), hhh00 ),
            ( (0,1), hhh01 ),
            ( (1,0), hhh10 ),
            ( (1,1), hhh11 )
            ]

    def WriteIT(outNAME:str, varNAME:str, outHISTs:list):
        csv_out = CSVWriter(outNAME)
        for inbin, hists in outHISTs:
            RecordSingle( csv_out, inbin, getattr(hists,varNAME) )
        csv_out.Write()
    WriteIT( outputtemplate.format(tag='XS_l'), 'l', outHISTs )
    WriteIT( outputtemplate.format(tag='XS_c'), 'c', outHISTs )
    WriteIT( outputtemplate.format(tag='XS_b'), 'b', outHISTs )

    outMERGE_HISTs = [
            ( (0,0), hhh00 ),
            ( (0,0), hhh01 ),
            ( (1,0), hhh10 ),
            ( (1,0), hhh11 )
            ]
    def WriteMerged(outNAME:str, varNAME:str, outHISTs:list):
        csv_out = CSVWriter(outNAME)
        for inbin, hists in outHISTs:
            RecordSingle_( csv_out, inbin, getattr(hists,varNAME) )
        csv_out.Write()

    WriteMerged( outputtemplate.format(tag='mcPredicted_l'), 'mcPredicted_l', outMERGE_HISTs )
    WriteMerged( outputtemplate.format(tag='mcPredicted_c'), 'mcPredicted_c', outMERGE_HISTs )
    WriteMerged( outputtemplate.format(tag='mcPredicted_b'), 'mcPredicted_b', outMERGE_HISTs )

    WriteMerged( outputtemplate.format(tag='mcPredicted_leading_l'), 'mcPredicted_leading_l', outMERGE_HISTs )
    WriteMerged( outputtemplate.format(tag='mcPredicted_leading_c'), 'mcPredicted_leading_c', outMERGE_HISTs )
    WriteMerged( outputtemplate.format(tag='mcPredicted_leading_b'), 'mcPredicted_leading_b', outMERGE_HISTs )
