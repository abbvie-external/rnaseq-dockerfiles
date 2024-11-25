#!/usr/bin/env python3

'''
'''

import argparse
import glob
import json
import os
import pprint
import sys

def get_file_paths(sample_dir_list):
    sample_count_dict = dict()
    for sample_dir in sample_dir_list:
        sample = os.path.basename(sample_dir)
        sample_count_dict[sample] = os.path.join(sample_dir,'kallisto','scaledcounts', sample+'.scaledcounts.tsv')
    return sample_count_dict

def get_sample_data(count_file):
    sample_dict = dict()
    with open(count_file, 'r') as f:
        header_line = f.readline().rstrip()
        for line in f:
            line_split = line.strip('\n').split('\t')
            gene_name = line_split[0]
            gene_count = line_split[1]
            sample_dict[gene_name] = gene_count
    return sample_dict

def get_counts(sample_count_dict):
    joined_dict = dict()
    for sample in sorted(sample_count_dict):
        sample_data = get_sample_data(sample_count_dict[sample])
        for gene_name in sample_data:
            if gene_name not in joined_dict:
                joined_dict[gene_name] = dict()
            joined_dict[gene_name][sample] = sample_data[gene_name]
    return joined_dict

def write_data(counts_table, project_id):
    with open(project_id+'.kallisto_quant.scaledcounts.tsv', 'w') as f:
        for i, row in enumerate(counts_table):
            line = '\t'.join(row)
            if i < len(counts_table):
                line += '\n'
            f.write(line)
    return

def fill_zeros(counts_data, sample_list):
    output_table = list()
    output_table.append(['trascript_id'] + sample_list)
    for gene_id in sorted(list(counts_data.keys())):
        gene_row = list()
        gene_row.append(gene_id)
        for sample in sample_list:
            if sample in counts_data[gene_id]:
                gene_row.append(counts_data[gene_id][sample])
            else:
                gene_row.append('0')
        output_table.append(gene_row)
    return output_table

def join_counts(project_id, sample_dir_list):
    sample_list = sorted([os.path.basename(x) for x in sample_dir_list])
    sample_count_dict = get_file_paths(sample_dir_list)

    counts_data = get_counts(sample_count_dict)
    counts_table = fill_zeros(counts_data, sample_list)
    write_data(counts_table, project_id)
    return

def main():
    parser = argparse.ArgumentParser(description='merge kallisto scaled tpm counts')
    parser.add_argument('-s', '--sample-dir',
                        action='append',
                        required=True)
    parser.add_argument('-p', '--project-id',
                        required=True)
    args = parser.parse_args()
    sample_dir_list = args.sample_dir
    project_id = args.project_id

    join_counts(project_id, sample_dir_list)
    return

if __name__ == '__main__':
    main()
