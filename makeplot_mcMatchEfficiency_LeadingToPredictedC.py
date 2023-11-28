#!/usr/bin/env python3
from makeplot_ratiotool import TakeRatio
import matplotlib.pyplot as plt
from makeplot_tools import  draw_EP
from makeplot_ratiotool import draw_EP_ratio
from makeplot_tools import XYscatterPoints
from makeplot_drawingprocess import DrawingProcess,HackData
import makeplot_tools as myTool

def draw_scatter_plot(
        yRANGE:list,
        xySCATTERpointS:[XYscatterPoints],
        inTITLE:str = '',
        outFIGname:str = 'h_testbarrelpho.png',
        ):

    print(f'[fig output - LOG] Generating {outFIGname}')
    draw_EP_ratio( xySCATTERpointS,
            yTITLE='weighed $\gamma$+c yield',
            yRANGE = yRANGE,
            logY = True,
            inTITLE=inTITLE,
            ratioTITLE = 'Matching Eff',
            ratioYrange = (0.3,1.05),
            )
    plt.savefig(outFIGname)
    plt.close()


def get_data_point_barrel(inTUPLE:tuple) -> XYscatterPoints:
    ''' inTUPLE like
    f1 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv',
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_b.csv',
            'NNPDF3p1 NLO in 5NFS intrinsic charm')
    '''
    pETAbin,jETAbin = (0,0)
    def get_data_point_(inCSVfile:str, desc:str,pETAbin:int,jETAbin:int) -> XYscatterPoints:
        value_pair = myTool.LoadCSVFile(inCSVfile, 'value', pETAbin,jETAbin)
        error_pair = myTool.LoadCSVFile(inCSVfile, 'error', pETAbin,jETAbin)

        pt_arr, values = myTool.GetXYscatterPOINT(value_pair)
        _     , errors = myTool.GetXYscatterPOINT(error_pair)

        return XYscatterPoints(x=pt_arr,y=values,y_err=errors,desc=desc)

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
    def get_data_point_(inCSVfile:str, desc:str,pETAbin:int,jETAbin:int) -> XYscatterPoints:
        value_pair = myTool.LoadCSVFile(inCSVfile, 'value', pETAbin,jETAbin)
        error_pair = myTool.LoadCSVFile(inCSVfile, 'error', pETAbin,jETAbin)

        pt_arr, values = myTool.GetXYscatterPOINT(value_pair)
        _     , errors = myTool.GetXYscatterPOINT(error_pair)

        return XYscatterPoints(x=pt_arr,y=values,y_err=errors,desc=desc)

    c_data_point = get_data_point_(inTUPLE[0],inTUPLE[2],pETAbin,jETAbin)
    b_data_point = get_data_point_(inTUPLE[1],inTUPLE[2],pETAbin,jETAbin)
    inputdatapoint = [b_data_point,c_data_point]
    return list(TakeRatio(inputdatapoint))[0]


def draw_scatter_plot_ratio(
        yRANGE:list,
        xySCATTERpointS:[XYscatterPoints],
        inTITLE:str = 'truth $\gamma$+c / $\gamma$+b',
        outFIGname:str = 'h_testbarrelpho.png',
        ):

    print(f'[fig output - LOG] Generating {outFIGname}')
    draw_EP( xySCATTERpointS,
            yTITLE = 'weighed $\gamma$+c yield',
            yRANGE = yRANGE,
            logY = False,
            inTITLE = inTITLE)
    plt.savefig(outFIGname)
    plt.close()
if __name__ == "__main__":
    f1P = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv',
            'truth $\gamma$+c')
    f1L = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_c.csv',
            'leading $\gamma$+c')
    f2P = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_c.csv',
            'truth $\gamma$+c')
    f2L = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv',
            'leading $\gamma$+c')
    f3P = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_c.csv',
            'truth $\gamma$+c')
    f3L = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_c.csv',
            'leading $\gamma$+c')
    f4P = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_c.csv',
            'truth $\gamma$+c')
    f4L = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv',
            'leading $\gamma$+c')
    def task(draw_obj):
        draw_obj.DrawSingle( f1P,f1L,inTITLE='$\gamma$+c yield from 5NFS intrinsic charm',outFIGtemplate = 'NNPDF31_nlo_as_0118.pdf')
        draw_obj.DrawSingle( f2P,f2L,inTITLE='$\gamma$+c yield from 4NFS intrinsic charm',outFIGtemplate = 'NNPDF31_nlo_as_0118_nf_4.pdf')
        draw_obj.DrawSingle( f3P,f3L,inTITLE='$\gamma$+c yield from 5NFS perturbative charm',outFIGtemplate = 'NNPDF31_nlo_pch_as_0118.pdf')
        draw_obj.DrawSingle( f4P,f4L,inTITLE='$\gamma$+c yield from 4NFS perturbative charm',outFIGtemplate = 'NNPDF31_nlo_pch_as_0118_nf_4.pdf')

    tag = 'LeadingCEff'
    task( DrawingProcess(draw_scatter_plot,HackData.barrel_data,'_'.join([tag,'barrelPho'])) )
    task( DrawingProcess(draw_scatter_plot,HackData.endcap_data,'_'.join([tag,'endcapPho'])) )



    f1 = ( f1L[0],f1P[0], '5NFS intrinsic charm' )
    f2 = ( f2L[0],f2P[0], '4NFS intrinsic charm' )
    f3 = ( f3L[0],f3P[0], '5NFS perturbative charm' )
    f4 = ( f4L[0],f4P[0], '4NFS perturbative charm' )

    def task(draw_obj):
        draw_obj.DrawSingle( f1,f2,f3,f4 ,inTITLE='Matching efficiency between $\gamma$+leading jet over $\gamma$+c',outFIGtemplate = 'all.pdf')

    tag = 'LeadingCEff'
    task( DrawingProcess(draw_scatter_plot_ratio,get_data_point_barrel,'_'.join([tag,'barrelPho'])) )
    task( DrawingProcess(draw_scatter_plot_ratio,get_data_point_endcap,'_'.join([tag,'endcapPho'])) )
