#!/usr/bin/env python3
import ROOT
import csv


def phosel(pETAbin) -> str:
    if pETAbin == 0:
        return 'fabs(Particle_Eta[phoIdx])<1.4442'
    if pETAbin == 1:
        cut_endcapPho1 = 'fabs(Particle_Eta[phoIdx])>1.566'
        cut_endcapPho2 = 'fabs(Particle_Eta[phoIdx])<2.5'
        return f'{cut_endcapPho1} && {cut_endcapPho2}'

def jetsel(jETAbin) -> str:
    if jETAbin == 0:
        return 'fabs(Particle_Eta[jetIdx])<1.5'
    if jETAbin == 1:
        cut_endcapJet1 = 'fabs(Particle_Eta[jetIdx])>1.5'
        cut_endcapJet2 = 'fabs(Particle_Eta[jetIdx])<2.4'
        return f'{cut_endcapJet1} && {cut_endcapJet2}'

# add bin width to denominator to find cross section
def yield_to_crosssection(pETAbin,jETAbin, hiST) -> None:
    etabin_width = 1.
    if pETAbin == 0: etabin_width *= 1.4442*2.
    if pETAbin == 1: etabin_width *= (1.566-1.4442)*2.


    for ptbin in range(1,hiST.GetNbinsX()+1):
        evt_weight = 1./( hiST.GetBinWidth(ptbin) * etabin_width )
        hiST.SetBinContent( ptbin, hiST.GetBinContent(ptbin) * evt_weight )
        hiST.SetBinError  ( ptbin, hiST.GetBinError  (ptbin) * evt_weight )


class CSVWriter:
    def __init__(self, outNAME:str):
        self.ofile = outNAME
        self.content = []
    def Write(self):
        with open(self.ofile, 'w') as newfile:
            csvwritter = csv.DictWriter(newfile, fieldnames=self.content[0].keys())
            csvwritter.writeheader()
            csvwritter.writerows(self.content)

    def append_data(self, inputDATA) -> None:
        self.content.append(inputDATA)

    @classmethod
    def yield_and_error(cls, theTH1:ROOT.TH1F):
        max_pt_bin = theTH1.GetNbinsX() # from 0 to max-1
        vals = [ theTH1.GetBinContent(ptbin+1) for ptbin in range(max_pt_bin) ]
        errs = [ theTH1.GetBinError  (ptbin+1) for ptbin in range(max_pt_bin) ]
        return [ (val,err) for val,err in zip(vals,errs) ]
