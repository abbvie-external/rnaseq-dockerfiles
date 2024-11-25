#!/usr/bin/env python

'''
extract a single contig from a {g}vcf
'''

import argparse
from pathlib import Path

def write_contig(vcf, contig):
    outfile = Path(vcf.stem + '.' + contig + vcf.suffix)
    ct = contig + '\t'
    started_contig = False
    finished_contig = False
    with open(vcf, 'r') as f_read:
        with open(outfile, 'w') as f_write:
            for line in f_read:
                if line.startswith('#'):
                    f_write.write(line)
                elif line.startswith(ct):
                    started_contig = True
                    f_write.write(line)
                elif started_contig:
                    finished_contig = True
                    break
    return

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--vcf',
                        required=True)
    parser.add_argument('-c', '--contig',
                        required=True)
    args = parser.parse_args()
    vcf = Path(args.vcf)
    contig = args.contig
    write_contig(vcf, contig)
    return

if __name__ == '__main__':
    main()
