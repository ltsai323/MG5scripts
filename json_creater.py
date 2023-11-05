#!/usr/bin/env python3

def PrintHelp():
    print('------- args -----')
    print('1. input madgraph directory name')
    print('2. sorting method. The available string is "creationTime" and "defaultOrder"')
    print('3. ptgmin definition. Separated by "," or " "\n\n')
    exit(1)

import os
def ListRootFiles(inPATH:str, sortingMETHOD:str):
    rootfiles = []
    objdir = inPATH+'/Events/'

    contents = os.listdir(objdir)
    if sortingMETHOD == 'creationTime':
        # creation time orderd to let ptgmin from small to large
        contents = sorted(contents, key=lambda item: os.path.getctime(os.path.join(objdir, item)))
    elif sortingMETHOD == 'defaultOrder':
        contents = sorted(contents)
    else:
        PrintHelp()
    for items in contents:
        if len(items) < 6: continue
        if not items.endswith('.root'): continue
        rootfiles.append( os.path.abspath(objdir+items) )
    return rootfiles

def PtGmin(rawPTGminLIST, sizeOFrootFILEs:int):
    sizeOFptgminLIST = len(rawPTGminLIST)

    out = rawPTGminLIST
    if sizeOFptgminLIST == 0: out = [0] * sizeOFrootFILEs
    if sizeOFptgminLIST == 1: out = rawPTGminLIST[0].split(',')

    if len(out) != sizeOFrootFILEs:
        raise IOError(f'[Error] Input pt min cuts({len(out)}) is incompetible with loaded root files ({sizeOFrootFILEs})')
    return out

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2+1: PrintHelp()
    inPATH = sys.argv[1]
    if '/' == inPATH[-1]: inPATH = inPATH[:-1]

    # 'creationTime' and 'defaultOrder'
    sortingMETHOD = sys.argv[2]


    hasptSetup = len(sys.argv)>2
    ptgminLIST = sys.argv[3:] if hasptSetup else []

    root_files = ListRootFiles(inPATH, sortingMETHOD)
    print('[INFO] Loaded Root Files')
    for rootfile in root_files:
        print('  ->  '+rootfile)


    ptgmin_list = PtGmin(ptgminLIST,len(root_files))


    import json
    output_json_file = inPATH+'.json'
    with open(output_json_file,'w') as ofile:
        output_content = [
                { 'ptgmin': ptcut, 'rootfile': rootfile }
                for ptcut,rootfile in zip(ptgmin_list,root_files) ]
        ofile.write( json.dumps(output_content, indent=2))
        print(f'[INFO] output file is {output_json_file}')

    os.system(f'ln -s {output_json_file}')

