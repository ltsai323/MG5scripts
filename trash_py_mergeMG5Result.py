#!/usr/bin/env python3

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


def mergecuts(*cutstrs):
    def singlecut(cut): return '('+cut+')'
    # remove empty item if detected
    cuts = (singlecut(c) for c in cutstrs if c)
    return ' & '.join(cuts)


def get_binned_differencial_xs(
        bin_edge, phoETAbin: int, jetETAbin: int,
        mergedhist):

    isBARRELpho = 1 if phoETAbin == 0 else False
    isBARRELjet = 1 if jetETAbin == 0 else False

    width_PhoEta = 1.4442*2. if isBARRELpho else (2.5-1.566) * 2.
    width_JetEta = 1.5000*2. if isBARRELjet else (2.4-1.500) * 2.

    ptbin_widths = bin_edge[1:] - bin_edge[:-1]
    xs_contents = [bin_content /
                   (width_PhoPt*width_PhoEta*width_JetEta)
                   for width_PhoPt, bin_content in
                   zip(ptbin_widths, mergedhist)]

    plt.clf()
    plt.bar(bin_edge[:-1], xs_contents, width=ptbin_widths)
    plt.yscale('log')
    return xs_contents

def PtRange(inputENTRIES:list):
    # find pho pt range
    # -1 means nothing
    # once the ptgmin is not found in json file. These code gets wrond. asdf
    ptgmins = {entry.ptgmin: idx for idx, entry in enumerate(inputENTRIES)}
    sorted_pt = sorted(ptgmins.keys())

    phoptrange = {}
    for ptminIdx in range(len(sorted_pt)):
        ptmin = sorted_pt[ptminIdx]
        ptmax = sorted_pt[ptminIdx+1] if ptminIdx + 1 != len(inputENTRIES) else None

        fileIdx = ptgmins[ptmin]
        phoptrange[fileIdx] = (ptmin, ptmax)

    return [
        ('branches["Particle.PT"][:,3]>%.1f' % ptrange[0],
         'branches["Particle.PT"][:,3]<%.1f' % ptrange[1] if ptrange[1] else None)
        for key, ptrange in phoptrange.items() ]
def Cut_Quark(quarkNAME:str=''):
    quarkID = 'np.abs(branches["Particle.PID"][:,2])'
    if quarkNAME == 'b': return f'{quarkID} == 5'
    if quarkNAME == 'c': return f'{quarkID} == 4'
    if quarkNAME == 'l': return f'({quarkID} < 4) | ({quarkID} == 21)'
    INFO('Checking none b/c/l quark.')
    return f'({quarkID}>5)&({quarkID}!=21)'

def binned_val_in_selection( commonOBJ:list, additionalCUT:str, xAXIS:list):
    assignedXaxis = True if len(commonOBJ) > 3 else False
    efflumilist     = commonOBJ[0]
    branchlist      = commonOBJ[1]
    phoPtRangeCut   = commonOBJ[2]
    bin_edge        = commonOBJ[3] if assignedXaxis else 100 # 100 bins in auto x-range.
    xAxis = xAXIS # [variableName, idx]

    additional_cut = additionalCUT

    hist1D_y = []
    for efflumi, branches, pCuts in zip(efflumilist, branchlist, phoPtRangeCut):
        evt_weight= event_weight_calc(branches,efflumi)

        # photon cross section section
        cut_fiducial_region = mergecuts(pCuts[0], pCuts[1])
        cut_total = mergecuts(cut_fiducial_region, additionalCUT)
        sel_data = selected_data(branches,cut_total)

        pho_idx = np.where(sel_data.array('Particle.PID') == 22)
        print(pho_idx)
        exit(0)

        res_pho_pt = data_with_weight()
        res_pho_pt.AddWeightedEvent(sel_data,evt_weight)
        #data_point, data_weight = res_pho_pt.GetDataAndWeight('Particle.PID', 2)
        data_point, data_weight = res_pho_pt.GetDataAndWeight(*xAxis)

        hist, out_bin_edge, _ = pyhist_factory( data_point,data_weight,bin_edge)
        hist1D_y.append(hist)

    out_x = out_bin_edge
    out_y = HistMerger(*hist1D_y)
    return (out_x,out_y)
def BinnedVal_PhotonPt_InCut( commonOBJ:list, additionalCUT:str):
    efflumilist     = commonOBJ[0]
    branchlist      = commonOBJ[1]
    phoPtRangeCut   = commonOBJ[2]
    bin_edge        = commonOBJ[3]

    additional_cut = additionalCUT

    hist1D_y = []
    for efflumi, branches, pCuts in zip(efflumilist, branchlist, phoPtRangeCut):
        evt_weight= event_weight_calc(branches,efflumi)

        # photon cross section section
        cut_fiducial_region = mergecuts(pCuts[0], pCuts[1])
        cut_total = mergecuts(cut_fiducial_region, additionalCUT)
        sel_data = selected_data(branches,cut_total)

        res_pho_pt = data_with_weight()
        res_pho_pt.AddWeightedEvent(sel_data,evt_weight)
        data_point, data_weight = res_pho_pt.GetDataAndWeight('Particle.PT', 3)

        hist, _, _ = pyhist_factory( data_point,data_weight,bin_edge)
        hist1D_y.append(hist)
    mergehist = HistMerger(*hist1D_y)
    out_x = bin_edge
    out_y = mergehist
    #mergehist = HistMerger(*(bincontents for bincontents in hist1D_y ))
    return (out_x,out_y)

if __name__ == "__main__":
    inputInfos = JsonIO(EntryDef)
    inputInfos.LoadFile(sys.argv[1])

    ifiles = (uproot.open(entry.ifile) for entry in inputInfos.entry)
    branchlist = [ifile['LHEF'].arrays() for ifile in ifiles]

    # -1 means no to use efflumi weight
    # using xs reweight
    efflumilist = [entry.efflumi if hasattr(
        entry, 'efflumi') else -1 for entry in inputInfos.entry]
    '''
    # find pho pt range
    # -1 means nothing
    # once the ptgmin is not found in json file. These code gets wrond. asdf
    ptgmins = {entry.ptgmin: idx for idx, entry in enumerate(inputInfos.entry)}
    sorted_pt = sorted(ptgmins.keys())

    phoptrange = [None] * len(branchlist)
    for ptminIdx in range(len(sorted_pt)):
        ptmin = sorted_pt[ptminIdx]
        ptmax = sorted_pt[ptminIdx+1] if ptminIdx + \
            1 != len(branchlist) else None

        fileIdx = ptgmins[ptmin]
        phoptrange[fileIdx] = (ptmin, ptmax)
    phoPtRangeCut = [
        ('branches["Particle.PT"][:,3]>%.1f' % ptmin,
         'branches["Particle.PT"][:,3]<%.1f' % ptmax if ptmax else None)
        for ptmin, ptmax in phoptrange
    ]
    '''
    phoPtRangeCut = PtRange(inputInfos.entry)
    # once the ptgmin is not found in json file. These code gets wrong. asdf

    # hist binning
    from py_pt_ranges_definition import PhoPtBinning
    dataEra = 'UL2016'
    bin_edge = np.array(PhoPtBinning(dataEra))

    # used cut collection
    cut_endcapPho1 = 'np.abs(branches["Particle.Eta"][:,3])>1.566'
    cut_endcapPho2 = 'np.abs(branches["Particle.Eta"][:,3])<2.5'
    cut_endcapPho = mergecuts(cut_endcapPho1, cut_endcapPho2)
    cut_barrelPho = 'np.abs(branches["Particle.Eta"][:,3])<1.4442'
    cut_pho = [cut_barrelPho, cut_endcapPho]

    cut_endcapJet1 = 'np.abs(branches["Particle.Eta"][:,2])>1.5'
    cut_endcapJet2 = 'np.abs(branches["Particle.Eta"][:,2])<2.4'
    cut_endcapJet = mergecuts(cut_endcapJet1, cut_endcapJet2)
    cut_barrelJet = 'np.abs(branches["Particle.Eta"][:,2])<1.5'
    cut_jet = [cut_barrelJet, cut_endcapJet]

    commonobj = (efflumilist, branchlist, phoPtRangeCut, bin_edge)

    output_CSV_content = []
    phoEtaBin=0
    jetEtaBin=0
    if True:
        if True:
    # for phoEtaBin in range(2):
    #     for jetEtaBin in range(2):
    #        x, yield_pho = BinnedVal_PhotonPt_InCut(commonobj,
    #                mergecuts(cut_pho[phoEtaBin], cut_jet[jetEtaBin])
    #                )
    #        x, yield_l = BinnedVal_PhotonPt_InCut(commonobj,
    #                mergecuts(cut_pho[phoEtaBin], cut_jet[jetEtaBin], Cut_Quark('l'))
    #                )
    #        x, yield_c = BinnedVal_PhotonPt_InCut(commonobj,
    #                mergecuts(cut_pho[phoEtaBin], cut_jet[jetEtaBin], Cut_Quark('c'))
    #                )
    #        x, yield_b = BinnedVal_PhotonPt_InCut(commonobj,
    #                mergecuts(cut_pho[phoEtaBin], cut_jet[jetEtaBin], Cut_Quark('b'))
    #                )
            x, yield_weird = binned_val_in_selection( (efflumilist,branchlist,phoPtRangeCut),
                    mergecuts(cut_pho[phoEtaBin], cut_jet[jetEtaBin], Cut_Quark()),
                    ('Particle.PID',2)
                    )
            for idx, (vALL, vl, vc, vb) in enumerate(zip(yield_pho, yield_l, yield_c, yield_b)):
                netval = vALL-vl-vc-vb
                print(f'pt bin {idx}, {vALL}, {vl}, {vc}, {vb}. Net value {netval} ({netval/vALL})')
            plt.savefig('out_checkplot.png')


            exit(0)
            diff_xs = get_binned_differencial_xs( bin_edge, phoEtaBin, jetEtaBin, mergehist )
            diff_xsL= get_binned_differencial_xs( bin_edge, phoEtaBin, jetEtaBin, mergehistL)
            diff_xsC= get_binned_differencial_xs( bin_edge, phoEtaBin, jetEtaBin, mergehistC)
            diff_xsB= get_binned_differencial_xs( bin_edge, phoEtaBin, jetEtaBin, mergehistB)
            plt.savefig(f'out_checkplot_{phoEtaBin}_{jetEtaBin}.png')

            for phoPtBin, xs in enumerate( zip(diff_xs,diff_xsL,diff_xsC,diff_xsB) ):
                print(xs)
                output_CSV_content.append( {
                    'pEtaBin': phoEtaBin,
                    'jEtaBin': jetEtaBin,
                    'pPtBin': phoPtBin,
                    'crossSection': xs[0],
                    'crossSectionError': 0.,
                    'crossSectionL': xs[1],
                    'crossSectionLError': 0.,
                    'crossSectionC': xs[2],
                    'crossSectionCError': 0.,
                    'crossSectionB': xs[3],
                    'crossSectionBError': 0.,
                } )

    import csv
    with open('out_mergeMG5Result.csv', 'w') as newfile:
        csvwritter = csv.DictWriter(newfile, fieldnames=output_CSV_content[0].keys())
        csvwritter.writeheader()
        csvwritter.writerows(output_CSV_content)
