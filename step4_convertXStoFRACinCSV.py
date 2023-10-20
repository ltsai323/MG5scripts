#!/usr/bin/env python3


if __name__ == "__main__":
    inFILEname = sys.argv[1]
    #inFILEname = 'in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_CT14nlo/MG5result.csv'
    with open(inFILEname,'r') as infile:
        import csv
        csv_reader = csv.DictReader(infile)

        csv_out = []
        for evt in csv_reader:
            frac = lambda xNAME: float(evt[xNAME]) / float(evt['crossSection'])
            err  = lambda xNAME: 0

            fracL = frac('crossSectionL')
            fracC = frac('crossSectionC')
            fracB = frac('crossSectionB')

            fracLerr = err('hi')
            fracCerr = err('hi')
            fracBerr = err('hi')
            print( f'[INFO] bin {evt["pEtaBin"]}_{evt["jEtaBin"]}_{evt["pPtBin"]:2s}  fraction L/C/B = {fracL:10.5f} / {fracC:10.5f} / {fracB:10.5f}' )
            csv_out.append( {
                'pEtaBin': evt['pEtaBin'],
                'jEtaBin': evt['jEtaBin'],
                'pPtBin': evt['pPtBin'],
                'fracL': fracL,
                'fracLerr': fracLerr,
                'fracC': fracC,
                'fracCerr': fracCerr,
                'fracB': fracB,
                'fracBerr': fracBerr,
            } )

        newfilename = '.'.join( inFILEname.split('.')[:-1] ) + '_frac.csv'
        print(f'[LOG] Output csv file : {newfilename}')
        with open(newfilename, 'w') as newfile:
            csvwritter = csv.DictWriter(newfile, fieldnames=csv_out[0].keys())
            csvwritter.writeheader()
            csvwritter.writerows(csv_out)
