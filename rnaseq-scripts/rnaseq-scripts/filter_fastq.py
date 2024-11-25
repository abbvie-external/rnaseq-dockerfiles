import argparse
import glob
import os
import sys
from pathlib import Path

from gzip import open as gzopen
from Bio import SeqIO

def get_freads(flist: Path) -> set:
    freads = set()
    with flist.open(mode='r') as f_read:
        for line in f_read:
            freads.add(line.strip())
    return freads

def filter_fastq(fwd: Path, rev: Path, flist:Path) -> None:
    freads = get_freads(flist)
    fwd_out = Path(Path(fwd.stem).stem + '.filter' + Path(fwd.stem).suffix)
    rev_out = Path(Path(rev.stem).stem + '.filter' + Path(rev.stem).suffix)
    with open(fwd_out, 'w') as f1_write:
        with gzopen(fwd, "rt") as f1_read:
            for record in SeqIO.parse(f1_read, "fastq"):
                if record.id in freads:
                    SeqIO.write(record, f1_write, "fastq")
    with open(rev_out, 'w') as f2_write:
        with gzopen(fwd, "rt") as f2_read:
            for record in SeqIO.parse(f2_read, "fastq"):
                if record.id in freads:
                    SeqIO.write(record, f2_write, "fastq")
    return

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--forward_fastq',
                        required=True)
    parser.add_argument('-r', '--reverse_fastq',
                        required=True)
    parser.add_argument('-l', '--filter_list',
                        required=True)
    args = parser.parse_args()
    fwd = Path(args.forward_fastq)
    rev = Path(args.reverse_fastq)
    flist = Path(args.filter_list)

    filter_fastq(fwd, rev, flist)
    return

if __name__ == '__main__':
    main()
