#!/usr/bin/env python

import argparse
import os
import pprint

def get_contig_set(fastadict):
    contig_set = set()
    with open(fastadict, 'r') as f_open:
        for line in f_open:
            if line.startswith('@SQ'):
                line_split = line.split('\t')
                seq_name = line_split[1].split(':')[1]
                contig_set.add(seq_name)
    return contig_set

def write_pruned_bed(bed, contig_set):
    print('')
    print('write_pruned_bed()')
    in_bed = os.path.basename(bed)
    in_bed_name, in_bed_ext = os.path.splitext(in_bed)
    out_bed = in_bed_name + '.prune' + in_bed_ext
    with open(out_bed, 'w') as f_write:
        with open(bed, 'r') as f_read:
            for line in f_read:
                line_split = line.split('\t')
                seq_name = line_split[0]
                if seq_name in contig_set:
                    print(f'seq_name: {seq_name}')
                    f_write.write(line)
    return out_bed

def main():
    parser = argparse.ArgumentParser('convert readgroups to json')

    parser.add_argument('-f', '--fastadict',
                        required = True
    )
    parser.add_argument('-b', '--bed',
                        required = True
    )

    args = parser.parse_args()
    fastadict = args.fastadict
    bed = args.bed

    contig_set = get_contig_set(fastadict)
    print('congig_set:')
    pprint.pprint(contig_set)
    out_bed = write_pruned_bed(bed, contig_set)
    return

if __name__ == '__main__':
    main()
