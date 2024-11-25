#!/usr/bin/env python


import argparse
import json
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Convert a column in a TSV file to a JSON list')
    parser.add_argument('-i', '--input_file',
                        help='Input TSV file',
                        required=True)
    parser.add_argument('-c', '--column',
                        help='Column to convert to JSON list',
                        required=True)

    args = parser.parse_args()
    input_file = Path(args.input_file)
    column = args.column
    list_items = pd.read_csv(input_file, sep='\t')[column].tolist()
    out_list = [x for x in list_items if not pd.isna(x)]
    output_file = input_file.stem + '.json'
    with open(output_file, 'w') as f:
        json.dump(out_list, f)
    return

if __name__ == '__main__':
    main()
