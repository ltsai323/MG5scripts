#!/usr/bin/env pythonb3

import json

bash_function = '''#!/usr/bin/env sh
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
'''

if __name__ == "__main__":
    import os

    tmp_func_file = open('tmp_func.sh','w')
    tmp_func_file.write(bash_function)
    tmp_func_file.close()
    bash_cmd_template = 'source ${{PWD}}/tmp_func.sh && code_exec {ptL} {ptR} "{inROOT}"  "{outTAG}"'


    import sys
    #$infile = 'in_mergeMG5Result.gjet_NLO_loop_sm_no_b_mass_CT14nlo.json'
    infile = sys.argv[1]
    filename = os.path.basename(infile)
    outtag = os.path.splitext(filename)[0]


    output_folder = outtag
    if not os.path.exists(output_folder): raise IOError(f'[step2_MG5SecondaryHandler.py-Error] - output folder {output_folder} not found')
    if not os.path.isdir(output_folder): raise IOError(f'[step2_MG5SecondaryHandler.py-Error] - output folder {output_folder} not found')
    with open(infile,'r') as infile:
        loadList = json.load(infile)
        for idx,loadItem in enumerate(loadList):
            inRoot = loadItem['rootfile']
            ptLow = int(loadItem['ptgmin'])
            ptHigh= int(loadList[idx+1]['ptgmin'] if idx+1 < len(loadList) else 9999.)
            print( f'{ptLow} to {ptHigh} in root file {inRoot}')
            bash_cmd = bash_cmd_template.format(
                    ptL=ptLow,
                    ptR=ptHigh,
                    inROOT=inRoot,
                    outTAG=outtag)
            print('[INFO] executing command ', bash_cmd)
            os.system(bash_cmd)

    cmd_hadd = f'hadd {outtag}/MG5result.root {outtag}/frag_*.root'
    print('[INFO]', cmd_hadd)
    os.system(cmd_hadd)
    os.remove('tmp_func.sh')

