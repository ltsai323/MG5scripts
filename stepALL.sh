infile=$1
outdir="${infile%.json}"
python3 step1_init.py $infile
python3 step2_MG5SecondaryHandler.py $infile
python3 step3_extractXSinCSV.py ${outdir}/MG5result.root
python3 step3_extractYieldinCSV.noWeightForStatisticsChecking.py ${outdir}/MG5result.root
python3 step4_convertXStoFRACinCSV.py ${outdir}/MG5result.csv
