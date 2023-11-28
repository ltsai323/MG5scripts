inFOLDER=`realpath $1`

function the_exit() { echo -e "\n\n--- Error ---\n$1"; exit; }
outJSONfile=${inFOLDER}.json
linkedJSONfile=`basename $outJSONfile`

if [ -e "$linkedJSONfile" ]; then
    echo -e "\n[Message - Warning] json file $linkedJSONfile existed. Previously information is"
    ls -l $linkedJSONfile
    echo "[Deleted - Warning] Previous link destroyed."
    unlink $linkedJSONfile || the_exit "[Unlink failed - Error] $linkedJSONfile is not a link"
fi
sh convertTOroot.sh $inFOLDER || the_exit "[Execution failed - Error] Unable to successfully execute convertTOroot.sh"
python3 json_creater.py $inFOLDER || the_exit "[Execution failed - Error] Unable to successfully execute json_creater.py"
