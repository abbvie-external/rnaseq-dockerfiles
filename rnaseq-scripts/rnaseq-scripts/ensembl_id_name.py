#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='merge featurecount reports')
    parser.add_argument('-s', '--species-json',
                        required=True)
    args = parser.parse_args()
    species_json = Path(args.species_json)
    with open(species_json, 'r') as f:
        data = json.load(f)

    data_dict = dict()
    no_name = list()
    for gene in data['genes']:
        if 'name' in gene:
            data_dict[gene['id']] = gene['name']
        else:
            no_name.append(gene['id'])
    out_dict = dict()
    for key in sorted(list(data_dict.keys())):
        out_dict[key] = data_dict[key]

    outfile = Path(species_json.stem+'.tsv')
    with open(outfile, 'w') as f:
        for item in out_dict:
            f.write(item+'\t'+out_dict[item]+'\n')

    with open(species_json.stem+'.noname.tsv', 'w') as f:
        for item in no_name:
            f.write(item+'\n')
    return

if __name__ == '__main__':
    main()
