#!/usr/bin/env python3
import matplotlib.pyplot as plt
from makeplot_tools import  draw_EP
import makeplot_tools as myTool
from makeplot_tools import XYscatterPoints
from makeplot_tools import LoadCSVFile
from makeplot_ratiotool import TakeRatio
from makeplot_drawingprocess import DrawingProcess

def get_data_point(inCSVfileWITHdesc:(str,str)) -> XYscatterPoints:
    def get_data_point_(inCSVfile:str, desc:str,pETAbin:int,jETAbin:int) -> XYscatterPoints:
        value_pair = myTool.LoadCSVFile(inCSVfile, 'value', pETAbin,jETAbin)
        error_pair = myTool.LoadCSVFile(inCSVfile, 'error', pETAbin,jETAbin)

        pt_arr, values = myTool.GetXYscatterPOINT(value_pair)
        _     , errors = myTool.GetXYscatterPOINT(error_pair)

        return XYscatterPoints(x=pt_arr,y=values,y_err=errors,desc=desc)
    barrel_data_point = get_data_point_(inCSVfileWITHdesc[0],inCSVfileWITHdesc[1],0,0)
    endcap_data_point = get_data_point_(inCSVfileWITHdesc[0],inCSVfileWITHdesc[1],1,0)
    return list(TakeRatio( [endcap_data_point,barrel_data_point] ))[0]

def draw_scatter_plot(
        yRANGE:list,
        xySCATTERpointS:[XYscatterPoints],
        inTITLE:str = '$\gamma$+c yield ratio in barrel photon and endcap photon',
        outFIGname:str = 'h_testbarrelpho.png',
        ):

    draw_EP( xySCATTERpointS,
            yTITLE='ratio to $\gamma$+c in barrel/endcap',
            yRANGE = yRANGE,
            logY = False,
            inTITLE=inTITLE)
    plt.savefig(outFIGname)
    print(f'[fig output - LOG] {outFIGname}')
    plt.close()



if __name__ == "__main__":
    import makeplot_file_collecter as inputs
    #f1 = inputs.Get(inputs.mcPredictedC_intrinsicC_0118_nf5)
    #f2 = inputs.Get(inputs.mcPredictedC_intrinsicC_0118_nf4        )
    #f3 = inputs.Get(inputs.mcPredictedC_perturbativeC_0118_nf5     )
    #f4 = inputs.Get(inputs.mcPredictedC_perturbativeC_0118_nf4     )

    f1 = inputs.Get(inputs.mcPredictedC_intrinsicC_0118_nf5        )
    f2 = inputs.Get(inputs.mcPredictedC_perturbativeC_0118_nf5     )
    f3 = inputs.Get(inputs.mcPredictedC_perturbativeC_0118_nf3     )

    def task(draw_obj):
        the_title = '$\gamma$+c yield ratio in barrel photon and endcap photon in NNPDF3.1 NLO'
        draw_obj.DrawSingle( f1,f2,f3,
                inTITLE=the_title,
            outFIGtemplate='all.pdf')

    tag='ratioOfBarrelCtoEndcapC_predicted'
    task( DrawingProcess(draw_scatter_plot,get_data_point,tag) )
