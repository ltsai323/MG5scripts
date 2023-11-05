inFOLDER=`realpath $1`
inPTcut=$2


sh convertTOroot.sh $inFOLDER
#python3 json_creater.py $inFOLDER creationTime $inPTcut
python3 json_creater.py $inFOLDER defaultOrder $inPTcut
