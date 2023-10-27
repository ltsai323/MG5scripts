#!/usr/bin/env python3

import csv
import sys
import ROOT
def RootEntries(inFILEname:str) -> float:
  rootfile = ROOT.TFile.Open(inFILEname)
  roottree = rootfile.Get('LHEF')
  return float(roottree.GetEntries())

def CSVEntries(inFILEname:str) -> float:
  with open(inFILEname,'r') as infile:
    csv_reader = csv.DictReader(infile)
    sum_entries = sum( [ float(d['yield']) for d in csv_reader ] )
    return sum_entries

if __name__ == "__main__":
  inDIR = sys.argv[1]

  inCSV = inDIR+'/MG5result_yieldCheckForStatistics.csv'
  csv_entries = CSVEntries(inCSV)

  inROOT = inDIR+'/MG5result.root'
  root_entries = RootEntries(inROOT)

  print(f'csv entries {csv_entries} / ref entries {root_entries} = {csv_entries / root_entries:.4f}')
