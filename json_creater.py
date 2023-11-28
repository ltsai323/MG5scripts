#!/usr/bin/env python3

def PrintHelp():
    print('automatically loads inputPATH/Events/run_summary.txt and create pt sorted root files')
    print('------- args -----')
    print('1. input madgraph directory name')
    exit(1)

import os

def ReadBinning(inPATH:str):
    with open(inPATH+'/Events/run_summary.txt','r') as ifile:
        valid_lines = ( line.strip() for line in ifile.readlines() if '(' in line )
        pt_rootFile_map = {}
        for line in valid_lines:
            bin_name,pt_cut = eval(line)
            root_file=bin_name+'.root'
            rel_root_file = inPATH+'/Events/'+root_file
            abs_root_file = os.path.abspath(rel_root_file)
            print(f'\n----- checking {rel_root_file}')

            pt_rootFile_map[pt_cut] = abs_root_file
            if not os.path.exists(abs_root_file):
                raise IOError(f'[File not found - Error] @pt{pt_cut}. {abs_root_file} doesn\'t exist')
            print(f'[LOG] valid {root_file}')
        print(f'[LOG] All related ROOT files prepared.')
        return pt_rootFile_map

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 1+1: PrintHelp()
    inPATH = sys.argv[1]
    if '/' == inPATH[-1]: inPATH = inPATH[:-1]
    if not os.path.exists(inPATH): raise IOError('[Folder not found - Error] {inPATH}')


    pt_rootFile_map = ReadBinning(inPATH)


    import json
    output_json_file = inPATH+'.json'
    with open(output_json_file,'w') as ofile:
        output_content = [
                { 'ptgmin': ptcut, 'rootfile': pt_rootFile_map[ptcut] }
                for ptcut in sorted(pt_rootFile_map.keys()) ]
        ofile.write( json.dumps(output_content, indent=2))
        print(f'[INFO] output file is {output_json_file}')

    if os.path.exists( os.path.basename(output_json_file) ):
        print(f'[Link existed - Warning] Output file {output_json_file} created. But no link put to current directory.')
    else:
        os.system(f'ln -s {output_json_file}')
        print(f'[Link Created - LOG] Output file {output_json_file} created. Create a link to current directory')
