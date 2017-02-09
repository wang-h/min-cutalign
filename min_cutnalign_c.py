# -*- coding: utf-8 -*-
# 　Copyright 2013 by Hao Wang  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from collections import defaultdict
from copy import deepcopy
import math,time 
import _partitionize
__min__=10e-7
import logging
logging.basicConfig( level=logging.INFO)

def read_tt(tt_file, reverse):
	tt=defaultdict(dict)
	for line in tt_file:
		if reverse:
			tw, sw, _, scores, _ = line.rstrip("\n").split("\t")
		else:
			sw, tw, _, scores, _ = line.rstrip("\n").split("\t")
		pst, pts    = map(float, scores.split()) 
		tt[sw][tw]  = math.sqrt(pst*pts) 
	return tt
def read_tt_e2f(e2f_file, f2e_file, reverse):
	tt=defaultdict(dict)
	for line in e2f_file:
		sw, tw, score  = line.rstrip("\n").split() 
		tt[sw][tw]  = float(score)
	for line in f2e_file:
		tw, sw, score  = line.rstrip("\n").split() 
		tt[sw][tw]  = math.sqrt(tt[sw][tw]*float(score))	
	return tt
def alignment_matrix(tt,sws,tws):
	
	ls,lt=map(len,[sws,tws])
	matrix = [[0.0] * lt for _ in range(ls)]
	for i in range(ls):
		for j in range(lt):
			matrix[i][j] =  tt[sws[i]].get(tws[j], __min__)
	return matrix 


 
def min_cutnalign(tt, stdin):
	for i,line in enumerate(stdin):
		if i % 10000 ==0:
			logging.info('Line %d'%i)
		sws, tws = map(lambda x: x.split(), line.rstrip("\n").split("\t"))
		lx , ly  = len(sws), len(tws)
		assert lx<=100 and ly<=100 , "Sentence %d too long!"%i
		matrix   = alignment_matrix(tt, sws, tws) 
		
		alignment= _partitionize.partitionize_in_C(matrix, lx, ly) 
		print (alignment) 
		
if __name__ == '__main__': 
	import argparse
	parser = argparse.ArgumentParser(description="""
	This is an python script for real-time word alignment if given the translation table in advance.
	""")
	parser.add_argument('-t', action='store', dest='tt', type=argparse.FileType('r'),
		            help='translation table')
	parser.add_argument('-i', action='store', dest='input', type=argparse.FileType('r'),
		            help='parallel corpus')
	parser.add_argument('-r', action='store', dest='reverse', type=bool, default =False,
		            help='parallel corpus')
	parser.add_argument('--e2f', action='store', dest='e2f', type=argparse.FileType('r'),
		            help='parallel corpus')
	parser.add_argument('--f2e', action='store', dest='f2e',  type=argparse.FileType('r'),
		            help='parallel corpus')
	parser.add_argument('--version', action='version', version='%(prog)s 0.1')
	args   = parser.parse_args() 
	#print (args)
	if args.tt:
		tt    = read_tt(args.tt,args.reverse)
	if args.e2f and args.f2e:
		tt    = read_tt_e2f(args.e2f,args.f2e,args.reverse)
	min_cutnalign(tt, args.input)
