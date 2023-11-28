inDIR=$1
#inDIR=/wk_cms3/ltsai/wk_cms/ltsai/CMSSW/Run3Winter22/CMSSW_12_2_4/src/MG5_aMC_v3_5_0/gjet_NLO_loop_sm_no_b_mass_NNPDF31_nlo_as_0118_bcONLY
function the_exit() { echo -e '\n----------\n'$1'\n------------\n\n'; exit; }

#  sh      step0_dataConvertion.sh $inDIR 30,55,100,135,175,200,220,300,400,500,700 || the_exit 'step0 failed'
#  
 infile=`basename $inDIR`.json
 outdir=`basename $inDIR`
#  python3 step1_init.py $infile || the_exit 'step1 failed'
#  python3 step2_MG5SecondaryHandler.py $infile || the_exit 'step2 failed'
#  #python3 step3_extractXSinCSV.py ${outdir}/MG5result.root || the_exit 'step3.1 failed'
python3 step3_extractYieldinCSV.noWeightForStatisticsChecking.py ${outdir}/MG5result.root || the_exit 'step3.2 failed'
#python3 step4_convertXStoFRACinCSV.py ${outdir}/MG5result.csv || the_exit 'step4 failed'
