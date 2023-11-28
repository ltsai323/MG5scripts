#!/usr/bin/env sh

inJSON=$1
new_folder=`basename ${inJSON%.json}`
touch $new_folder ; /bin/rm -rf $new_folder
mkdir -p $new_folder
echo "[mkdir - LOG] Creating output folder $new_folder"


