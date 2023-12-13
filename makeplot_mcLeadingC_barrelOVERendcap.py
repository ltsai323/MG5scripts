#!/usr/bin/env python3
from makeplot_mcPredictedC_barrelOVERendcap import *


if __name__ == "__main__":
    import makeplot_file_collecter as inputs
    #f1 = inputs.Get(inputs.mcLeadingC_intrinsicC_0118_nf5        )
    #f2 = inputs.Get(inputs.mcLeadingC_intrinsicC_0118_nf4        )
    #f3 = inputs.Get(inputs.mcLeadingC_perturbativeC_0118_nf5     )
    #f4 = inputs.Get(inputs.mcLeadingC_perturbativeC_0118_nf4     )

    f1 = inputs.Get(inputs.mcLeadingC_intrinsicC_0118_nf5        )
    f2 = inputs.Get(inputs.mcLeadingC_perturbativeC_0118_nf5     )
    f3 = inputs.Get(inputs.mcLeadingC_perturbativeC_0118_nf3     )

    def task(draw_obj):
        draw_obj.DrawSingle( f1,f2,f3,
                inTITLE = '$\gamma$+c yield ratio to barrel over endcap in PDF NNPDF3.1 NLO',
            outFIGtemplate='all.pdf')

    tag = 'ratioOfBarrelCtoEndcapC_leadingJet'
    task( DrawingProcess(draw_scatter_plot,get_data_point,tag) )
