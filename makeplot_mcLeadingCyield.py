#!/usr/bin/env python3
import matplotlib.pyplot as plt
from makeplot_tools import  draw_EP
from makeplot_ratiotool import draw_EP_ratio
from makeplot_tools import XYscatterPoints
from makeplot_drawingprocess import DrawingProcess,HackData
from makeplot_drawingprocess import yRangeFinder_LinearScale

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
    import makeplot_file_collecter as inputs
    f1 = inputs.Get(inputs.mcLeadingC_intrinsicC_0118_nf5)
    f2 = inputs.Get(inputs.mcLeadingC_perturbativeC_0118_nf5)
    f3 = inputs.Get(inputs.mcLeadingC_perturbativeC_0118_nf3)

    def task(draw_obj):
        the_title = '$\gamma$+c yield predicted by PDF NNPDF3.1 NLO'
        draw_obj.DrawSingle( f1,f2,f3, inTITLE = the_title,
            outFIGtemplate='all.pdf')
        draw_obj.DrawSingle( f1, inTITLE = the_title,
            outFIGtemplate='NNPDF31_nlo_as_0118.pdf')
        draw_obj.DrawSingle( f2, inTITLE = the_title,
            outFIGtemplate='NNPDF31_nlo_pch_as_0118.pdf')
        draw_obj.DrawSingle( f3, inTITLE = the_title,
            outFIGtemplate='NNPDF31_nlo_pch_as_0118_nf3.pdf')

        printDetailComparison = True
        if printDetailComparison:
            print('[INFO] Generate detailed plot')
            draw_obj.SetDetailPlotArgument(
                    ('rangeAuto', None),
                    ('rangeHuge', (1e-3,300.)),
                    ('rangeTiny', (1e-2,5.)),
                    )
            draw_obj.DrawDetail(f1,f2, inTITLE=the_title, outFIGtemplate = 'NF5.pdf')
            draw_obj.DrawDetail(f2,f3, inTITLE=the_title, outFIGtemplate = 'perturbativeC.pdf')
            draw_obj.DrawDetail(f1,f3, inTITLE=the_title, outFIGtemplate = 'mainTrg.pdf')
        else:
            print('[INFO] No detailed plot generated')

    tag = 'leadingC'
    task( DrawingProcess(draw_scatter_plot,HackData.barrel_data,'_'.join([tag,'barrelPho'])) )
    task( DrawingProcess(draw_scatter_plot,HackData.endcap_data,'_'.join([tag,'endcapPho'])) )
