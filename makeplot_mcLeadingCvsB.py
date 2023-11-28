#!/usr/bin/env python3
import matplotlib.pyplot as plt

import makeplot_tools as myTool
from makeplot_tools import XYscatterPoints
from makeplot_ratiotool import TakeRatio
from makeplot_tools import  draw_EP
from makeplot_ratiotool import draw_EP_ratio
from makeplot_drawingprocess import DrawingProcess,HackData
from makeplot_drawingprocess import yRangeFinder_LinearScale


def get_data_point_(inCSVfile:str, desc:str,pETAbin:int,jETAbin:int) -> XYscatterPoints:
    value_pair = myTool.LoadCSVFile(inCSVfile, 'value', pETAbin,jETAbin)
    error_pair = myTool.LoadCSVFile(inCSVfile, 'error', pETAbin,jETAbin)

    pt_arr, values = myTool.GetXYscatterPOINT(value_pair)
    _     , errors = myTool.GetXYscatterPOINT(error_pair)

    return XYscatterPoints(x=pt_arr,y=values,y_err=errors,desc=desc)
def get_data_point_barrel(inTUPLE:tuple) -> XYscatterPoints:
    ''' inTUPLE like
    f1 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv',
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_b.csv',
            'NNPDF3p1 NLO in 5NFS intrinsic charm')
    '''
    pETAbin,jETAbin = (0,0)

    c_data_point = get_data_point_(inTUPLE[0],inTUPLE[2],pETAbin,jETAbin)
    b_data_point = get_data_point_(inTUPLE[1],inTUPLE[2],pETAbin,jETAbin)
    inputdatapoint = [b_data_point,c_data_point]
    return list(TakeRatio(inputdatapoint))[0]
def get_data_point_endcap(inTUPLE:tuple) -> XYscatterPoints:
    ''' inTUPLE like
    f1 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv',
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_b.csv',
            'NNPDF3p1 NLO in 5NFS intrinsic charm')
    '''
    pETAbin,jETAbin = (1,0)

    c_data_point = get_data_point_(inTUPLE[0],inTUPLE[2],pETAbin,jETAbin)
    b_data_point = get_data_point_(inTUPLE[1],inTUPLE[2],pETAbin,jETAbin)
    inputdatapoint = [b_data_point,c_data_point]
    return list(TakeRatio(inputdatapoint))[0]


def draw_scatter_plot(
        yRANGE:list,
        xySCATTERpointS:[XYscatterPoints],
        inTITLE:str = 'truth $\gamma$+c / $\gamma$+b',
        outFIGname:str = 'h_testbarrelpho.png',
        ):

    print(f'[fig output - LOG] Generating {outFIGname}')
    draw = draw_EP if len(xySCATTERpointS)==1 else draw_EP_ratio
    draw( xySCATTERpointS,
            yTITLE = 'weighed $\gamma$+c yield',
            yRANGE = yRANGE,
            logY = False,
            inTITLE = inTITLE)
    plt.savefig(outFIGname)
    plt.close()


if __name__ == "__main__":
    f1 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_c.csv',
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_b.csv',
            '5NFS intrinsic charm')
    f2 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv',
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_leading_b.csv',
            '4NFS intrinsic charm')
    f3 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_c.csv',
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_b.csv',
            '5NFS perturbative charm')
    f4 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv',
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_leading_b.csv',
            '4NFS perturbative charm')


    def task(draw_obj):
        the_title = 'Truth ratio of $\gamma$+C / $\gamma$+b in NNPDF3.1 NLO @ leading jet selection'
        draw_obj.DrawSingle( f1,f2,f3,f4,
                inTITLE=the_title,
            outFIGtemplate='AllMCCompare.pdf')
        draw_obj.DrawSingle( f1,
                inTITLE=the_title,
            outFIGtemplate='NNPDF31_nlo_as_0118.pdf')
        draw_obj.DrawSingle( f2,
                inTITLE=the_title,
            outFIGtemplate='NNPDF31_nlo_as_0118_nf_4.pdf')
        draw_obj.DrawSingle( f3,
                inTITLE=the_title,
            outFIGtemplate='NNPDF31_nlo_pch_as_0118.pdf')
        draw_obj.DrawSingle( f4,
                inTITLE=the_title,
            outFIGtemplate='NNPDF31_nlo_pch_as_0118_nf_4.pdf')

        printDetailComparison = True
        if printDetailComparison:
            print('[INFO] Generate detailed plot')
            calculated_y_ranges = yRangeFinder_LinearScale( (get_data_point_endcap(f) for f in [f1,f2,f3,f4]) )
            draw_obj.SetDetailPlotArgument( *calculated_y_ranges )
            draw_obj.DrawDetail( f1,f2,f3,f4, inTITLE=the_title, outFIGtemplate='AllMCCompare.pdf')
            draw_obj.DrawDetail(f1, inTITLE=the_title, outFIGtemplate = 'NNPDF31_nlo_as_0118.pdf')
            draw_obj.DrawDetail(f2, inTITLE=the_title, outFIGtemplate = 'NNPDF31_nlo_as_0118_nf_4.pdf')
            draw_obj.DrawDetail(f3, inTITLE=the_title, outFIGtemplate = 'NNPDF31_nlo_pch_as_0118.pdf')
            draw_obj.DrawDetail(f4, inTITLE=the_title, outFIGtemplate = 'NNPDF31_nlo_pch_as_0118_nf_4.pdf')
        else:
            print('[INFO] No detailed plot generated')


    tag='leadingCvsB'
    task( DrawingProcess(draw_scatter_plot, get_data_point_barrel,'_'.join([tag,'barrelPho'])) )
    task( DrawingProcess(draw_scatter_plot, get_data_point_endcap,'_'.join([tag,'endcapPho'])) )
