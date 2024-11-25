#!/usr/bin/env python3

import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description='merge featurecount reports')
    parser.add_argument('-s', '--species-json',
                        required=True)
    parser.add_argument('-k', '--gene-key',
                        required=False)
    parser.add_argument('-v', '--gene-value',
                        required=True)
    args = parser.parse_args()
    species_json = args.species_json
    gene_key = args.gene_key
    gene_value = args.gene_value
    with open(species_json, 'r') as f:
        data = json.load(f)
    data_dict = dict()
    for gene in data['genes']:
        data_dict[gene[gene_key]] = gene[gene_value]
    out_dict = dict()
    for key in sorted(list(data_dict.keys())):
        out_dict[key] = data_dict[key]
    infile = os.path.basename(species_json)
    infile_base, infile_ext = os.path.splitext(infile)
    outfile = infile_base+'_'+gene_key+'_'+gene_value+infile_ext
    with open(outfile, 'w') as f:
        json.dump(out_dict, f)
    return

if __name__ == '__main__':
    main()
