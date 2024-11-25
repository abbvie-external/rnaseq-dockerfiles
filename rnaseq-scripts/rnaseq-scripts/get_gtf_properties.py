#!/usr/bin/env python

'''
example:

python get_gtf_properties.py -i <file.gtf>
'''

import argparse

def get_props(inputgtf):
    prop_set = set()
    with open(inputgtf ,'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            prop_list = line.split('\t')[-1].split(';')
            for prop in prop_list:
                prop_key = prop.strip().split(' ')[0]
                prop_set.add(prop_key)
    with open(inputgtf+'.props', 'w') as f:
        for prop in sorted(list(prop_set)):
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
