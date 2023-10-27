#!/usr/bin/env python3


import csv

import sys

if __name__ == "__main__":
    infile = 'MG5result_frac.csv'

    with open(infile,'r') as ifile:
        csvreader = csv.DictReader(ifile)

        cc = [ rr for rr in csvreader ]
        frac_barrelPho = [ float(v['fracC']) for v in cc if v['pEtaBin']=='0' and v['jEtaBin']=='0' ]
        frac_endcapPho = [ float(v['fracC']) for v in cc if v['pEtaBin']=='1' and v['jEtaBin']=='0' ]
        print(frac_barrelPho)
        print(frac_endcapPho)
        print(frac_barrelPho)



