#!/usr/bin/env python

import argparse
import json
import os
import sys

import pysam

def extract_readgroup_json(bam_path):
    bam_file = os.path.basename(bam_path)
    bam_name, bam_ext = os.path.splitext(bam_file)
    samfile = pysam.AlignmentFile(bam_path, 'rb', check_sq=False)
    samfile_header = samfile.header
    readgroup_dict_list = samfile_header['RG']
    if len(readgroup_dict_list) < 1:
        print(f'There are no readgroups in BAM: {bam_name}')
        print(f'\treadgroup: {readgroup_dict_list}')
        sys.exit(1)
    else:
        for readgroup_dict in readgroup_dict_list:
            print(f'readgroup_dict: {readgroup_dict}')
            readgroup_json_file = readgroup_dict['ID'] + '.json'
            readgroup_json_file = readgroup_json_file.replace('+','')
            print(f'readgroup_json_file: {readgroup_json_file}\n')
            with open(readgroup_json_file, 'w') as f:
                json.dump(readgroup_dict, f, ensure_ascii=False)
    return

def main():
    parser = argparse.ArgumentParser('convert readgroups to json')

    parser.add_argument('-b', '--bam_path',
                        required = True
    )

    args = parser.parse_args()
    bam_path = args.bam_path

    extract_readgroup_json(bam_path)
    return

if __name__ == '__main__':
    main()
