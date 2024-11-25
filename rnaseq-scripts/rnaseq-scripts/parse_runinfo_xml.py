#!/usr/bin/env python3

'''
'''

import argparse
import os
import xml.etree.ElementTree as ET

def get_runiditem(runinfoxml, runidkey):
    tree = ET.parse(runinfoxml)
    root = tree.getroot()
    run = root.find('Run')
    runiditem = run.find(runidkey)
    runidval = runiditem.text
    return runidval

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-x', '--runinfoxml',
                        required=True)
    parser.add_argument('-r', '--runidkey',
                        required=True)
    args = parser.parse_args()
    runinfoxml = args.runinfoxml
    runidkey = args.runidkey

    runidval = get_runiditem(runinfoxml, runidkey)
    print(runidval)
    return

if __name__ == '__main__':
    main()
