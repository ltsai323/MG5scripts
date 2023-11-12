#!/usr/bin/env python3
import matplotlib.pyplot as plt

import csv
NULLVAL=1e-100 # small enough, you will find a weird log scale plot

class pPtBinnedContent:
    def __init__(self, pPTbin:str, inVAL:str):
        self.pPtBin = int(pPTbin)
        self.value  = float(inVAL)
def LoadCSVFile(inFILEname:str, var:str, pETAbin:int, jETAbin:int) -> list:
    with open(inFILEname, 'r') as ifile:
        csv_content = csv.DictReader(ifile)
        #return [ (int(c['pPtBin']),float(c[var])) for c in csv_content if c['pEtaBin']==str(pETAbin) and c['jEtaBin']==str(jETAbin) ]
        return [ pPtBinnedContent(c['pPtBin'],c[var]) for c in csv_content if c['pEtaBin']==str(pETAbin) and c['jEtaBin']==str(jETAbin) ]

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


MARKER_STYLE = [ 'o', '^', 's', 'D' ]
COLORS = [ 'blue', 'green', 'orange', 'purple' ]
def draw_EP(inFILEwithDESCs:list, pETAbin:int, jETAbin:int,
        inTITLE:str = 'blah',
        yTITLE:str = '$d^{3}\sigma$ / d$\eta_{\gamma}$ d$\eta_{C}$ d$p_{T}^{\gamma}$',
        yRANGE:tuple = (), logY:bool = True,
        ):
    '''
    # input argument in format
    inputs = [
            ('infile1.csv', 'desc used in legend1'),
            ('infile2.csv', 'desc used in legend2'),
            ('infile3.csv', 'desc used in legend3'),
            ]
    '''
    plt.cla()
    fig = plt.figure(facecolor='none', edgecolor='none', figsize=(6, 4), dpi=80)

    for idx, (inFILE,desc) in enumerate(inFILEwithDESCs):
        value_pair = LoadCSVFile(inFILE, 'value', pETAbin,jETAbin)
        error_pair = LoadCSVFile(inFILE, 'error', pETAbin,jETAbin)
        pt_arr, values = GetXYscatterPOINT(value_pair)
        _     , errors = GetXYscatterPOINT(error_pair)
        plt.errorbar(pt_arr, values, yerr=errors, label=desc, markersize=3,fmt=MARKER_STYLE[idx], color=COLORS[idx])

    plt.title(inTITLE)
    plt.xlabel('$p_{T}^{\gamma}$ (GeV)')
    plt.ylabel(yTITLE)
    if len(yRANGE)>0.: plt.ylim(yRANGE[0],yRANGE[1])
    if logY: plt.yscale('log')
    plt.legend()

def draw_EP_ratio(inFILEwithDESCs:list, pETAbin:int, jETAbin:int,
        inTITLE:str = 'blah',
        yTITLE:str = '$d^{3}\sigma$ / d$\eta_{\gamma}$ d$\eta_{C}$ d$p_{T}^{\gamma}$',
        yRANGE:tuple = (), logY:bool = True,
        ratioTITLE:str = 'ratio',
        ):
    '''
    # input argument in format
    # this code will take the first entry as the denominator
    inputs = [
            ('infile1.csv', 'desc used in legend1'),
            ('infile2.csv', 'desc used in legend2'),
            ('infile3.csv', 'desc used in legend3'),
            ]
    '''
    plt.cla()
    #fig = plt.figure(facecolor='none', edgecolor='none', figsize=(6, 4), dpi=80)
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]},
            facecolor='none', edgecolor='none', figsize=(6,4),dpi=80,
            )
    ax2.axhline(y=1, color='black', linestyle='--', label='Ratio=1')



    ratio_value = None
    ratio_error = None
    for idx, (inFILE,desc) in enumerate(inFILEwithDESCs):
        value_pair = LoadCSVFile(inFILE, 'value', pETAbin,jETAbin)
        error_pair = LoadCSVFile(inFILE, 'error', pETAbin,jETAbin)
        pt_arr, values = get_xy_scatter_point__implement_very_small_value(value_pair)
        _     , errors = get_xy_scatter_point__implement_very_small_value(error_pair)
        ax1.errorbar(pt_arr, values, yerr=errors, label=desc, markersize=3,fmt=MARKER_STYLE[idx], color=COLORS[idx])

        # set first entry as ratio  denominator
        # take ratio relative to first entry
        if ratio_value == None:
            ratio_value = values
            ratio_error = errors
        else:
            ratio_v = [NULLVAL] * len(values)
            ratio_e = [NULLVAL] * len(values)
            for kdx, (v,e,_v,_e) in enumerate(zip(values, errors,ratio_value,ratio_error)):
                if  v == NULLVAL: continue
                if _v == NULLVAL: continue
                ratio_v[kdx] = v/_v
                variance_x = e / _v
                variance_y = -1. * v / (_v*_v) * _e
                ratio_e[kdx] = ( variance_x**2+variance_y**2 )**0.5

            ax2.errorbar(pt_arr, ratio_v, ratio_e, markersize=3, fmt=MARKER_STYLE[idx], color=COLORS[idx])

    ax1.set_title(inTITLE)
    ax1.set_ylabel(yTITLE)
    if logY: ax1.set_yscale('log')
    if len(yRANGE)>0.: ax1.set_ylim(yRANGE[0],yRANGE[1])
    ax1.legend()

    ax2.set_xlabel('$p_{T}^{\gamma}$ (GeV)')
    ax2.set_ylabel(ratioTITLE)
    ax2.set_ylim(0.5,1.5)
