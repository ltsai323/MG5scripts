#!/usr/bin/env python3
if __name__ == "__main__":
    import os
    import sys
    injson = sys.argv[1]

    outdir = '.'.join( injson.split('.')[:-1] )
    os.mkdir(outdir)
