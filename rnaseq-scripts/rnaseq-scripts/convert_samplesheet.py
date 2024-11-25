#!/usr/bin/env python3

'''
'''

import argparse
import os

def get_ss_idx(samplesheet):
    ss_idx = dict()
    with open(samplesheet, 'r') as f_open:
        for line in f_open:
            if line.startswith('Lane,'):
                line = line.strip()
                line_split = line.split(',')
                ss_idx['Lane'] = line_split.index('Lane')
                ss_idx['Sample_ID'] = line_split.index('Sample_ID')
                ss_idx['index'] = line_split.index('index')
                ss_idx['index2'] = line_split.index('index2')
                break
            elif line.startswith('Sample_ID,'):
                print(f'line: {line}')
                line = line.strip()
                line_split = line.split(',')
                print(f'line_split: {line_split}')
                ss_idx['Sample_ID'] = line_split.index('Sample_ID')
                ss_idx['Index'] = line_split.index('Index')
                ss_idx['Index2'] = line_split.index('Index2')
                break
    return ss_idx    

def get_ss_vals(samplesheet, ss_idx, lanecount):
    ss_vals = dict()
    in_data = False
    if 'Lane' in ss_idx:
        with open(samplesheet, 'r') as f_open:
            for line in f_open:
                if in_data:
                    line_split = line.split(',')
                    lane = line_split[ss_idx['Lane']]
                    sample_id = line_split[ss_idx['Sample_ID']]
                    index1 = line_split[ss_idx['index']]
                    index2 = line_split[ss_idx['index2']]
                    if not lane in ss_vals:
                        ss_vals[lane] = dict()
                    ss_vals[lane][sample_id] = index1 + '\t' + index2
                if line.startswith('Lane,'):
                    in_data = True
    else:
        with open(samplesheet, 'r') as f_open:
            for line in f_open:
                if in_data:
                    if ',' not in line:
                        break
                    line = line.strip()
                    line_split = line.split(',')
                    sample_id = line_split[ss_idx['Sample_ID']]
                    index1 = line_split[ss_idx['Index']]
                    index2 = line_split[ss_idx['Index2']]
                    for lane in range(1, int(lanecount)+1):
                        print(f'LANE: {lane}')
                        if not str(lane) in ss_vals:
                            ss_vals[str(lane)] = dict()
                        print()
                        print(f'ss_vals: {ss_vals}')
                        print(f'sample_id: {sample_id}')
                        print(f'index1: {index1}')
                        print(f'index2: {index2}')
                        ss_vals[str(lane)][sample_id] = index1 + '\t' + index2
                if line.startswith('Sample_ID,'):
                    in_data = True
    return ss_vals

def write_vals(ss_vals):
    for lane in sorted(list(ss_vals)):
        barcode_f = f'Barcode_file_L{lane.zfill(3)}.txt'
        library_f = f'Library_file_L{lane.zfill(3)}.txt'
        print(f'lane: {lane} \t ss_vals[lane]: {ss_vals[lane]}')
        with open(barcode_f, 'w') as barcode_o:
            barcode_o.write('barcode_name\tlibrary_name\tbarcode_sequence_1\tbarcode_sequence_2\n')
            for i,sample_id in enumerate(ss_vals[lane], 1):
                print(f'\ti: {i} \t sample_id: {sample_id}')
                print(f'\t\tss_vals[lane][sample_id]: {ss_vals[lane][sample_id]}')
                barcode_o.write(f'Adapter-{i}\t{sample_id}\t{ss_vals[lane][sample_id]}\n')
        with open(library_f, 'w') as library_o:
            library_o.write('OUTPUT\tSAMPLE_ALIAS\tLIBRARY_NAME\tBARCODE_1\tBARCODE_2\n')
            for sample_id in ss_vals[lane]:
                bam_path = f'{sample_id}_L{lane.zfill(3)}.bam'
                library_o.write(f'{bam_path}\t{sample_id}\t{sample_id}\t{ss_vals[lane][sample_id]}\n')
            unmatched_bam = f'Unmatched_L{lane.zfill(3)}.bam'
            library_o.write(f'{unmatched_bam}\tUnmatched\tUnmatched\tN\tN\n')
    return

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', '--samplesheet',
                        required=True)
    parser.add_argument('-l', '--lanecount',
                        required=False)
    args = parser.parse_args()
    samplesheet = args.samplesheet
    lanecount = args.lanecount

    ss_idx = get_ss_idx(samplesheet)
    ss_vals = get_ss_vals(samplesheet, ss_idx, lanecount)
    write_vals(ss_vals)
    return

if __name__ == '__main__':
    main()
