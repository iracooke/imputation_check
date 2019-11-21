#!/usr/bin/env python3

import argparse
import sys
import vcf
import collections
import pdb

parser = argparse.ArgumentParser(description='Compare pruned and imputed genotypes')

parser.add_argument('impvcf',metavar='imputed',type=argparse.FileType('r'),help='Imputed VCF File',default=sys.stdin)

parser.add_argument('pruned',metavar='pruned',type=argparse.FileType('r'),help='Pruned genotypes in text format',default=sys.stdin)

parser.add_argument('-o','--output',metavar='FILE',nargs='?',type=argparse.FileType('w'),help='Comparison output',default=sys.stdout)

args  = parser.parse_args()

vcf_reader = vcf.Reader(args.impvcf)

pruned_fields = args.pruned.readline().strip().split('\t')

#pdb.set_trace()

p_gt_template = collections.namedtuple('prunedgenotype',pruned_fields)

next_pruned = p_gt_template(*args.pruned.readline().strip().split('\t'))

args.output.write("record\tIMP_GT\tREF\tALT\n")

record_num = 1
for record in vcf_reader:

	if record_num == int(next_pruned.record):
		args.output.write(next_pruned.record+"\t"+record.samples[int(next_pruned.sample_index)].data.GT+"\t"+str(record.REF)+"\t"+str(record.ALT)+"\n")
		next_pruned = p_gt_template(*args.pruned.readline().strip().split('\t'))

	record_num+=1


