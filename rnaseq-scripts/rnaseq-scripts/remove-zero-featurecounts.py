import argparse
from pathlib import Path

def remove_zero_counts(tsvinput):
    tsvoutput = tsvinput.stem + '.nonzero.tsv'
    with open(tsvoutput, 'w') as f_output:
        with open(tsvinput, 'r') as f_input:
            for line in f_input:
                line_split = line.strip().split('\t')
                value_list = line_split[1:]
                if all(x == '0' for x in value_list):
                    continue
                else:
                    f_output.write(line)
    return

def main():
    parser = argparse.ArgumentParser(description='remove zero counts')
    parser.add_argument('-i', '--tsvinput',
                        required=True)
    args = parser.parse_args()
    tsvinput = Path(args.tsvinput)

    remove_zero_counts(tsvinput)
    return

if __name__ == '__main__':
    main()
