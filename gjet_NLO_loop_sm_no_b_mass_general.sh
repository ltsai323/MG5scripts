#!/usr/bin/env sh
lhapdf_id=$1
lhapdf_name=$2

function the_exit() { echo -e "\n\n $1 \n\n"; exit 1; }
function the_echo() { echo -e "[gjet_NLO_loop_sm_no_b_mass_general.sh] $1"; }
function MG5_initConfiguration() {
runFILE=$1
outFOLDER=$2
cat > $runFILE <<EOF
set lhapdf lhapdf-config
import model loop_sm-no_b_mass
define bc = b b~ c c~
generate p p > bc a [QCD]
output $outFOLDER
EOF
./bin/mg5_aMC $runFILE || the_exit "run file $runFILE is not able to initialize ./bin/mg5_aMC";
mkdir $outFOLDER/Events/accomplished;
}
function MG5_runConfiguration() {
lhapdfNAME=$1
lhapdfID=$2
python3 ../run_card_generator.py $1 $2;
}
function MG5_appendRunConfiguration() {
lhapdfNAME=$1
lhapdfID=$2
python3 ../run_card_generator.py $1 $2 bin011 33;
}
function MG5_generateEvent() {
### in the sub directory
for a in `ls -t Events/run_card_*.dat`; do
    cp $a Cards/run_card.dat || the_exit "failed to copy $a to run_card.dat"
    name_1=`basename $a`
    name_2=${name_1#run_card_}
    name=${name_2%.dat}

    ./bin/generate_events aMC@NLO -n $name -f  && mv $a Events/accomplished/ || the_exit "$name execution failed"
done
}



out_folder=gjet_NLO_loop_sm_no_b_mass_${lhapdf_name}_bcONLY
if [ $# -eq 2 ]; then
    #### execute all program
    the_echo 'creat new MG5 repository'

    ## program start
    touch $out_folder ; /bin/rm -rf $out_folder || the_exit "clean up failed"
    run_file=$PWD/run_init_${lhapdf_name}.txt
    MG5_initConfiguration $run_file $out_folder || the_exit "initialize failed"
    cd $out_folder || the_exit "change directory failed"
    mv $run_file Events/

    MG5_runConfiguration $lhapdf_name $lhapdf_id || the_exit "run card generation failed"
    MG5_generateEvent
elif [ $3 == "append" ] ; then
    the_echo "append new runs into existing MG5 repository: $out_folder"

    cd $out_folder || the_exit "change directory failed"
    MG5_appendRunConfiguration $lhapdf_name $lhapdf_id || the_exit "run card generation failed"
    ##MG5_generateEvent
    
else
    ## test python code only
    the_echo "test mode creating run_card_blahblah.txt to $out_folder"

    touch $out_folder ; /bin/rm -rf $out_folder || the_exit "clean up failed"
    mkdir -p ${out_folder}/Events
    cd $out_folder
    MG5_runConfiguration $lhapdf_name $lhapdf_id || the_exit "run card generation failed"
fi
