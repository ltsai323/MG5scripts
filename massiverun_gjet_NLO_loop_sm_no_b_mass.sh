#!/usr/bin/env sh

function code_exec()
{ sh gjet_NLO_loop_sm_no_b_mass_general.sh $1 $2 > log_"$2" 2>&1 ; }
function code_test()
{ sh gjet_NLO_loop_sm_no_b_mass_general.sh $1 $2 ; }

#code_test 303400 TEST_NNPDF31_nlo_as_0118

code_exec 303400 NNPDF31_nlo_as_0118 &
code_exec 320500 NNPDF31_nlo_as_0118_nf_4 &
code_exec 303800 NNPDF31_nlo_pch_as_0118 &
code_exec 321500 NNPDF31_nlo_pch_as_0118_nf_4 &
wait
