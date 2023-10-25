#!/usr/bin/env
loadDIR=$1
loaddir=`realpath $loadDIR`
workdir=$loaddir/Events
exec_file=/afs/cern.ch/work/l/ltsai/Work/HiggsCombine/CMSSW_11_3_4/src/MG5_aMC_v3_4_2/ExRootAnalysis/ExRootLHEFConverter 

function the_exit() { echo [ERROR] $1; exit; }


cd $workdir
# -tr is important to keep the creation order in json creation
for trgdir in `ls -tr -d $workdir/*/`; do
    out_root=${trgdir%/}.root
    echo processing $out_root
    loadFILE=${trgdir}/events.lhe.gz
    processFILE=${trgdir}/events.lhe
    gzip -d $loadFILE # ignore the result
    

    $exec_file $processFILE $out_root > /dev/null || \
        the_exit "[INFO] $out_root failed creation"
done

