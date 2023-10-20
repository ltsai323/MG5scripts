#!/usr/bin/env
loadDIR=$1
loaddir=`realpath $loadDIR`

exec_file=/afs/cern.ch/work/l/ltsai/Work/HiggsCombine/CMSSW_11_3_4/src/MG5_aMC_v3_4_2/ExRootAnalysis/ExRootLHEFConverter 


# -tr is important to keep the creation order in json creation
for trgdir in `ls -tr -d $loaddir/Events/*/`; do
    out_root=${trgdir%/}.root
    echo processing $out_root

    cp $trgdir/events.lhe.gz tmp.gz && gzip -d tmp.gz && $exec_file tmp $out_root > /dev/null && /bin/rm tmp || echo "[INFO] $out_root failed creationg"
done

