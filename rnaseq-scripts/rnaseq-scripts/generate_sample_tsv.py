#!/usr/bin/env python

'''
example

python3 ~/rnaseq-scripts/generate_sample_tsv.py -c SampleID -d $(pwd) -t test.tsv -s _ -k 4 -r _R1.
'''


import argparse
import glob
import os

def get_fastq_list(fastqdir):
    sample_dirs = glob.glob(os.path.join(fastqdir, '*.fastq.gz'))
    return sorted(list(sample_dirs))

def get_sample_list(fastq_list, separator, keptsplits, readkey):
    fastq_names = [os.path.basename(x) for x in fastq_list]
    sample_set = set()
    for fastq in fastq_names:
        if readkey in fastq:
            fastq_split = fastq.split(separator)
            sample_name = separator.join(fastq_split[:keptsplits])
            sample_set.add(sample_name)
    return sorted(list(sample_set))

def write_samples_tsv(columnid, sample_list, tsvname):
    with open(tsvname, 'w') as f_open:
        f_open.write(columnid + '\n')
        for sample in sample_list:
            f_open.write(sample + '\n')
    return tsvname

def main():
    parser = argparse.ArgumentParser(description='merge featurecount reports')
    parser.add_argument('-c', '--columnid',
                        required=True)
    parser.add_argument('-d', '--fastqdir',
                        required=True)
    parser.add_argument('-k', '--keptsplits',
                        required=True)
    parser.add_argument('-r', '--readkey',
                        required=True)
    parser.add_argument('-s', '--separator',
                        required=True)
    parser.add_argument('-t', '--tsvname',
                        required=True)
    args = parser.parse_args()
    columnid = args.columnid
    fastqdir = args.fastqdir
    readkey = args.readkey
    tsvname = args.tsvname
    separator = args.separator
    keptsplits = int(args.keptsplits)

    fastq_list = get_fastq_list(fastqdir)
    sample_list = get_sample_list(fastq_list, separator, keptsplits, readkey)
    tsv_path = write_samples_tsv(columnid, sample_list, tsvname)
    # sample_dict = get_sample_dict(fastq_list)
    # yml_path = write_samples_yml(projectname, projectdir, sample_dict)
    return

if __name__ == '__main__':
    main()
