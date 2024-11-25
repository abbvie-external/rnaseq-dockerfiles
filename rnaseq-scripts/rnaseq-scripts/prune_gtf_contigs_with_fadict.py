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

def write_pruned_gtf(gtf, contig_set):
    print('')
    print('write_pruned_gtf()')
    in_gtf = os.path.basename(gtf)
    in_gtf_name, in_gtf_ext = os.path.splitext(in_gtf)
    out_gtf = in_gtf
    with open(out_gtf, 'w') as f_write:
        with open(gtf, 'r') as f_read:
            for line in f_read:
                if line.startswith('#'):
                    f_write.write(line)
                    continue
                line_split = line.split('\t')
                seq_name = line_split[0]
                if seq_name in contig_set:
                    f_write.write(line)
    return out_gtf

def main():
    parser = argparse.ArgumentParser("prune a gtf's contigs")

    parser.add_argument('-f', '--fastadict',
                        required = True
    )
    parser.add_argument('-g', '--gtf',
                        required = True
    )

    args = parser.parse_args()
    fastadict = args.fastadict
    gtf = args.gtf

    contig_set = get_contig_set(fastadict)
    print('congig_set:')
    pprint.pprint(contig_set)
    out_gtf = write_pruned_gtf(gtf, contig_set)
    return

if __name__ == '__main__':
    main()
