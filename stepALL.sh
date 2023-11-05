inDIR=$1
#inDIR=/wk_cms3/ltsai/wk_cms/ltsai/CMSSW/Run3Winter22/CMSSW_12_2_4/src/MG5_aMC_v3_5_0/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_bcONLY

#sh      step0_dataConvertion.sh $inDIR 30,55,100,135,175,200,220,300,400,500,700

infile=`basename $inDIR`.json
outdir=`basename $inDIR`
python3 step1_init.py $infile
python3 step2_MG5SecondaryHandler.py $infile
python3 step3_extractXSinCSV.py ${outdir}/MG5result.root
python3 step3_extractYieldinCSV.noWeightForStatisticsChecking.py ${outdir}/MG5result.root
python3 step4_convertXStoFRACinCSV.py ${outdir}/MG5result.csv
