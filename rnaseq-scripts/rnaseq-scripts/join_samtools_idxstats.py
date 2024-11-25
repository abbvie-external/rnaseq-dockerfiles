#!/usr/bin/env python3

'''
'''

import argparse
import glob
import json
import os
from pathlib import Path
import pprint
import sys

def get_file_paths(sample_dir_list):
    sample_count_dict = dict()
    for sample_dir in sample_dir_list:
        sample = os.path.basename(sample_dir)
        aligned_sample_path =  os.path.join(sample_dir,'bam_metrics','samtools',sample+'.Aligned.sortedByCoord.out.idxstats')
        dedup_sample_path =  os.path.join(sample_dir,'bam_metrics','samtools',sample+'.Aligned.dedup.idxstats')
        if Path(dedup_sample_path).exists():
            sample_count_dict[sample] = dedup_sample_path
        elif Path(aligned_sample_path).exists():
            sample_count_dict[sample] = aligned_sample_path
        else:
            print(f'Can not find per sample metrics file {sample_path} to join')
            raise Exception('path not found')
    return sample_count_dict

def get_count_data(count_file, column_number):
    count_dict = dict()
    with open(count_file, 'r') as f:
        for line in f:
            line_split = line.split('\t')
            contig = line_split[0].strip()
            count = str(int(line_split[column_number - 1].strip()))
            count_dict[contig] = count
    return count_dict

def join_counts(sample_count_dict, column_number):
    joined_dict = dict()
    for sample in sorted(sample_count_dict):
        count_data = get_count_data(sample_count_dict[sample], column_number)
        for gene in count_data:
            if gene not in joined_dict:
                joined_dict[gene] = dict()
            joined_dict[gene][sample] = count_data[gene]
    return joined_dict

def write_data(sample_list, project_id, counts_data):
    header = ['contig'] + sample_list
    output_table = list()
    output_table.append(header)
    for contig in counts_data:
        contig_row = list()
        contig_row.append(contig)
        for sample in sample_list:
            if sample in list(counts_data[contig].keys()):
                contig_row.append(counts_data[contig][sample])
            else:
                contig_row.append('0')
        output_table.append(contig_row)
    with open(project_id+'.samtools.idxstats.tsv', 'w') as f:
        for i, row in enumerate(output_table):
            line = '\t'.join(row)
            if i < len(output_table):
                line += '\n'
            f.write(line)
    return

def get_sample_list(sample_dir_list):
    sample_list = sorted([os.path.basename(x) for x in sample_dir_list])
    return sample_list

def join_data(project_id, sample_dir_list):
    count_position = 3

    sample_list = get_sample_list(sample_dir_list)
    sample_count_dict = get_file_paths(sample_dir_list)
    print(f'sample_count_dict:')

    pprint.pprint(sample_count_dict)

    counts_data = join_counts(sample_count_dict, count_position)
    write_data(sample_list, project_id, counts_data)
    return

def main():
    parser = argparse.ArgumentParser(description='merge samtools idxstats counts')
    parser.add_argument('-s', '--sample-dir',
                        action='append',
                        required=True)
    parser.add_argument('-p', '--project-id',
                        required=True)
    args = parser.parse_args()
    sample_dir_list = args.sample_dir
    project_id = args.project_id

    join_data(project_id, sample_dir_list)
    return

if __name__ == '__main__':
    main()
