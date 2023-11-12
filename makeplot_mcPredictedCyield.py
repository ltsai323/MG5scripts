#!/usr/bin/env python3
import matplotlib.pyplot as plt


from makeplot_tools import draw_EP_ratio, draw_EP

def DrawRatioBarrelPho(inFILEwithDESCs:list, inTITLE:str, outFIGname:str = 'h_testbarrelpho.png'):
    draw_EP_ratio(inFILEwithDESCs, 0,0,
            yTITLE='$\gamma$+c yield',
            yRANGE = (1e-4, 1e4),
            logY = True,
            ratioTITLE = 'ratio',
            inTITLE=inTITLE,
            )
    plt.savefig(outFIGname)
    print(f'[fig output - LOG] {outFIGname}')
def DrawRatioEndcapPho(inFILEwithDESCs:list, inTITLE:str, outFIGname:str = 'h_testbarrelpho.png'):
    draw_EP_ratio(inFILEwithDESCs, 1,0,
            yTITLE='$\gamma$+c yield',
            yRANGE = (1e-4, 1e4),
            logY = True,
            ratioTITLE = 'ratio',
            inTITLE=inTITLE)
    plt.savefig(outFIGname)
    print(f'[fig output - LOG] {outFIGname}')
def DrawBarrelPho(inFILEwithDESCs:list, inTITLE:str, outFIGname:str = 'h_testbarrelpho.png'):
    draw_EP(inFILEwithDESCs, 0,0,
            yTITLE='$\gamma$+c yield',
            #yRANGE = (1e-5, 1e4),
            inTITLE=inTITLE)
    plt.savefig(outFIGname)
    print(f'[fig output - LOG] {outFIGname}')
def DrawEndcapPho(inFILEwithDESCs:list, inTITLE:str, outFIGname:str = 'h_testbarrelpho.png'):
    draw_EP(inFILEwithDESCs, 1,0,
            yTITLE='$\gamma$+c yield',
            #yRANGE = (1e-5, 1e4),
            inTITLE=inTITLE)
    plt.savefig(outFIGname)
    print(f'[fig output - LOG] {outFIGname}')
def DrawAllPhoRegion(inFILEwithDESCs:list, inTITLE:str, outFIGtemplate:str = 'h_test_{region}.png' ):
    DrawBarrelPho(inFILEwithDESCs,inTITLE+' in barrel photon', outFIGtemplate.format(region='barrelPho'))
    DrawEndcapPho(inFILEwithDESCs,inTITLE+' in endcap photon', outFIGtemplate.format(region='endcapPho'))
    DrawRatioBarrelPho(inFILEwithDESCs,inTITLE+' in barrel photon', outFIGtemplate.format(region='ratio_barrelPho'))
    DrawRatioEndcapPho(inFILEwithDESCs,inTITLE+' in endcap photon', outFIGtemplate.format(region='ratio_endcapPho'))

if __name__ == "__main__":
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
    DrawAllPhoRegion(infile_withdesc,
            inTITLE = 'truth C yield',outFIGtemplate = 'h_truthC_ALL_{region}.pdf')


    printDetailComparison = True
    if printDetailComparison:
        print('[INFO] Generate detailed plot')
        infile_withdesc = ( f1,f2 )
        DrawAllPhoRegion(infile_withdesc,
                inTITLE = 'truth C yield',outFIGtemplate = 'h_truthC_intrinsicC_{region}.pdf')


        infile_withdesc = ( f3,f4 )
        DrawAllPhoRegion(infile_withdesc,
                inTITLE = 'truth C yield',outFIGtemplate = 'h_truthC_perturbativeC_{region}.pdf')


        infile_withdesc = ( f1,f3 )
        DrawAllPhoRegion(infile_withdesc,
                inTITLE = 'truth C yield',outFIGtemplate = 'h_truthC_NF5_{region}.pdf')


        infile_withdesc = ( f2,f4 )
        DrawAllPhoRegion(infile_withdesc,
                inTITLE = 'truth C yield',outFIGtemplate = 'h_truthC_NF4_{region}.pdf')
