#!/usr/bin/env python3
import matplotlib.pyplot as plt
from makeplot_tools import XYscatterPoints
import makeplot_tools as myTool

def y_range_pair_finder( xySCATTERpointS:[XYscatterPoints], isLOGscale:bool ):
    y_range = ( (min(xy_scatter_point.y),max(xy_scatter_point.y)) for xy_scatter_point in xySCATTERpointS )
    output = [ ('rangeAuto', ()) ] # additional default value
    if isLOGscale:
        output.extend([ (f'range{idx}', (ymin*0.1,ymax*10.)) for idx,(ymin,ymax) in enumerate(y_range) ])
    else:
        output.extend([ (f'range{idx}', (1.1*ymin-0.1*ymax,1.1*ymax-0.1*ymin)) for idx,(ymin,ymax) in enumerate(y_range) ])
    return output
def yRangeFinder_LogScale(xySCATTERpointS):
    return y_range_pair_finder(xySCATTERpointS,True)
def yRangeFinder_LinearScale(xySCATTERpointS):
    return y_range_pair_finder(xySCATTERpointS,False)

class DrawingProcess:
    def __init__(self, singleDRAWINGfunc, hackDATAfunc, taG:str='sometag'):
        self._draw_func = singleDRAWINGfunc
        self._hack_data = hackDATAfunc
        self._tag = taG

    def DrawSingle(self,*inFILEwithDESCs,
            inTITLE:str = '',
            outFIGtemplate:str = 'thename.pdf',
            yRANGE:tuple = () ):

        datapoints = [ self._hack_data(in_tuple) for in_tuple in inFILEwithDESCs ]
        self._draw_func(yRANGE,datapoints, inTITLE=inTITLE, outFIGname='_'.join(['h',self._tag,outFIGtemplate]))


    def SetDetailPlotArgument(self, *tagANDrange):
        ''' tagANDrange: ('rangeL', (10.,500.)), ('rangeS',(10.,20.)) '''
        self.additional_filetag = [ filetag for filetag, y_range in tagANDrange ]
        self.additional_y_range = [ y_range for filetag, y_range in tagANDrange ]
    def SetAutoDetail(self, rangeFINDERfunc):
        self.additional_range_finder = rangeFINDERfunc

    def DrawDetail(self,*inFILEwithDESCs, inTITLE:str='', outFIGtemplate:str = 'thename.pdf'):
        looping = None
        if hasattr(self, 'additional_filetag'):
            looping = zip(self.additional_filetag,self.additional_y_range)
        elif hasattr(self, 'additional_range_finder'):
            datapoints = [ self._hack_data(in_tuple) for in_tuple in inFILEwithDESCs ]
            looping = list(self.additional_range_finder(datapoints))
            print(f'[hhhh] looping size {len(looping)}')
        if looping:
            for tag,y_range in looping:
                self.DrawSingle(*inFILEwithDESCs,
                        inTITLE = inTITLE,
                        outFIGtemplate = '_'.join([tag,outFIGtemplate]),
                        yRANGE = y_range)
        else:
            raise RuntimeError('[set argument first-ERROR] DrawingProcess::DrawBarrelPhoAndEndcapPho_Detail() attribute "additional_filetag" or "additional_range_finder" not found')


def __single_drawing_func__template__(
        yRANGE:list,
    xySCATTERpointS:[XYscatterPoints],
    outFIGname:str = 'h_testbarrelpho.png',
    ):
    from makeplot_tools import  draw_EP
    from makeplot_ratiotool import draw_EP_ratio

    print(f'[fig output - LOG] Generating {outFIGname}')
    draw_EP_ratio( xySCATTERpointS,
            yTITLE='weighed $\gamma$+c yield',
            yRANGE = yRANGE,
            logY = True,
            inTITLE='the comparison',
            ratioTITLE = 'leading / truth',
            ratioYrange = (0.3,1.1),
            )
    plt.savefig(outFIGname)
    plt.close()

class HackData:
    @staticmethod
    def barrel_data(inTUPLE:tuple) -> XYscatterPoints:
        ''' inTUPLE
        f1 = (
                'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_b.csv',
                'NNPDF3p1 NLO in 5NFS intrinsic charm')
        '''
        inCSVfile,desc=inTUPLE
        value_pair = myTool.LoadCSVFile(inCSVfile, 'value', 0,0)
        error_pair = myTool.LoadCSVFile(inCSVfile, 'error', 0,0)

        pt_arr, values = myTool.GetXYscatterPOINT(value_pair)
        _     , errors = myTool.GetXYscatterPOINT(error_pair)

        return XYscatterPoints(x=pt_arr,y=values,y_err=errors,desc=desc)
    @staticmethod
    def endcap_data(inTUPLE:tuple) -> XYscatterPoints:
        ''' inTUPLE
        f1 = (
                'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_b.csv',
                'NNPDF3p1 NLO in 5NFS intrinsic charm')
        '''
        inCSVfile,desc=inTUPLE
        value_pair = myTool.LoadCSVFile(inCSVfile, 'value', 1,0)
        error_pair = myTool.LoadCSVFile(inCSVfile, 'error', 1,0)

        pt_arr, values = myTool.GetXYscatterPOINT(value_pair)
        _     , errors = myTool.GetXYscatterPOINT(error_pair)

        return XYscatterPoints(x=pt_arr,y=values,y_err=errors,desc=desc)
if __name__ == "__main__":
    f1 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118/MG5result_mcPredicted_c.csv',
            'NNPDF3p1 NLO in 5NFS intrinsic charm')
    f2 = (
            'gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_nf_4/MG5result_mcPredicted_c.csv',
            'NNPDF3p1 NLO in 4NFS intrinsic charm')


    draw_barrel = DrawingProcess(__single_drawing_func__template__, HackData.barrel_data, 'barrelPho')

    draw_barrel.DrawSingle( f1,f2,
            outFIGtemplate='all_truthC.pdf')
    draw_barrel.DrawSingle( f1,
            outFIGtemplate='NNPDF31_nlo_as_0118_truthC.pdf')

    draw_barrel.SetDetailPlotArgument(
            ('rangeAuto', None),
            ('rangeHuge', (1e-3,300.)),
            ('rangeTiny', (1e-2,5.)),
            )
    draw_barrel.DrawDetail(f1,f2, outFIGtemplate = 'intrinsicC_truthC.pdf')
