inFOLDER=$1
inPTcut=30,55,100,140,200,300,500


sh convertTOroot.sh $inFOLDER
#python3 json_creater.py $inFOLDER creationTime $inPTcut
python3 json_creater.py $inFOLDER defaultOrder $inPTcut
