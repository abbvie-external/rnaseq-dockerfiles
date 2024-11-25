#!/usr/bin/env python3

'''
'''

import argparse
import glob
import json
import os
from pathlib import Path
import sys

def get_file_paths(attribute_type, feature_type, sample_dir_list):
    sample_counts_dict = dict()
    sample_junccounts_dict = dict()
    for sample_dir in sample_dir_list:
        sample = os.path.basename(sample_dir)
        aligned_sample_counts_path =  os.path.join(sample_dir,'bam_metrics','featurecounts',sample+'.Aligned.sortedByCoord.out.bam.'+feature_type+'.'+attribute_type+'.counts')
        aligned_sample_junccounts_path = os.path.join(sample_dir,'bam_metrics','featurecounts',sample+'.Aligned.sortedByCoord.out.bam.'+feature_type+'.'+attribute_type+'.counts.jcounts')
        dedup_sample_counts_path =  os.path.join(sample_dir,'bam_metrics','featurecounts',sample+'.Aligned.dedup.bam.'+feature_type+'.'+attribute_type+'.counts')
        dedup_sample_junccounts_path = os.path.join(sample_dir,'bam_metrics','featurecounts',sample+'.Aligned.dedup.bam.'+feature_type+'.'+attribute_type+'.counts.jcounts')
        if Path(dedup_sample_counts_path).exists():
            sample_counts_dict[sample] = dedup_sample_counts_path
            sample_junccounts_dict[sample] = dedup_sample_junccounts_path
        elif Path(aligned_sample_counts_path).exists():
            sample_counts_dict[sample] = aligned_sample_counts_path
            sample_junccounts_dict[sample] = aligned_sample_junccounts_path
        else:
            raise Exception(f"Can't find per sample metrics file {dedup_sample_file_path} or {aligned_sample_file_path} to join!")
    return sample_counts_dict, sample_junccounts_dict

def get_index_list(header_line, gene_header_names):
    index_list = list()
    header_split = header_line.split('\t')
    for gene_header in gene_header_names:
        gene_index = header_split.index(gene_header)
        index_list.append(gene_index)
    return index_list

def get_gene_value(line_split, index_list):
    gene_value_list = list()
    for num in index_list:
        gene_value = line_split[num].replace(',',';')
        gene_value_list.append(gene_value)
    gene_value = ','.join(gene_value_list)
    return gene_value

def get_counts_data(counts_file, gene_header_names):
    counts_dict = dict()
    with open(counts_file, 'r') as f:
        header_line = f.readline()
        if header_line.startswith('#'):
            header_line = f.readline()
        index_list = get_index_list(header_line, gene_header_names)
        for line in f:
            line_split = line.split('\t')
            gene_value = get_gene_value(line_split, index_list)
            if '_PAR_Y' in gene_value:
                continue
            counts = line_split[-1].rstrip('\n')
            counts_dict[gene_value] = counts
    return counts_dict

def join_counts(sample_counts_dict, header_names):
    joined_dict = dict()
    for sample in sorted(sample_counts_dict):
        counts_data = get_counts_data(sample_counts_dict[sample], header_names)
        for gene in counts_data:
            if gene not in joined_dict:
                joined_dict[gene] = dict()
            joined_dict[gene][sample] = counts_data[gene]
    return joined_dict

def write_data(sample_list, project_id, counts_data, header_names, counts_type, attribute_type, feature_type):
    header = header_names + sample_list
    with open(project_id+'.'+feature_type+'.'+attribute_type+'.'+counts_type+'.featurecounts.tsv', 'w') as f:
        f.write('\t'.join(header) + '\n')
        for ens_gene in sorted(counts_data):
            gene_row = list()
            if ',' in ens_gene:
                gene_row = ens_gene.split(',')
            else:
                gene_row.append(ens_gene)
            for sample in sample_list:
                if sample in list(counts_data[ens_gene].keys()):
                    gene_row.append(counts_data[ens_gene][sample])
                else:
                    gene_row.append('0')
            gene_line = '\t'.join(gene_row) + '\n'
            f.write(gene_line)
    return

def get_sample_list(sample_dir_list):
    sample_list = sorted([os.path.basename(x) for x in sample_dir_list])
    return sample_list

def join_data(attribute_type, project_id, sample_dir_list, aggregation_type, feature_type):
    counts_header_names = ['Geneid']
    junccounts_header_names = ['PrimaryGene','SecondaryGenes',
                               'Site1_chr','Site1_location','Site1_strand',
                               'Site2_chr','Site2_location','Site2_strand']

    sample_list = get_sample_list(sample_dir_list)
    sample_counts_dict, sample_junccounts_dict = get_file_paths(attribute_type, feature_type, sample_dir_list)
    if aggregation_type == 'counts':
        counts_data = join_counts(sample_counts_dict, counts_header_names)
        write_data(sample_list, project_id, counts_data, counts_header_names, 'counts', attribute_type, feature_type)
    if aggregation_type == 'junccounts':
        junccounts_data = join_counts(sample_junccounts_dict, junccounts_header_names)
        write_data(sample_list, project_id, junccounts_data, junccounts_header_names, 'junccounts', attribute_type, feature_type)
    return

def main():
    parser = argparse.ArgumentParser(description='merge featurecounts reports')
    parser.add_argument('-a', '--attribute-type', # exon_id, gene_id, transcript_id
                        required=True)
    parser.add_argument('-f', '--feature-type', # CDS, exon, gene, transcript
                        required=True)
    parser.add_argument('-s', '--sample-dir',
                        action='append',
                        required=True)
    parser.add_argument('-p', '--project-id',
                        required=True)
    parser.add_argument('-t', '--aggregation-type', # counts || junccounts
                        required=True)
    
    args = parser.parse_args()
    attribute_type = args.attribute_type
    sample_dir_list = args.sample_dir
    project_id = args.project_id
    aggregation_type = args.aggregation_type
    feature_type = args.feature_type

    join_data(attribute_type, project_id, sample_dir_list, aggregation_type, feature_type)
    return

if __name__ == '__main__':
    main()
