#!/usr/bin/env sh
function code_exec() {
ptMIN=$1
ptMAX=$2
iFILE=$3
oTAG=$4

echo '[INFO] a.Loop('$ptMIN,$ptMAX,"$iFILE", "${oTAG}/frag_${ptMIN}_${ptMAX}.root"')'
root <<EOF
.L MG5SecondaryHandler.C
MG5SecondaryHandler a
a.Loop($ptMIN,$ptMAX,"$iFILE", "${oTAG}/frag_${ptMIN}_${ptMAX}.root")
EOF
}
