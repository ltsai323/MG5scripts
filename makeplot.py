#!/usr/bin/env python3
import matplotlib.pyplot as plt

import csv
class pPtBinnedContent:
    def __init__(self, pPTbin:str, inVAL:str):
        self.pPtBin = int(pPTbin)
        self.value  = float(inVAL)
def LoadCSVFile(inFILEname:str, var:str, pETAbin:int, jETAbin:int) -> list:
    with open(inFILEname, 'r') as ifile:
        csv_content = csv.DictReader(ifile)
        #return [ (int(c['pPtBin']),float(c[var])) for c in csv_content if c['pEtaBin']==str(pETAbin) and c['jEtaBin']==str(jETAbin) ]
        return [ pPtBinnedContent(c['pPtBin'],c[var]) for c in csv_content if c['pEtaBin']==str(pETAbin) and c['jEtaBin']==str(jETAbin) ]

def GetXYscatterPOINT(pPTbinnedCONTENTlist:list):
    from py_pt_ranges_definition import PhoPtBinning
    pt_axis = PhoPtBinning('UL2016PreVFP')
    x_vals = [pt_axis[content.pPtBin] for content in pPTbinnedCONTENTlist]
    y_vals = [content.value for content in pPTbinnedCONTENTlist]
    return ( x_vals, y_vals )

if __name__ == "__main__":
    import sys
    title = sys.argv[1]
    ifile = sys.argv[2]

    #loadVar = 'crossSection'
    loadVar = 'crossSectionC'

    draw00 = True
    if draw00:
        content = LoadCSVFile(ifile, loadVar,0,0)
        xarr,yarr = GetXYscatterPOINT(content)
        plt.scatter(xarr,yarr, label='barrel $\gamma$, barrel C', marker='o')
    draw01 = True
    if draw00:
        content = LoadCSVFile(ifile, loadVar,0,1)
        xarr,yarr = GetXYscatterPOINT(content)
        plt.scatter(xarr,yarr, label='barrel $\gamma$, endcap C', marker='s')
    draw10 = True
    if draw00:
        content = LoadCSVFile(ifile, loadVar,1,0)
        xarr,yarr = GetXYscatterPOINT(content)
        plt.scatter(xarr,yarr, label='endcap $\gamma$, barrel C', marker='D')
    draw11 = True
    if draw00:
        content = LoadCSVFile(ifile, loadVar,1,1)
        xarr,yarr = GetXYscatterPOINT(content)
        plt.scatter(xarr,yarr, label='endcap $\gamma$, endcap C', marker='^')

    plt.title(f'{title} simulation')
    plt.xlabel('$p_{T}^{\gamma}$ (GeV)')
    plt.ylabel('$d^{3}\sigma$ / d$\eta_{\gamma}$ d$\eta_{C}$ d$p_{T}^{\gamma}$')
    plt.ylim(1e-7,1e3)
    plt.yscale('log')
    plt.legend()
    plt.savefig(f'h_{title}.pdf')


