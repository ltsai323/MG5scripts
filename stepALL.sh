inDIR=$1
#inDIR=/wk_cms3/ltsai/wk_cms/ltsai/CMSSW/Run3Winter22/CMSSW_12_2_4/src/MG5_aMC_v3_5_0/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_bcONLY

sh      step0_dataConvertion.sh $inDIR

infile=`realpath $inDIR`.json # use output json file of step0
outdir=`basename $inDIR` # create a new directory in the same name here
echo -e "\n\nvvvvvvvvvvvvvv vvvvvvvvvvvvvvv  start step1_outputFOLDER_init.sh"
sh      step1_outputFOLDER_init.sh $infile
echo -e "\n\nvvvvvvvvvvvvvv vvvvvvvvvvvvvvv  start step2_MG5SecondaryHandler.py"
python3 step2_MG5SecondaryHandler.py $infile
echo -e "\n\nvvvvvvvvvvvvvv vvvvvvvvvvvvvvv  start step3_extractXSinCSV.py"
python3 step3_extractXSinCSV.py ${outdir}/MG5result.root
echo -e "\n\nvvvvvvvvvvvvvv vvvvvvvvvvvvvvv  start step3_extractYieldinCSV.noWeightForStatisticsChecking.py"
python3 step3_extractYieldinCSV.noWeightForStatisticsChecking.py ${outdir}/MG5result.root
echo -e "\n\nvvvvvvvvvvvvvv vvvvvvvvvvvvvvv  start step4_convertXStoFRACinCSV.py"
python3 step4_convertXStoFRACinCSV.py ${outdir}/MG5result.csv
