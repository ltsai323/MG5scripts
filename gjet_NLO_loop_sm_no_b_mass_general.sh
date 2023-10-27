#!/usr/bin/env sh
lhapdf_id=$1
lhapdf_name=$2
out_folder=gjet_NLO_loop_sm_no_b_mass_${lhapdf_name}

touch $out_folder ; /bin/rm -rf $out_folder

run_info=info_${out_folder}.txt
cat > $run_info <<EOF
Used LHAPDF PDF set : $lhapdf_name
            ID : $lhapdf_id
EOF


mg5_script=run_${out_folder}.txt
cat > $mg5_script <<EOF
set lhapdf /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/external/slc7_amd64_gcc900/bin/lhapdf-config
set fastjet /afs/cern.ch/work/l/ltsai/Work/HiggsCombine/CMSSW_11_3_4/src/MG5_aMC_v3_4_2/HEPTools/fastjet/bin/fastjet-config
import model loop_sm-no_b_mass
generate p p > j a [QCD]
output $out_folder
EOF

function fill_run_info() {
inLABEL=$1
phoPTmin=$2
cat >> $mg5_script <<EOF
launch -n $inLABEL
set pdlabel = lhapdf
set lhaid = $lhapdf_id
set nevents 100000
set ebeam 6500
set ebeam 6500
set ptj = 30
set etaj = 2.4
set ptgmin = $phoPTmin
set etagamma = 2.5
EOF
}

#fill_run_info bin1 30
#fill_run_info bin2 55
#fill_run_info bin3 100
fill_run_info bin4 140
#fill_run_info bin5 200
#fill_run_info bin6 300
#fill_run_info bin7 500

./bin/mg5_aMC $mg5_script

mv $mg5_script $out_folder/Events/
mv $run_info   $out_folder/Events/


