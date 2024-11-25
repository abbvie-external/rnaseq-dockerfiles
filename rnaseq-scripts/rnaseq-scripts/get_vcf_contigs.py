#!/usr/bin/env python

'''
get list of contigs from a {g}vcf
'''

import argparse
import json
from pathlib import Path

def get_contigs(vcf):
    contig_list = list()
    with open(vcf, 'r') as f_open:
        for line in f_open:
            if not line.startswith('##'):
                break
            if line.startswith('##contig=<ID='):
                contig = line.split('=')[2].split(',')[0]
                contig_list.append(contig)
    return contig_list

def write_contigs(contig_list, file_name):
    out_file = Path(file_name + '.json')
    with open(out_file, 'w') as f:
        json.dump(contig_list, f)
    return

def write_txts(contig_list):
    for i, contig in enumerate(contig_list, 1):
        outfile = Path(str(i).rjust(4,'0') + '.txt')
        with open(outfile, 'w') as f_out:
            f_out.write(contig.strip())
    return

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--vcf',
                        required=True)
    args = parser.parse_args()
    vcf = Path(args.vcf)
    contig_list = get_contigs(vcf)
    write_contigs(contig_list, vcf.stem)
    # write_txts(contig_list)
    return

if __name__ == '__main__':
    main()
