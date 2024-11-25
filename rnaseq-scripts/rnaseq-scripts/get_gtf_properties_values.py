#!/usr/bin/env python

'''
example:

python get_gtf_properties.py -i <file.gtf>
'''

import argparse

def get_props(inputgtf):
    prop_dict = dict()
    with open(inputgtf ,'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            prop_list = line.split('\t')[-1].split(';')
            for prop in prop_list:
                prop = prop.strip()
                if len(prop) == 0:
                    continue
                prop_split = prop.split(' ')
                prop_key = prop_split[0]
                if not prop_key in prop_dict:
                    prop_dict[prop_key] = set()
                prop_dict[prop_key].add(prop_split[1])
    for prop_key in sorted(list(prop_dict.keys())):
        with open(inputgtf+'.'+prop_key, 'w') as f:
            for prop in sorted(list(prop_dict[prop_key])):
                f.write(prop+'\n')
    return

def main():
    parser = argparse.ArgumentParser(description='get property keys')
    parser.add_argument('-i', '--inputgtf',
                        required=True)
    args = parser.parse_args()
    get_props(args.inputgtf)
    return

if __name__ == '__main__':
    main()
