#!/usr/bin/env python3

import argparse
import copy
import os

import ruamel.yaml

def mod_ref(reference_value):
    file_name = os.path.basename(reference_value)
    file_split = file_name.split('.')
    out_name = file_split[0]+'_'+file_split[1]+'.fa'
    return out_name

def mod_refn(reference_value):
    file_name = os.path.basename(reference_value)
    file_split = file_name.split('.')
    refn = file_split[1]
    return refn

def create_jobs(commands, template_data, yaml):
    command_list = list()
    with open(commands, 'r') as f_open:
        for line in f_open:
            line_split = line.strip().split()
            coverage_idx = line_split.index('-c')
            coverage_value = int(line_split[coverage_idx+1])
            reference_idx = line_split.index('-r')
            reference_value = line_split[reference_idx+1]
            error_idx = line_split.index('-E')
            error_value = float(line_split[error_idx+1])
            sim_idx = line_split.index('-o')
            sim_value = line_split[sim_idx+1]
            run_dict = copy.deepcopy(template_data)
            if '_' in reference_value or reference_value.count('.') == 2:
                ref = mod_ref(reference_value)
                refn = mod_refn(reference_value)
            else:
                ref = os.path.basename(reference_value)
                refn = False
            if ' -v ' in line:
                vcf_idx = line_split.index('-v')
                vcf_value = line_split[vcf_idx+1]
                vcf_basename = os.path.basename(vcf_value)
                vcf_dir = os.path.dirname(run_dict['target_bed']['location'])
                vcf = os.path.join(vcf_dir, vcf_basename)
                print(f'vcf: {vcf}')
                run_dict['vcf_file'] = {'class': 'File', 'location': vcf}
            sim = sim_value.split('_')[0]
            err = error_value
            cov = coverage_value
            run_dict['coverage'] = cov
            run_dict['error_rate'] = err
            run_dict['output_prefix'] = sim_value
            run_dict['reference']['location'] = run_dict['reference']['location'].replace('null', ref)
            run_dict['reference']['secondaryFile'][0]['location'] = run_dict['reference']['secondaryFile'][0]['location'].replace('null', ref+'.fai')
            if refn: 
                run_dict['target_bed']['location'] = run_dict['target_bed']['location'].replace('.bed', '_'+refn+'.bed')
            with open(sim+'.yml', 'w') as f_open:
                document = yaml.dump(run_dict, f_open)
    return

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-t', '--template_yaml',
                        required=True)
    parser.add_argument('-c', '--commands',
                        required=True)
    args = parser.parse_args()
    commands = args.commands
    template_yaml = args.template_yaml

    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)
    with open(template_yaml, 'r') as f_open:
        template_data = yaml.load(f_open)

    create_jobs(commands, template_data, yaml)
    return

if __name__ == '__main__':
    main()
