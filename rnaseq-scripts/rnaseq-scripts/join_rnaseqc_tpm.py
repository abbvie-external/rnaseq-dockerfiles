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
        aligned_sample_tpm_path =  os.path.join(sample_dir,'bam_metrics','rnaseqc',sample+'.Aligned.sortedByCoord.out.bam.gene_tpm.gct')
        dedup_sample_tpm_path =  os.path.join(sample_dir,'bam_metrics','rnaseqc',sample+'.Aligned.dedup.bam.gene_tpm.gct')
        if Path(dedup_sample_tpm_path).exists():
            sample_count_dict[sample] = dedup_sample_tpm_path
        elif Path(aligned_sample_tpm_path).exists():
            sample_count_dict[sample] = aligned_sample_tpm_path
        else:
            raise Exception(f"Can't find per sample metrics file {dedup_sample_file_path} or {aligned_sample_file_path} to join!")
    return sample_count_dict

def get_gene_value(line_split, index_list):
    gene_value_list = list()
    for num in index_list:
        gene_value = line_split[num].replace(',',';')
        gene_value_list.append(gene_value)
    gene_value = ','.join(gene_value_list)
    return gene_value

def get_index_list(header_line, gene_header_names):
    print('get_index_list()')
    print(f'header_line: {header_line}')
    print(f'gene_header_names: {gene_header_names}')
    index_list = list()
    header_split = header_line.split('\t')
    for name in gene_header_names:
        name_index = header_split.index(name)
        index_list.append(name_index)
    return index_list

def get_count_data(count_file, gene_header_names):
    count_dict = dict()
    with open(count_file, 'r') as f:
        version_line = f.readline().rstrip()
        genecount_line = f.readline().rstrip()
        header_line = f.readline().rstrip()
        index_list = get_index_list(header_line, gene_header_names)
        for line in f:
            line_split = line.split('\t')
            gene_value = get_gene_value(line_split, index_list)
            count = line_split[-1].rstrip('\n')
            count_dict[gene_value] = count
    return count_dict

def join_counts(sample_count_dict, header_names):
    joined_dict = dict()
    for sample in sorted(sample_count_dict):
        count_data = get_count_data(sample_count_dict[sample], header_names)
        for gene in count_data:
            if gene not in joined_dict:
                joined_dict[gene] = dict()
            joined_dict[gene][sample] = count_data[gene]
    return joined_dict

def write_data(sample_list, project_id, counts_data, header_names):
    header = header_names + sample_list
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
    with open(project_id+'.rnaseqc.gene_tpm.tsv', 'w') as f:
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
    count_header_names = ['Name']

    sample_list = get_sample_list(sample_dir_list)
    sample_count_dict = get_file_paths(sample_dir_list)
    print(f'sample_count_dict:')

    pprint.pprint(sample_count_dict)

    counts_data = join_counts(sample_count_dict, count_header_names)
    write_data(sample_list, project_id, counts_data, count_header_names)
    return

def main():
    parser = argparse.ArgumentParser(description='merge rnaseqc tpm counts')
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
