#!/usr/bin/env sh

#./py_mergeMG5Result.py in_mergeMG5Result.json
# outFolder=NLO_loop_sm_no_b_mass_NNPDF3p1nlo
# python3 ./py_mergeMG5Result.py in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_NNPDF3p1nlo.json
# outFolder=NLO_loop_sm_no_b_mass_CT14nlo
# python3 ./py_mergeMG5Result.py in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_CT14nlo.json
# outFolder=NLO_loop_sm_no_b_mass_CT14nnlo
# python3 ./py_mergeMG5Result.py in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_CT14nnlo.json
outFolder=NLO_loop_sm_no_b_mass_NNPDF3p1nnlo
python3 ./py_mergeMG5Result.py in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_NNPDF3p1nnlo.json

touch $outFolder
/bin/rm -r $outFolder
mkdir -p $outFolder
mv out* $outFolder/

echo ===========================================
echo output folder $outFolder
echo ===========================================
