#!/usr/bin/env python3
import matplotlib.pyplot as plt
from makeplot_tools import  draw_EP
from makeplot_ratiotool import draw_EP_ratio
from makeplot_tools import XYscatterPoints
from makeplot_drawingprocess import DrawingProcess,HackData

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
            ratioTITLE = 'ratio',
            ratioYrange = (0.5,1.5),
            )
    plt.savefig(outFIGname)
    plt.close()



if __name__ == "__main__":
    f1 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_leading_c.csv',
            '5NFS intrinsic charm')
    f2 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv',
            '4NFS intrinsic charm')
    f3 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118/MG5result_mcPredicted_leading_c.csv',
            '5NFS perturbative charm')
    f4 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_pch_as_0118_nf_4/MG5result_mcPredicted_leading_c.csv',
            '4NFS perturbative charm')

    def task(draw_obj):
        the_title = '$\gamma$+c yield predicted by PDF NNPDF3.1 NLO'
        draw_obj.DrawSingle( f1,f2,f3,f4,
                inTITLE = the_title,
            outFIGtemplate='all.pdf')
        draw_obj.DrawSingle( f1,
                inTITLE = the_title,
            outFIGtemplate='NNPDF31_nlo_as_0118.pdf')
        draw_obj.DrawSingle( f2,
                inTITLE = the_title,
            outFIGtemplate='NNPDF31_nlo_as_0118_nf_4.pdf')
        draw_obj.DrawSingle( f3,
                inTITLE = the_title,
            outFIGtemplate='NNPDF31_nlo_pch_as_0118.pdf')
        draw_obj.DrawSingle( f4,
                inTITLE = the_title,
            outFIGtemplate='NNPDF31_nlo_pch_as_0118_nf_4.pdf')

        printDetailComparison = True
        if printDetailComparison:
            print('[INFO] Generate detailed plot')
            draw_obj.SetDetailPlotArgument(
                    ('rangeAuto', None),
                    ('rangeHuge', (1e-3,300.)),
                    ('rangeTiny', (1e-2,5.)),
                    )
            draw_obj.DrawDetail(f1,f2, inTITLE=the_title, outFIGtemplate = 'intrinsicC.pdf')
            draw_obj.DrawDetail(f3,f4, inTITLE=the_title, outFIGtemplate = 'perturbativeC.pdf')
            draw_obj.DrawDetail(f1,f3, inTITLE=the_title, outFIGtemplate = 'NF5.pdf')
            draw_obj.DrawDetail(f2,f4, inTITLE=the_title, outFIGtemplate = 'NF4.pdf')
        else:
            print('[INFO] No detailed plot generated')

    tag = 'leadingC'
    task( DrawingProcess(draw_scatter_plot,HackData.barrel_data,'_'.join([tag,'barrelPho'])) )
    task( DrawingProcess(draw_scatter_plot,HackData.endcap_data,'_'.join([tag,'endcapPho'])) )
