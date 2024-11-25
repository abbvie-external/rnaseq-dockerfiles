#!/usr/bin/env python3

import argparse
import os

def fix_bed(bed, output):
    with open(bed, 'r') as f_read:
        with open(output, 'w') as f_write:
            for line in f_read:
                line_split = line.strip().split()
                new_line = line_split[:3]
                if len(line_split) > 3:
                    new_name = line_split[0]+'.'+line_split[1]+'.'+line_split[2]+'.'+line_split[4]
                else:
                    new_name = line_split[0]+'.'+line_split[1]+'.'+line_split[2]+'.unknown'
                new_line.append(new_name)
                new_line.append('0')
                new_line = '\t'.join(new_line)
                f_write.write(new_line+'\n')
    return

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-b', '--bed',
                        required=True)
    parser.add_argument('-o', '--output',
                        required=True)
    args = parser.parse_args()
    bed = args.bed
    output = args.output

    fix_bed(bed, output)
    return

if __name__ == '__main__':
    main()
