#!/usr/bin/env python3

'''
'''

import argparse
import os
import sys
import xml.etree.ElementTree as ET

def get_runiditem(xmlinput, xmltype, xmlkey):
    tree = ET.parse(xmlinput)
    root = tree.getroot()
    if xmltype == 'runinfo':
        items = root.find('Run')
    elif xmltype == 'runparameters':
        items = root.find('Setup')
    else:
        print(f'unknown xml type: {xmltype}\n')
        sys.exit(1)
    xmlitem = items.find(xmlkey)
    keyval = xmlitem.text
    return keyval

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-x', '--xmlinput',
                        required=True)
    parser.add_argument('-t', '--xmltype',
                        required=True,
                        choices=['runinfo', 'runparameters'])
    parser.add_argument('-k', '--xmlkey',
                        required=True)
    args = parser.parse_args()
    xmlinput = args.xmlinput
    xmltype = args.xmltype
    xmlkey = args.xmlkey

    keyval = get_runiditem(xmlinput, xmltype, xmlkey)
    print(keyval)
    return

if __name__ == '__main__':
    main()
