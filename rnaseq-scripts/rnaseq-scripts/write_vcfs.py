#!/usr/bin/env python

'''
get list of contigs from a {g}vcf
'''

import argparse
import json
from pathlib import Path

def get_vcf_header(vcf):
    vcf_header = list()
    with open(vcf, 'r') as f_read:
        for line in f_read:
            if not line.startswith('#'):
                break
            vcf_header.append(line)
    return vcf_header

def write_header(f_write, vcf_header):
    for line in vcf_header:
        f_write.write(line)
    return

def write_empty_files(vcf, vcf_header, start, finish):
    for pos in range(start, finish):
        out_file = Path(vcf.stem + '.' + str(pos).rjust(4,'0') + vcf.suffix)
        with open(out_file, 'w') as f_write:
            for line in vcf_header:
                f_write.write(line)
    return

def write_contigs(vcf, contig_list):
    vcf_header = get_vcf_header(vcf)
    current_contig = None
    i = 1
    with open(vcf, 'r') as f_read:
        for line in f_read:
            if line.startswith('#'):
                continue
            else:
                this_contig = line.split('\t')[0]
                if current_contig is None:
                    current_contig = this_contig
                    pos = contig_list.index(current_contig)+1
                    if pos > i:
                        write_empty_files(vcf, vcf_header, i, pos)
                    i = pos
                    out_file = Path(vcf.stem + '.' + str(pos).rjust(4,'0') + vcf.suffix)
                    f_write = open(out_file, 'w')
                    write_header(f_write, vcf_header)
                    f_write.write(line)
                elif this_contig == current_contig:
                    f_write.write(line)
                else:
                    f_write.close()
                    current_contig = this_contig
                    i += 1
                    pos = contig_list.index(current_contig)+1
                    if pos > i:
                        write_empty_files(vcf, vcf_header, i, pos)
                    out_file = Path(vcf.stem + '.' + str(pos).rjust(4,'0') + vcf.suffix)
                    f_write = open(out_file, 'w')
                    write_header(f_write, vcf_header)
                    f_write.write(line)
        f_write.close()
    if contig_list.index(current_contig)+1 < len(contig_list):
        write_empty_files(vcf, vcf_header, contig_list.index(current_contig)+1, len(contig_list)+1)
    return

def read_contig_list(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    return json_data

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--vcf',
                        required=True)
    parser.add_argument('-j', '--json',
                        required=True)
    args = parser.parse_args()
    vcf_path = Path(args.vcf)
    json_path = Path(args.json)
    contig_list = read_contig_list(json_path)
    
    write_contigs(vcf_path, contig_list)
    return

if __name__ == '__main__':
    main()
