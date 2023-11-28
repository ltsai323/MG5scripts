#!/usr/bin/env python3
from makeplot_mcPredictedC_barrelOVERendcap import *


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
        draw_obj.DrawSingle( f1,f2,f3,f4,
                inTITLE = '$\gamma$+c yield ratio to barrel over endcap in PDF NNPDF3.1 NLO',
            outFIGtemplate='all.pdf')

    tag = 'ratioOfBarrelCtoEndcapC_leadingJet'
    task( DrawingProcess(draw_scatter_plot,get_data_point,tag) )
