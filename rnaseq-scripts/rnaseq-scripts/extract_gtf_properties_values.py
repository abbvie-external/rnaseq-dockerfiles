#!/usr/bin/env python3

'''
example:

python extract_gtf_properties.py -i <file.gtf> -k "gene_type:miRNA" -k "transcript_type:protein_coding"
'''

import argparse
import os

def is_matched(prop, key_value_dict):
    prop_split = prop.split(' ')
    prop_key = prop_split[0]
    prop_value = prop_split[1].strip("'").strip('"')
    if prop_key in key_value_dict:
        return prop_value in key_value_dict[prop_key]
    return False

def get_props(inputgtf, modname, key_value_dict):
    prop_dict = dict()
    inputgtfname = os.path.basename(inputgtf)
    inputname, input_ext = os.path.splitext(inputgtfname)
    gtf_out = inputname + '.' + modname + input_ext
    with open(gtf_out, 'w') as f_write:
        with open(inputgtf ,'r') as f_read:
            for line in f_read:
                if line.startswith('#'):
                    f_write.write(line)
                    continue
                prop_list = line.split('\t')[-1].split(';')
                for prop in prop_list:
                    prop = prop.strip()
                    if len(prop) == 0:
                        continue
                    matched = is_matched(prop, key_value_dict)
                    if matched:
                        f_write.write(line)
                        break
    return

def get_key_value_dict(keyvalues):
    key_value_dict = dict()
    for keyvalue in keyvalues:
        keyvalue_split = keyvalue.split(':')
        key = keyvalue_split[0]
        if key not in key_value_dict:
            key_value_dict[key] = set()
        key_value_dict[key].add(keyvalue_split[1])
    return key_value_dict

def main():
    parser = argparse.ArgumentParser(description='extract gtf with property key values')
    parser.add_argument('-i', '--input',
                        required=True)
    parser.add_argument('-m', '--modname',
                        required=True)
    parser.add_argument('-k', '--keyvalues',
                        action='append',
                        required=True)
    args = parser.parse_args()
    key_value_dict = get_key_value_dict(args.keyvalues)
    get_props(args.input, args.modname, key_value_dict)
    return

if __name__ == '__main__':
    main()
