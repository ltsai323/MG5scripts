#!/usr/bin/env python3


if __name__ == "__main__":
    import sys
    inFILEname = sys.argv[1]
    #inFILEname = 'in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_CT14nlo/MG5result.csv'


    print(f'[INFO] at file {inFILEname}')
    with open(inFILEname,'r') as infile:
        import csv
        csv_reader = csv.DictReader(infile)

        for evt in csv_reader:
            vv = lambda xNAME: float(evt[xNAME])
            vvA = vv('crossSection')
            vvL = vv('crossSectionL')
            vvC = vv('crossSectionC')
            vvB = vv('crossSectionB')
            print( f'[INFO] bin {evt["pEtaBin"]}_{evt["jEtaBin"]}_{evt["pPtBin"]:2s} {vvA:12.5f} - {vvL:12.5f} - {vvC:12.5f} - {vvB:12.5f} = net value = {100.*((vvA-vvL-vvC-vvB)/vvA):8.5f} %')
