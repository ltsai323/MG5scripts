
infile=in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_CT14nlo.json
outdir="${infile%.json}"
python3 step1_init.py $infile
python3 step2_MG5SecondaryHandler.py $infile
python3 step3_extractXSinCSV.py ${outdir}/MG5result.root
python3 step3_extractXSinCSV.noweight.py ${outdir}/MG5result.root
python3 step4_convertXStoFRACinCSV.py ${outdir}/MG5result.csv
