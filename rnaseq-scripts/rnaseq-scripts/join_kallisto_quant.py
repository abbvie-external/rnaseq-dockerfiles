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
        sample_count_dict[sample] = os.path.join(sample_dir,'kallisto', 'quant','abundance.tsv')
    return sample_count_dict

def get_index_dict(header_line, header_names):
    index_dict = dict()
    header_split = header_line.split('\t')
    for name in header_names:
        name_index = header_split.index(name)
        index_dict[name] = name_index
    return index_dict

def get_sample_data(data_key, data_val, header_names, count_file):
    sample_dict = dict()
    with open(count_file, 'r') as f:
        header_line = f.readline().rstrip()
        index_dict = get_index_dict(header_line, header_names)
        for line in f:
            line_split = line.strip('\n').split('\t')
            gene_name = line_split[index_dict[data_key]]
            gene_count = line_split[index_dict[data_val]]
            sample_dict[gene_name] = gene_count
    return sample_dict

def get_quants(data_key, data_val, header_names, sample_count_dict):
    joined_dict = dict()
    for sample in sorted(sample_count_dict):
        sample_data = get_sample_data(data_key, data_val, header_names, sample_count_dict[sample])
        for gene_name in sample_data:
            if gene_name not in joined_dict:
                joined_dict[gene_name] = dict()
            joined_dict[gene_name][sample] = sample_data[gene_name]
    return joined_dict

def write_data(counts_data, data_key, data_val, project_id, sample_list):
    header = [data_key] + sample_list
    output_table = list()
    output_table.append(header)
    for ens_gene in sorted(counts_data):
        gene_row = list()
        gene_row.append(ens_gene)
        for sample in sample_list:
            if sample in list(counts_data[ens_gene].keys()):
                gene_row.append(counts_data[ens_gene][sample])
            else:
                gene_row.append('0')
        output_table.append(gene_row)
    with open(project_id+'.kallisto_quant.abundance.'+data_val+'.tsv', 'w') as f:
        for i, row in enumerate(output_table):
            line = '\t'.join(row)
            if i < len(output_table):
                line += '\n'
            f.write(line)
    return

def get_sample_list(sample_dir_list):
    sample_list = sorted([os.path.basename(x) for x in sample_dir_list])
    print('sample_list:')
    pprint.pprint(sample_list)
    return sample_list

def join_quants(data_key, data_val, header_names, project_id, sample_dir_list):
    sample_list = get_sample_list(sample_dir_list)
    sample_count_dict = get_file_paths(sample_dir_list)

    print(f'sample_count_dict:')
    pprint.pprint(sample_count_dict)

    counts_data = get_quants(data_key, data_val, header_names, sample_count_dict)
    write_data(counts_data, data_key, data_val, project_id, sample_list)
    return

def main():
    parser = argparse.ArgumentParser(description='merge rnaseqc tpm counts')
    parser.add_argument('-s', '--sample-dir',
                        action='append',
                        required=True)
    parser.add_argument('-p', '--project-id',
                        required=True)
    parser.add_argument('-t', '--data-type',
                        choices=['length', 'eff_length', 'est_counts', 'tpm'],
                        required=True)
    args = parser.parse_args()
    sample_dir_list = args.sample_dir
    project_id = args.project_id
    data_val = args.data_type

    header_names = ['target_id', 'length', 'eff_length', 'est_counts', 'tpm']
    data_key = header_names[0]

    join_quants(data_key, data_val, header_names, project_id, sample_dir_list)
    return

if __name__ == '__main__':
    main()
