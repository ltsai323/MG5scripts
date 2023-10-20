#!/usr/bin/env python3


def ListRootFiles(inPATH:str):
    import os
    rootfiles = []
    objdir = inPATH+'/Events/'

    contents = os.listdir(objdir)
    # creation time orderd to let ptgmin from small to large
    contents = sorted(contents, key=lambda item: os.path.getctime(os.path.join(objdir, item)))
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
    inPATH = sys.argv[1]
    if '/' == inPATH[-1]: inPATH = inPATH[:-1]
    ptgminLIST = sys.argv[2:]

    root_files = ListRootFiles(inPATH)
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

