import argparse
import glob
import os
import sys

from gzip import open as gzopen
from Bio.SeqIO.QualityIO import FastqGeneralIterator

def reheader(fwd, umi, rev):
    fwdhandle = gzopen(fwd, "rt")
    revhandle = gzopen(rev, "rt")
    umihandle = gzopen(umi, "rt")

    fwd_iter = FastqGeneralIterator(fwdhandle)
    rev_iter = FastqGeneralIterator(revhandle)
    umi_iter = FastqGeneralIterator(umihandle)

    fwd_out = os.path.basename(fwd)
    rev_out = os.path.basename(umi)
    outhandle1 = gzopen(fwd_out, "wt")
    outhandle2 = gzopen(rev_out, "wt")

    for (f_id, f_seq, f_q), (_,umi_seq,_), (r_id, r_seq, r_q) in zip(fwd_iter,umi_iter,rev_iter):
        outhandle1.write("@%s_%s\n%s\n+\n%s\n" % (f_id.split(" ")[0], umi_seq , f_seq, f_q))
        outhandle2.write("@%s_%s\n%s\n+\n%s\n" % (r_id.split(" ")[0], umi_seq , r_seq, r_q))

    outhandle1.close()
    outhandle2.close()
    fwdhandle.close()
    revhandle.close()
    umihandle.close()

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--forward_fastq',
                        required=True)
    parser.add_argument('-u', '--umi_fastq',
                        required=True)
    parser.add_argument('-r', '--reverse_fastq',
                        required=True)
    args = parser.parse_args()
    fwd = args.forward_fastq
    rev = args.reverse_fastq
    umi = args.umi_fastq

    reheader(fwd, umi, rev)
    return

if __name__ == '__main__':
    main()
