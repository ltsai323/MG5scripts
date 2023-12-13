#!/usr/bin/env python3
import matplotlib.pyplot as plt
import csv

import makeplot_tools as myTool
from uncertainties import ufloat
from dataclasses import dataclass

PRINT_BUG = False
def BUG(*args):
    if PRINT_BUG: print('[BUG] ', *args)

## generator. Used in for loop. The first input becomes denominator. The others are numerator.
from typing import Generator
def TakeRatio(xySCATTERwithDESC:[myTool.XYscatterPoints]) -> Generator[myTool.XYscatterPoints,None,None]:
    value_error_dict = lambda my_obj: { x:ufloat(v,e) for x,v,e in zip(my_obj.x,my_obj.y,my_obj.y_err) }
    denominator = value_error_dict(xySCATTERwithDESC[0])

    for idx, xy_scatter_with_desc in enumerate(xySCATTERwithDESC[1:]):
        BUG(xy_scatter_with_desc)
        numerator = value_error_dict(xy_scatter_with_desc)
        BUG('numerator ', numerator)
        BUG('denominator ', denominator)

        xList = [                          x  for x in numerator.keys() if x in denominator and abs(denominator[x]) > 1e-12 ]
        BUG(xList)
        #ratio = [ numerator[x]/denominator[x] for x in xList ]
        ratio = []
        for x in xList:
            BUG(' value a/b = %.3e/%.3e'%(numerator[x].nominal_value,denominator[x].nominal_value))
            ratio.append(numerator[x]/denominator[x])
        yield myTool.XYscatterPoints(
                x=xList, y=[r.nominal_value for r in ratio],y_err=[r.std_dev for r in ratio],desc=xy_scatter_with_desc.desc)

def draw_EP_ratio(xySCATTERwithDESC:[myTool.XYscatterPoints],
        inTITLE:str = 'blah',
        yTITLE:str = '$d^{3}\sigma$ / d$\eta_{\gamma}$ d$\eta_{C}$ d$p_{T}^{\gamma}$',
        yRANGE:tuple = (), logY:bool = True,
        ratioTITLE:str = 'ratio',
        ratioYrange:tuple = (0.5,1.5),
        ):
    plt.clf()
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]},
            facecolor='none', edgecolor='none', figsize=(6,4),dpi=80,
            )


    ## fill upper pad
    for idx, xy_scatter_with_desc in enumerate(xySCATTERwithDESC):
        ax1.errorbar(
                xy_scatter_with_desc.x,
                xy_scatter_with_desc.y,
           yerr=xy_scatter_with_desc.y_err,
          label=xy_scatter_with_desc.desc,
                markersize=3,fmt=myTool.MARKER_STYLE[idx], color=myTool.COLORS[idx])
    ax1.set_title(inTITLE)
    ax1.set_ylabel(yTITLE)

    if yRANGE and len(yRANGE)>0.:
        ax1.set_ylim(yRANGE[0],yRANGE[1])


        if logY:
            if yRANGE[0]<0.:
                print(f'[LogScale - WARNING] Failed log transform to  y axis range {yRANGE}. Use normal scale.')
            else:
                ax1.set_yscale('log')
    else:
        if logY: ax1.set_yscale('log')
    ax1.legend()

    ax2.axhline(y=1, color='black', linestyle='--', label='Ratio=1')
    ## fill lower pad
    for _idx, xy_scatter in enumerate(TakeRatio(xySCATTERwithDESC)):
        idx = _idx+1
        x = xy_scatter.x
        y = xy_scatter.y
        yErr = xy_scatter.y_err
        desc = xy_scatter.desc
        ax2.errorbar(x,y,yErr, markersize=3, fmt=myTool.MARKER_STYLE[idx], color=myTool.COLORS[idx])


    ax2.set_xlabel('$p_{T}^{\gamma}$ (GeV)')
    ax2.set_ylabel(ratioTITLE)
    ax2.set_ylim(*ratioYrange)
def TESTER_draw_EP_ratio():
    f1 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv',
            'NNPDF3p1 NLO in 5NFS intrinsic charm')
    f2 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_c.csv',
            'NNPDF3p1 NLO in 4NFS intrinsic charm')
    f3 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_c.csv',
            'NNPDF3p1 NLO in 5NFS perturbative charm')
    f4 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_c.csv',
            'NNPDF3p1 NLO in 4NFS perturbative charm')

    infile_withdesc = ( f1,f2,f3,f4 )
    pETAbin,jETAbin = (1,0)

    xyScatterWithDesc = [None] * len(infile_withdesc)
    for idx, (inFILE,desc) in enumerate(infile_withdesc):
        value_pair = myTool.LoadCSVFile(inFILE, 'value', pETAbin,jETAbin)
        error_pair = myTool.LoadCSVFile(inFILE, 'error', pETAbin,jETAbin)

        ## fill upper pad
        pt_arr, values = myTool.GetXYscatterPOINT(value_pair)
        _     , errors = myTool.GetXYscatterPOINT(error_pair)

        xyScatterWithDesc[idx] = myTool.XYscatterPoints(x=pt_arr,y=values,y_err=errors,desc=desc)


    inTITLE = 'test'
    outFIGname = 'h.png'
    draw_EP_ratio(xyScatterWithDesc,
            yTITLE='$\gamma$+c yield',
            #yRANGE = (1e-5, 1e4),
            inTITLE=inTITLE)
    plt.savefig(outFIGname)
    print(outFIGname + ' generated')


if __name__ == "__main__":
    TESTER_draw_EP_ratio()
