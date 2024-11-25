#!/usr/bin/env python3

import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='ensembl species json to tx2gene tsv')
    parser.add_argument('-s', '--species-json',
                        required=True)
    args = parser.parse_args()
    species_json = args.species_json
    with open(species_json, 'r') as f:
        data = json.load(f)
    data_dict = dict()
    for gene in data['genes']:
        gn_id = gene['id']
        for tx in gene['transcripts']:
            tx_id = tx['id']
            if tx_id in data_dict:
                print(f'tx_id: {tx_id} is duplicate')
                sys.exit(1)
            else:
                data_dict[tx_id] = gn_id
    out_dict = dict()
    for key in sorted(list(data_dict.keys())):
        out_dict[key] = data_dict[key]
    infile = os.path.basename(species_json)
    infile_base, infile_ext = os.path.splitext(infile)
    outfile = infile_base+'.tx2gene.tsv'
    with open(outfile, 'w') as f:
        f.write('transcript\tgene\n')
        for item in out_dict:
            f.write(item+'\t'+out_dict[item]+'\n')
    return

if __name__ == '__main__':
    main()
