#!/usr/bin/env sh
lhapdf_name=$2
lhapdf_id=$1
out_folder=gjet_NLO_loop_sm_no_b_mass_$lhapdf_name

touch $out_folder ; /bin/rm -rf $out_folder

cat > run.info <<EOF
Used LHAPDF PDF set : $lhapdf_name
            ID : $lhapdf_id
EOF


cat > run.txt <<EOF
import model loop_sm-no_b_mass
generate p p > j a [QCD]
output $out_folder
EOF

function fill_run_info_endcapPho() {
inLABEL=$1
phoPTmin=$2
cat >> run.txt <<EOF
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
{22: 1.566} = eta_min_pdg
EOF
}
function fill_run_info_barrelPho() {
inLABEL=$1
phoPTmin=$2
cat >> run.txt <<EOF
launch -n $inLABEL
set pdlabel = lhapdf
set lhaid = $lhapdf_id
set nevents 100000
set ebeam 6500
set ebeam 6500
set ptj = 30
set etaj = 2.4
set ptgmin = $phoPTmin
set etagamma = 1.4442
EOF
}
function fill_run_info() {
fill_run_info_barrelPho $1 $2;
fill_run_info_endcapPho $1 $2;
}

fill_run_info bin1 30
fill_run_info bin2 55
fill_run_info bin3 100
fill_run_info bin4 140
fill_run_info bin5 200
fill_run_info bin6 300
fill_run_info bin7 500

./bin/mg5_aMC run.txt | tee run.log

#mv log_*  $out_folder/Events/
#mv run_*  $out_folder/Events/
mv run.log  $out_folder/Events/
mv run.info $out_folder/Events/


