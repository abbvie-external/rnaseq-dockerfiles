#!/usr/bin/env python3

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='refseq cds to tx2gene tsv')
    parser.add_argument('-c', '--cds',
                        required=True)
    args = parser.parse_args()
    cds = Path(args.cds)

    tx_gene_dict = dict()
    with open(cds, 'r') as f_read:
        for line in f_read:
            if line.startswith('>'):
                transcript = line.split()[0].removeprefix('>').strip()
                if '|' in transcript:
                    gene = transcript.split('|')[1].strip()
                    tx_gene_dict[transcript] = gene

    outfile = Path(cds.stem+'.tx2gene.tsv')
    with open(outfile, 'w') as f:
        f.write('transcript\tgene\n')
        for tx in sorted(tx_gene_dict.keys()):
            f.write(tx+'\t'+tx_gene_dict[tx]+'\n')
    return

if __name__ == '__main__':
    main()
