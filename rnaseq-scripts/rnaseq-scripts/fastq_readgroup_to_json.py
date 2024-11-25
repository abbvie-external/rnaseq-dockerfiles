#!/usr/bin/env python

import argparse
import gzip
import json
import os
import sys

'''
https://en.wikipedia.org/wiki/FASTQ_format#Illumina_sequence_identifiers
'''

def extract_readgroup_json(fastq_path, sample):
    readgroup_meta = dict()
    if fastq_path.endswith('.gz'):
        with gzip.open(fastq_path, 'rb') as f_open:
            fastq_line = str(f_open.readline(), 'utf-8').strip('\n')
            #print('fastq_line: {}'.format(fastq_line))
    elif fastq_path.endswith('.fq') or fastq_path.endswith('fastq'):
        # todo
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
        readgroup_meta['SM'] = sample
    elif fastq_split[0].count(':') == 7:
        UNIQUE_INSTRUMENT_NAME = 0
        RUN_ID = 1
        FLOWCELL_ID = 2
        FLOWCELL_LANE = 3
        TILE_NUMBER = 4
        X_COORD = 5
        Y_COORD = 6
        UMI = 7
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
        readgroup_meta['SM'] = sample
    else:
        print(f'need to handle this case fastq_split[0].count(":"): {fastq_split[0].count(":")}')
        sys.exit(1)

    readgroup_json_file = readgroup_meta['ID']+'.json'
    with open(readgroup_json_file, 'w') as f:
        json.dump(readgroup_meta, f, ensure_ascii=False)
    return

def main():
    parser = argparse.ArgumentParser('convert readgroups to json')

    parser.add_argument('-f', '--fastq_path',
                        required = True
    )
    parser.add_argument('-s', '--sample',
                        required = True
    )

    args = parser.parse_args()
    fastq_path = args.fastq_path
    sample = args.sample

    extract_readgroup_json(fastq_path, sample)
    return

if __name__ == '__main__':
    main()
