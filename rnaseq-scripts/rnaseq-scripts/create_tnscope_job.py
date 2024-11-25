#!/usr/bin/env python3

'''
'''

import argparse
import os
import sys

import pysam
import ruamel.yaml

def write_job(job):
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)
    job_base, _ = os.path.splitext(os.path.basename(job['output']))
    job_path = job_base + '.yml'
    with open(job_path, 'w') as f_open:
        documents = yaml.dump(job, f_open)
    return job_path

def get_sample(bam):
    samfile = pysam.AlignmentFile(bam, 'rb', check_sq=False)
    samfile_header = samfile.header
    readgroup_dict_list = samfile_header['RG']
    if len(readgroup_dict_list) > 1:
        print('more than 1 readgroup')
        sys.exit(1)
    readgroup = readgroup_dict_list[0]
    sample = readgroup['SM']
    return sample

def create_job(bam, sentieon, reference):
    sample = get_sample(bam)
    job = dict()
    bai = bam.rstrip('.bam')+'.bai'
    vcf = os.path.basename(bam).rstrip('.bam')+'.vcf'
    bai_obj = {'class': 'File', 'path': bai}
    job['tumor_bam'] = {'class': 'File', 'path': bam,
                        'secondaryFiles': [bai_obj]}
    job['sentieon_license'] = sentieon
    job['reference'] = {'class': 'File', 'path': reference}
    job['output'] = vcf
    job['tumor_sample'] = sample
    return job

def main():
    parser = argparse.ArgumentParser(description='create tnscope jobs')

    parser.add_argument('--bam',
                        required=True)
    parser.add_argument('--sentieon',
                        required=True)
    parser.add_argument('--reference',
                        required=True)
    args = parser.parse_args()
    
    bam = args.bam
    sentieon = args.sentieon
    reference = args.reference

    job = create_job(bam, sentieon, reference)
    job_path = write_job(job)
    return

if __name__ == '__main__':
    main()
