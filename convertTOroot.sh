#!/usr/bin/env
loadDIR=$1
loaddir=`realpath $loadDIR`
workdir=$loaddir/Events
exec_file=/wk_cms3/ltsai/wk_cms/ltsai/CMSSW/Run3Winter22/CMSSW_12_2_4/src/MG5_aMC_v3_5_0/ExRootAnalysis/ExRootLHEFConverter

function the_exit() { echo [ERROR] $1; exit; }


cd $workdir
echo change to $workdir
# -t is important to keep the creation order in json creation
for trgdir in `ls -t -d $workdir/*/`; do
    out_root=${trgdir%/}.root
    loadFILE=${trgdir}/events.lhe.gz
    processFILE=${trgdir}/events.lhe

    echo -e "\n------ checking directory `basename $trgdir`"
    if [ -e $loadFILE ]; then gzip -d $loadFILE ;
    else echo "[File not found - ignore unzip] `basename $loadFILE`"   ; fi
    if [ ! -e $processFILE ]; then
        echo "[File not found - skip convert] `basename $processFILE`" ; continue; fi
    if [ -e $out_root ]; then
        echo "[File existed - skip convert] `basename $out_root`"      ; continue; fi

    echo "[status] `basename $out_root`"
    $exec_file $processFILE $out_root > /dev/null || \
        the_exit "[INFO] $out_root failed creation"
done

