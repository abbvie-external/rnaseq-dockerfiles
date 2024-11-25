
#!/usr/bin/env python3

'''
'''

import argparse
import os

import json

def get_idx_vals(samplesheet):
    ss_idx = dict()
    with open(samplesheet, 'r') as f_open:
        for line in f_open:
            if line.startswith('Lane,') or line.startswith('Sample_ID,'):
                line = line.strip()
                line_split = line.split(',')
                ss_idx['Sample_ID'] = line_split.index('Sample_ID')
                ss_idx['Sample_Project'] = line_split.index('Sample_Project')
                break
    return ss_idx    


def get_projects_samples(samplesheet, ss_idx):
    data = dict()
    data['projects'] = set()
    data['samples'] = set()
    in_data = False
    with open(samplesheet, 'r') as f_open:
        for line in f_open:
            if in_data:
                line_split = line.split(',')
                sample_id = line_split[ss_idx['Sample_ID']]
                project_id = line_split[ss_idx['Sample_Project']]
                data['projects'].add(project_id)
                data['samples'].add(sample_id)
            if line.startswith('Lane,') or line.startswith('Sample_ID,'):
                in_data = True
    data_list = dict()
    data_list['projects'] = sorted(list(data['projects']))
    data_list['samples'] = sorted(list(data['samples']))
    return data_list

def write_vals(data):
    out_path = 'samplesheet_projects_samples.json'
    with open(out_path, 'w') as f:
        projects_samples_data = json.dump(data, f)
    print(f'projects_samples_data: {data}')
    return out_path


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', '--samplesheet',
                        required=True)
    args = parser.parse_args()
    samplesheet = args.samplesheet

    ss_idx = get_idx_vals(samplesheet)
    data = get_projects_samples(samplesheet, ss_idx)
    write_vals(data)
    return

if __name__ == '__main__':
    main()
