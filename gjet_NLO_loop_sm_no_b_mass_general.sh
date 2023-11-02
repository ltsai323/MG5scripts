#!/usr/bin/env sh
lhapdf_id=$1
lhapdf_name=$2

function the_exit() { echo -e "\n\n $1 \n\n"; exit 1; }
function init() {
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



## program start
out_folder=gjet_NLO_loop_sm_no_b_mass_${lhapdf_name}_bcONLY

touch $out_folder ; /bin/rm -rf $out_folder || the_exit "clean up failed"
run_file=$PWD/run_init_${lhapdf_name}.txt
init $run_file $out_folder || the_exit "initialize failed"
cd $out_folder || the_exit "change directory failed"
mv $run_file Events/

python3 ../run_card_generator.py $lhapdf_name $lhapdf_id || the_exit "run card generation failed"

### execute
for a in `ls -t Events/run_card_*.dat`; do
    cp $a Cards/run_card.dat || the_exit "failed to copy $a to run_card.dat"
    name_1=`basename $a`
    name_2=${name_1#run_card_}
    name=${name_2%.dat}

    ./bin/generate_events aMC@NLO -n $name -f 
    mv $a Events/accomplished/
done
