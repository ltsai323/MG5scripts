#!/usr/bin/env python3
import matplotlib.pyplot as plt
from dataclasses import dataclass

import csv
NULLVAL=1e-100 # small enough, you will find a weird log scale plot

class pPtBinnedContent:
    def __init__(self, pPTbin:str, inVAL:str):
        self.pPtBin = int(pPTbin)
        self.value  = float(inVAL)
def LoadCSVFile_noNULL(inFILEname:str, var:str, pETAbin:int, jETAbin:int) -> list:
    with open(inFILEname, 'r') as ifile:
        csv_content = csv.DictReader(ifile)
        return [ pPtBinnedContent(c['pPtBin'],c[var]) for c in csv_content if c['pEtaBin']==str(pETAbin) and c['jEtaBin']==str(jETAbin) ]
def LoadCSVFile(inFILEname:str, var:str, pETAbin:int, jETAbin:int) -> list:
    return LoadCSVFile_noNULL(inFILEname,var,pETAbin,jETAbin)

def get_xy_scatter_point__implement_very_small_value(pPTbinnedCONTENTlist:list):
    from py_pt_ranges_definition import PhoPtBinning
    pt_axis = PhoPtBinning('UL2016PreVFP')

    # if there is skipped pt bin in CSV file, this algorithm will returned a NULLVAL

    x_vals = pt_axis # use all value
    y_vals = [ NULLVAL ] * len(pt_axis)
    for content in pPTbinnedCONTENTlist:
        y_vals[content.pPtBin] = content.value
    return ( x_vals, y_vals )
def get_xy_scatter_point__ignore_null_recording(pPTbinnedCONTENTlist:list):
    from py_pt_ranges_definition import PhoPtBinning
    pt_axis = PhoPtBinning('UL2016PreVFP')

    # if there is skipped pt bin in CSV file, this algorithm draws plot without bug
    x_vals = [pt_axis[content.pPtBin] for content in pPTbinnedCONTENTlist]
    y_vals = [content.value for content in pPTbinnedCONTENTlist]
    return ( x_vals, y_vals )
def GetXYscatterPOINT(pPTbinnedCONTENTlist:list):
    return get_xy_scatter_point__ignore_null_recording(pPTbinnedCONTENTlist)

@dataclass
class XYscatterPoints:
    x:[float]
    y:[float]
    y_err:[float]
    desc:str

    def __repr__(self):
        return f'XYscatterPoints: {self.desc}'


MARKER_STYLE = [ 'o', '^', 's', 'D' ]
COLORS = [ 'blue', 'green', 'orange', 'purple' ]

def draw_EP(xySCATTERwithDESC:[XYscatterPoints],
        inTITLE:str = 'blah',
        yTITLE:str = '$d^{3}\sigma$ / d$\eta_{\gamma}$ d$\eta_{C}$ d$p_{T}^{\gamma}$',
        yRANGE:tuple = (), logY:bool = True,
        ):
    plt.clf()
    fig = plt.figure(facecolor='none', edgecolor='none', figsize=(6, 4), dpi=80)

    for idx, xy_scatter_with_desc in enumerate(xySCATTERwithDESC):
        plt.errorbar(
                xy_scatter_with_desc.x,
                xy_scatter_with_desc.y,
           yerr=xy_scatter_with_desc.y_err,
          label=xy_scatter_with_desc.desc,
                markersize=3,fmt=MARKER_STYLE[idx], color=COLORS[idx])

    plt.title(inTITLE)
    plt.xlabel('$p_{T}^{\gamma}$ (GeV)')
    plt.ylabel(yTITLE)
    if yRANGE and len(yRANGE)>0.: plt.ylim(yRANGE[0],yRANGE[1])
    else: print('[AutoYrange - INFO:makeplot_tool] Input yRANGE not found. Auto value.')
    if logY: plt.yscale('log')
    plt.legend()
