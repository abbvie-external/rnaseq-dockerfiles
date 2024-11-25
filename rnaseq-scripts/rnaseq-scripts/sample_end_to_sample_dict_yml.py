#!/usr/bin/env python

'''
'''


import argparse
import collections
import glob
import json
import os
import sys

import ruamel.yaml

def get_fastq_list(fastqdir):
    sample_dirs = glob.glob(os.path.join(fastqdir, '*.fastq.gz'))
    return sorted(list(sample_dirs))

def get_sample_dict(fastq_list):
    sample_dict = dict()
    for fastq_path in sorted(fastq_list):
        fastq_file = os.path.basename(fastq_path)
        fastq_info = fastq_file.rstrip('.fastq.gz')
        fastq_split = fastq_info.split('_')
        fastq_sample = fastq_split[5]

        if fastq_sample not in sample_dict:
            readgroup_dict = dict()
            readgroup_dict['forward_fastq'] = str()
            readgroup_dict['reverse_fastq'] = str()
            sample_dict[fastq_sample] = [readgroup_dict]

        fastq_read = fastq_split[2]
        if fastq_read == str(1):
            sample_dict[fastq_sample][0]['forward_fastq'] = fastq_path
        elif fastq_read == str(2):
            sample_dict[fastq_sample][0]['reverse_fastq'] = fastq_path
        else:
            print(f'unexpected fastq_read: {fastq_read}')
            print(f'fastq_path: {fastq_path}')
            sys.exit(1)
    sample_dict = dict(collections.OrderedDict(sorted(sample_dict.items())))
    return sample_dict

def write_samples_yml(projectname, projectdir, sample_dict):
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)
    yml_path = os.path.join(projectdir, projectname + '_sample_fastq.yml')
    with open(yml_path, 'w') as f:
        sample_data = yaml.dump(sample_dict, f)
    return yml_path

def main():
    parser = argparse.ArgumentParser(description='merge featurecount reports')
    parser.add_argument('-f', '--fastqdir',
                        required=True)
    parser.add_argument('-n', '--projectname',
                        required=True)
    parser.add_argument('-p', '--projectdir',
                        required=True)
    args = parser.parse_args()
    fastqdir = args.fastqdir
    projectname = args.projectname
    projectdir = args.projectdir

    fastq_list = get_fastq_list(fastqdir)
    sample_dict = get_sample_dict(fastq_list)
    yml_path = write_samples_yml(projectname, projectdir, sample_dict)
    return

if __name__ == '__main__':
    main()
