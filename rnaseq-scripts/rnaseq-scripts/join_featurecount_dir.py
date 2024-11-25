#!/usr/bin/env python

'''
'''


import argparse
import glob
import json
import os
import sys

def get_sample_list(inputdir):
    sample_dirs = glob.glob(os.path.join(inputdir, '*'))
    sample_list = [os.path.basename(x) for x in sample_dirs]
    return sorted(sample_list)


def get_file_paths(inputdir, sample_list):
    sample_count_dict = dict()
    sample_jcount_dict = dict()
    for sample in sample_list:
        sample_count_dict[sample] = os.path.join(inputdir,sample,'featurecounts',sample+'.Aligned.sortedByCoord.out.bam.counts')
        sample_jcount_dict[sample] = os.path.join(inputdir,sample,'featurecounts',sample+'.Aligned.sortedByCoord.out.bam.counts.jcounts')
    return sample_count_dict, sample_jcount_dict


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


def get_count_data(count_file, gene_header_names):
    count_dict = dict()
    with open(count_file, 'r') as f:
        header_line = f.readline()
        if header_line.startswith('#'):
            header_line = f.readline()
        index_list = get_index_list(header_line, gene_header_names)
        for line in f:
            line_split = line.split('\t')
            gene_value = get_gene_value(line_split, index_list)
            if '_PAR_Y' in gene_value:
                continue
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

def write_data(sample_list, ens_hgnc_data, project_id, counts_data, header_names, count_type):
    hugo = False
    if len(header_names) == 1:
        header = ['gene_symbol'] + header_names + sample_list
        hugo = True
    else:
        header = header_names + sample_list
    output_table = list()
    output_table.append(header)
    for ens_gene in sorted(counts_data):
        gene_row = list()
        if hugo:
            hgnc_gene = ens_hgnc_data.get(ens_gene.split('.')[0])
            gene_row.append(hgnc_gene)
        if ',' in ens_gene:
            gene_row = ens_gene.split(',')
        else:
            gene_row.append(ens_gene)
        for sample in sample_list:
            if sample in list(counts_data[ens_gene].keys()):
                gene_row.append(counts_data[ens_gene][sample])
            else:
                gene_row.append('0')
        output_table.append(gene_row)
    with open(project_id+'_featurecounts.'+count_type, 'w') as f:
        for i, row in enumerate(output_table):
            line = '\t'.join(row)
            if i < len(output_table):
                line += '\n'
            f.write(line)
    return


def join_data(inputdir, ens_hgnc_data, project_id):
    count_header_names = ['Geneid']
    jcount_header_names = ['PrimaryGene','SecondaryGenes',
                           'Site1_chr','Site1_location','Site1_strand',
                           'Site2_chr','Site2_location','Site2_strand']
    sample_list = get_sample_list(inputdir)
    sample_count_dict, sample_jcount_dict = get_file_paths(inputdir, sample_list)
    counts_data = join_counts(sample_count_dict, count_header_names)
    jcounts_data = join_counts(sample_jcount_dict, jcount_header_names)
    write_data(sample_list, ens_hgnc_data, project_id, counts_data, count_header_names, 'counts')
    write_data(sample_list, ens_hgnc_data, project_id, jcounts_data, jcount_header_names, 'jcounts')
    return


def main():
    parser = argparse.ArgumentParser(description='merge featurecount reports')
    parser.add_argument('-i', '--inputdir',
                        required=True)
    parser.add_argument('-e', '--ens-hgnc-json',
                        required=True)
    parser.add_argument('-p', '--project-id',
                        required=True)
    args = parser.parse_args()
    with open(args.ens_hgnc_json, 'r') as f:
        ens_hgnc_data = json.load(f)
    join_data(args.inputdir, ens_hgnc_data, args.project_id)
    return

if __name__ == '__main__':
    main()
