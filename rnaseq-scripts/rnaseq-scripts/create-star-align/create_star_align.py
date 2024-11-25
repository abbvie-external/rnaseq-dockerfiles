#!/usr/bin/env python3

import argparse
import copy
import csv
import glob
import gzip
import os
import pprint
import re
import sys
import uuid

import ruamel.yaml
import pandas as pd

def get_sample_list(sample_data, design_csv):
    sample = sample_data['SAMPLE']
    if isinstance(sample, dict):
        if list(sample.keys())[0] == 'csv':
            csv_file = sample['csv']['file']
            print('csv_file: {}'.format(csv_file))
            csv_column = sample['csv']['column']
            print('csv_column: {}'.format(csv_column))
            assert(os.path.basename(design_csv) == csv_file)
            csv_df = pd.read_csv(design_csv)
            sample_list = list(csv_df[csv_column])
            print('sample_list: {}'.format(sample_list))
    cleaned_list = [x for x in sample_list if isinstance(x, str)]
    if len(cleaned_list) == 0:
        cleaned_list = [str(x).rstrip('.0') for x in sample_list]
        new_list = list()
        for item in cleaned_list:
            if '.' in item:
                item_split = item.split('.')
                sec_item = item_split[1][:len(item_split[0])]
                new_item = item_split[0] + '.' + sec_item
                new_list.append(new_item)
            else:
                new_list.append(item)
        cleaned_list = new_list
    for cleaned in cleaned_list:
        print('{0}: {1}'.format(cleaned, type(cleaned)))
    print('cleaned_list:')
    pprint.pprint(cleaned_list)
    return cleaned_list


def get_sample_fastq_dict(sample_list, fastq_dir):
    sample_fastq_dict = dict()
    print('get_sample_fastq_dict() sample_list: {}'.format(sample_list))
    for sample in sorted(sample_list):
        print('\tsample: {}'.format(sample))
        sample_fastq_prefix = os.path.join(fastq_dir,sample)
        fastq_list = glob.glob(sample_fastq_prefix + '_*')
        if len(fastq_list) == 0:
            fastq_list = glob.glob(sample_fastq_prefix + '.*')
        pprint.pprint('fastq_list: {}'.format(fastq_list))
        sample_fastq_dict[sample] = sorted(fastq_list)    
    return sample_fastq_dict

def get_lane_list(fastq_list):
    lane_set = set()
    p = re.compile('\S+_(L\d+)_\S+')
    for fastq in fastq_list:
        m = p.match(fastq)
        if m:
            lane_set.add(m.group(1))
    return sorted(list(lane_set))

def get_forward_reverse_fastq_dict(fastq_list, lane):
    forward_reverse_fastq_dict = dict()
    for fastq in fastq_list:
        if lane in fastq:
            if '_R1_' in fastq:
                if 'forward_fastq' in forward_reverse_fastq_dict:
                    print('more than one fw fq: {}'.format(fastq))
                    print('\tin rg!:')
                    pprint.pprint(forward_reverse_fastq_dict)
                    sys.exit(1)
                forward_reverse_fastq_dict['forward_fastq'] = fastq
            if '_R2_' in fastq:
                if 'reverse_fastq' in forward_reverse_fastq_dict:
                    print('more than one rev fq: {}'.format(fastq))
                    print('\tin rg!:')
                    pprint.pprint(forward_reverse_fastq_dict)
                    sys.exit(1)
                forward_reverse_fastq_dict['reverse_fastq'] = fastq
    return forward_reverse_fastq_dict

def get_sample_readgroup_dict(sample_fastq_dict, sample_data):
    sample_readgroup_dict = dict()
    for sample in sorted(sample_fastq_dict.keys()):
        print('sample: {}'.format(sample))
        sample_readgroup_dict[sample] = list()
        fastq_list = sorted(sample_fastq_dict[sample])
        if len(fastq_list) % 2 != 0:
            print('only handles PE data')
            sys.exit(1)
        readgroup_count = int(len(fastq_list)/2)
        for i in range(readgroup_count):
            r1_index = i * 2
            r2_index = (i * 2) + 1
            r1 = fastq_list[r1_index]
            r2 = fastq_list[r2_index]
            forward_reverse_fastq_dict = dict()
            forward_reverse_fastq_dict['forward_fastq'] = r1
            forward_reverse_fastq_dict['reverse_fastq'] = r2
            sample_readgroup_dict[sample].append(forward_reverse_fastq_dict)
    print('sample_readgroup_dict:')
    pprint.pprint(sample_readgroup_dict)
    return sample_readgroup_dict

def get_deref_readgroup(sample_data, design_csv):
    project_readgroup = sample_data['READGROUP']
    sample_list = get_sample_list(sample_data, design_csv)
    proj_rg_meta = dict()
    for sample in sample_list:
        proj_rg_meta[sample] = dict()
    for rg_item in project_readgroup:
        if isinstance(project_readgroup[rg_item], dict):
            csv_file = project_readgroup[rg_item]['csv']['file']
            csv_column = project_readgroup[rg_item]['csv']['column']
            assert(os.path.basename(design_csv) == csv_file)
            csv_df = pd.read_csv(design_csv)
            rg_value_list = list(csv_df[csv_column])
            assert(len(sample_list) == len(rg_value_list))
            for sample, rg_value in zip(sample_list, rg_value_list):
                proj_rg_meta[sample][rg_item] = rg_value.replace(' ','').replace('@','_').replace(',','_').replace(';','_')
        else:
            for sample in sample_list:
                proj_rg_meta[sample][rg_item] = project_readgroup[rg_item].replace(' ','').replace('@','_').replace(',','_').replace(';','_')
    return proj_rg_meta


'''
https://en.wikipedia.org/wiki/FASTQ_format#Illumina_sequence_identifiers
https://github.com/broadinstitute/picard/blob/master/testdata/picard/fingerprint/NA12891.over.fingerprints.shifted.for.crams.r1.sam
@A01016:49:HC5JTDRXX:2:2101:1524:1000 1:N:0:GACCTGAA+TTGGTGAG
'''
def get_fastq_readgroup(fastq_path, sample):
    readgroup_meta = dict()
    if fastq_path.endswith('.gz'):
        with gzip.open(fastq_path, 'rb') as f_open:
            fastq_line = str(f_open.readline(), 'utf-8').strip('\n')
            #print('fastq_line: {}'.format(fastq_line))
    elif fastq_path.endswith('.fq') or fastq_path.endswith('fastq'):
        #todo
        sys.exit(1)
    fastq_split = fastq_line.split(' ')
    if fastq_split[0].count(':') == 6:
        UNIQUE_INSTRUMENT_NAME = 0
        RUN_ID = 1
        FLOWCELL_ID = 2
        FLOWCELL_LANE = 3
        TILE_NUMBER = 4
        X_COORD = 5
        Y_COORD = 6
        fastq_flowcell = fastq_split[0].split(':')

        if fastq_split[1].count(':') == 3:
            PAIR_MEMBER = 0
            FILTERED = 1
            CONTROL_BITS = 2
            INDEX_SEQ = 3
            fastq_index = fastq_split[1].split(':')

        readgroup_meta['BC'] = fastq_index[INDEX_SEQ].replace('+', '-')
        readgroup_meta['ID'] = fastq_flowcell[FLOWCELL_ID].lstrip('@')[0:5] + '.' + fastq_flowcell[FLOWCELL_LANE]
        readgroup_meta['PU'] = fastq_flowcell[FLOWCELL_ID].lstrip('@') + '.' + fastq_flowcell[FLOWCELL_LANE] + '.' + fastq_index[INDEX_SEQ].replace('+', '-')
        readgroup_meta['LB'] = sample + '_' + fastq_index[INDEX_SEQ].replace('+', '-')
    return readgroup_meta


def get_sample_readgroup(sample_readgroup_dict):
    print('get_sample_readgroup()')
    print('sample_readgroup_dict:')
    pprint.pprint(sample_readgroup_dict)
    sample_readgroup = dict()
    for sample in sample_readgroup_dict:
        print('\tsample:')
        pprint.pprint(sample)
        sample_readgroup[sample] = list()
        for readgroup in sample_readgroup_dict[sample]:
            print('\t\treadgroup:')
            pprint.pprint(readgroup)
            rg = dict()
            rg['readgroup_meta'] = get_fastq_readgroup(readgroup['forward_fastq'], sample)
            rg['readgroup_meta']['SM'] = sample
            rg.update(readgroup)
            sample_readgroup[sample].append(rg)
    return sample_readgroup


def get_rg_meta(sample_readgroup_dict, sample_data, design_csv):
    dereferenced_project_readgroup = get_deref_readgroup(sample_data, design_csv)
    sample_readgroup = get_sample_readgroup(sample_readgroup_dict)
    for sample in sorted(list(sample_readgroup.keys())):
        for rg in sample_readgroup[sample]:
            rg['readgroup_meta'].update(dereferenced_project_readgroup[sample])
    return sample_readgroup


def create_fastq_readgroups(sample_data, fastq_dir, design_csv):
    sample_list = get_sample_list(sample_data, design_csv)
    print('sample_list:')
    pprint.pprint(sample_list)
    sample_fastq_dict = get_sample_fastq_dict(sample_list, fastq_dir)
    print('sample_fastq_dict')
    pprint.pprint(sample_fastq_dict)
    sample_readgroup_dict = get_sample_readgroup_dict(sample_fastq_dict, sample_data)
    print('sample_readgroup_dict')
    pprint.pprint(sample_readgroup_dict)
    sample_readgroup_meta_dict = get_rg_meta(sample_readgroup_dict, sample_data, design_csv)
    return sample_readgroup_meta_dict


def modify_fastq_paths(fastq_readgroups, fastq_dir_name):
    mod_fastq_readgroups = list()
    for rg in fastq_readgroups:
        new_rg = dict()
        new_rg['readgroup_meta'] = rg['readgroup_meta']
        forward_fastq_name = os.path.basename(rg['forward_fastq'])
        reverse_fastq_name = os.path.basename(rg['reverse_fastq'])
        forward_fastq_path = os.path.join(fastq_dir_name, forward_fastq_name)
        reverse_fastq_path = os.path.join(fastq_dir_name, reverse_fastq_name)
        new_rg['forward_fastq'] = {'class':'File','location': forward_fastq_path}
        new_rg['reverse_fastq'] = {'class':'File','location': reverse_fastq_path}
        mod_fastq_readgroups.append(new_rg)
    return mod_fastq_readgroups


def output_jobs(static_data, fastq_readgroups, fastq_dir_name, yaml):
    yaml.indent(sequence=4, offset=2)
    for sample in fastq_readgroups:
        sample_dict = copy.deepcopy(static_data)
        mod_fastq_readgroups = modify_fastq_paths(fastq_readgroups[sample], fastq_dir_name)
        sample_dict['pe_fastq_readgroup_list'] = mod_fastq_readgroups
        sample_dict['run_uuid'] = str(uuid.uuid4())
        with open(sample+'.yml', 'w') as f_open:
            documents = yaml.dump(sample_dict, f_open)
    return


def main():
    parser = argparse.ArgumentParser(description='create star alignment jobs')
    parser.add_argument('-s', '--sample_yaml',
                        required=True)
    parser.add_argument('-f', '--fastq_dir',
                        required=True)
    parser.add_argument('-n', '--fastq_dir_name',
                        required=True)
    parser.add_argument('-d', '--design_csv',
                        required=True)
    parser.add_argument('-c', '--static_yaml',
                        required=True)
    args = parser.parse_args()
    sample_yaml = args.sample_yaml
    fastq_dir = args.fastq_dir
    fastq_dir_name = args.fastq_dir_name
    design_csv = args.design_csv
    static_yaml = args.static_yaml

    yaml = ruamel.yaml.YAML()
    with open(sample_yaml, 'r') as f_open:
        sample_data = yaml.load(f_open)
    with open(static_yaml, 'r') as f_open:
        static_data = yaml.load(f_open)

    fastq_readgroups = create_fastq_readgroups(sample_data, fastq_dir, design_csv)
    output_jobs(static_data, fastq_readgroups, fastq_dir_name, yaml)
    return


if __name__ == '__main__':
    main()
