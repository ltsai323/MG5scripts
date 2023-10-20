#!/usr/bin/env python3

from python.JsonIOMgr import JsonIO
# from python.UseEffLumi import Entry_UseEffLumi as EntryDef
# from python.UseXSweight import Entry_UseXSweight as EntryDef
from python.UseXSweight import Entry_UseXSweight_WithPtCut as EntryDef

import sys
import uproot4 as uproot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import ROOT

showinfo = True

def INFO(*args):
    if showinfo:
        print('[INFO] ', *args)

def NewSelectedROOTfile(iFILE:str, oFILE:str, cutCONTENT:str, evtWEIGHT:float):
    print(iFILE)
    iDataFrame = ROOT.ROOT.RDataFrame('LHEF', iFILE)
    
    INFO(f'\n\nOutput file {oFILE}')
    INFO(f'Selecting event \n ---> {cutCONTENT}')
    iDataFrame. \
        Filter(cutCONTENT). \
        Define('evt_weight', f'{evtWEIGHT:.5f}'). \
        Snapshot('LHEF', oFILE)
    


if __name__ == "__main__":
    inputInfos = JsonIO(EntryDef)
    inputInfos.LoadFile(sys.argv[1])

    # uproot4 version
    # ifiles = [uproot.open(entry.ifile) for entry in inputInfos.entry]
    # branchlist = [ifile['LHEF'].arrays() for ifile in ifiles]

    ifiles = [ ROOT.TFile.Open(entry.ifile) for entry in inputInfos.entry ]
    #branchlist = [ ifile.Get('LHEF') for ifile in ifiles ]

    pt_min_idx = { entry.ptgmin: idx for idx, entry in enumerate(inputInfos.entry) }
    sorted_pt_min_idx_idx = [ pt_min_idx[entry] for entry in sorted(pt_min_idx.keys()) ]

    for i_, idx in enumerate(sorted_pt_min_idx_idx):
        #branch = branchlist[idx]

        pt_min = inputInfos.entry[idx].ptgmin
        pt_max = 999999.
        if i_+1 != len(sorted_pt_min_idx_idx):
            next_idx = sorted_pt_min_idx_idx[i_+1]
            pt_max = inputInfos.entry[next_idx].ptgmin

        #overallweight = GetWeight(branch)
        
        sel_name = f'(Particle.PT[3]>{pt_min})&&(Particle.PT[3]<{pt_max})'
        NewSelectedROOTfile(inputInfos.entry[idx].ifile, f'Output_{i_}.root', sel_name, 1.0)
    #for ifile in ifiles: ifile.Close()
    # # pt range from low to high ## uproot4 version. But uproot4 failed to write anything
    # output_branches = []
    # for i_, idx in enumerate(sorted_pt_min_idx_idx):
    #     branch = branchlist[idx]

    #     pt_min = inputInfos.entry[idx].ptgmin
    #     pt_max = 999999.
    #     if i_+1 != len(sorted_pt_min_idx_idx):
    #         next_idx = sorted_pt_min_idx_idx[i_+1]
    #         pt_max = inputInfos.entry[next_idx].ptgmin

    #     #overallweight = GetWeight(branch)
    #     
    #     sel_name = f'(branch["Particle.PT"][:,3]>{pt_min})&(branch["Particle.PT"][:,3]<{pt_max})'
    #     sel = eval(sel_name)
    #     output_branches.append(branch[sel])
    #     INFO(f'Selecting with \n --> {sel_name}')
    #     print(f'entries without select {len(branch)}')
    #     print(f'entries with--- select {len(output_branches[-1])}')

    # # #merged_tree = uproot.concatenate(output_branches)
    # # merged_tree = output_branches[0]
    # # with uproot.writing.recreate('mergedMG5tree.root') as output_file:
    # #     output_file['LHEF'] = merged_tree

    # # testing but failed
    # #branchlist = [ifile['LHEF'].arrays(library='pd') for ifile in ifiles]
    #     #sel_name = f'(branch["Particle.PT"][:,3]>{pt_min})& (branch["Particle.PT"][:,3]<{pt_max})'
    #     #INFO(f'Selecting with \n --> f{sel_name}')
    
    # for ifile in ifiles: ifile.close()