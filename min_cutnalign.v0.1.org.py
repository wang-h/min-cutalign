# -*- coding: utf-8 -*-
from collections import defaultdict
from copy import deepcopy
import math,time
import pprint
__min__=10e-7
import logging
logging.basicConfig( level=logging.INFO)
#        A          A   
#     +--------+-------+
#  B  |  AB    |  _AB  |
#     +--------+-------+
# _B  |  A_B   | _A_B  |
#     +--------+-------+
def FmeasureXY(matrix, i1, j1, i2, j2, i3, j3):
	Pi1j1, Pi1j2, Pi1j3 = matrix[i1][j1]  , matrix[i1][j2], matrix[i1][j3]
	Pi2j1, Pi2j2, Pi2j3 = matrix[i2][j1]  , matrix[i2][j2], matrix[i2][j3]
	Pi3j1, Pi3j2, Pi3j3 = matrix[i3][j1]  , matrix[i3][j2], matrix[i3][j3]
	AB	= Pi2j2 + Pi1j1 - Pi2j1 - Pi1j2
	_A_B	= Pi3j3 + Pi2j2 - Pi2j3 - Pi3j2
	_AB 	= Pi2j3 + Pi1j2 - Pi1j3 - Pi2j2
	A_B 	= Pi3j2 + Pi2j1 - Pi3j1 - Pi2j2
	_ABA_B = A_B + _AB
	_A_BAB = AB  + _A_B
	score  =  AB/(_ABA_B  + AB  + AB) + _A_B/(_ABA_B + _A_B + _A_B)
	score_ = _AB/(_A_BAB + _AB + _AB) +  A_B/(_A_BAB +  A_B +  A_B)
	return (score, score_)

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

def accumulated_alignment_matrix(matrix):
	lx,ly=len(matrix),len(matrix[0])
	accumulated_matrix=[[0.0] * (ly+1) for _ in range(lx+1)]
	accumulated_matrix[1][1] = matrix[0][0]
	for i in range(0,lx):
		for j in range(0,ly):
			accumulated_matrix[i+1][j+1] = accumulated_matrix[i][j+1] + accumulated_matrix[i+1][j ]\
				 - accumulated_matrix[i][j] + matrix[i][j]
	return 	accumulated_matrix 
def search_best_partition(matrix, i1, j1, i3, j3,lx,ly):
	bestScore = -2.0
	bestPartition = None
	for i2 in range(i1+1, i3):
		for j2 in range(j1+1, j3):
			score, score_     =  FmeasureXY(matrix, i1, j1, i2, j2, i3, j3)
			current_score     =  max(score, score_)
			if  current_score > bestScore:
				bestScore =   current_score
				bestPartition = (i2,j2,( current_score  == score)) 
	return bestPartition

def partitionize(matrix, i1, j1, i2, j2, links):
	# Set a minimal block size.
	# If the size of the block is bigger, then call recursively.	
	lx,ly = len(matrix),len(matrix[0])
	maxblocksize = 3
	if i2 - i1 <= 1 or j2 - j1 <= 1:
		links.update((i, j) for i in range(i1, i2) for j in range(j1, j2))
		return { (i1,i2): ((j1,j2), None, None) }
	i, j, mainDiag = search_best_partition(matrix, i1, j1, i2, j2,lx,ly)
	print (i, j, mainDiag)
	if mainDiag:
		tree1 = partitionize(matrix, i1, j1, i, j, links)
		tree2 = partitionize(matrix, i, j, i2, j2, links)  
	else:
		tree1 = partitionize(matrix, i, j1, i2, j, links)
		tree2 = partitionize(matrix, i1, j, i, j2, links)
	return {(i1,i2):((j1,j2), tree1, tree2) }

def min_cutnalign(tt, stdin):
	for i,line in enumerate(stdin):
		if i % 10000 ==0:
			logging.info('Line %d'%i)
		sws, tws = map(lambda x: x.split(), line.rstrip("\n").split("\t"))
		lx , ly  = len(sws), len(tws)
		matrix   = alignment_matrix(tt, sws, tws)
		accumulated_matrix  = accumulated_alignment_matrix(matrix)
		links = set()
		tree = partitionize(accumulated_matrix, 0, 0, lx, ly, links)
		print (" ".join(str(x)+"-"+str(y) for x,y in links))
		break
		
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
	args = parser.parse_args() 
	if args.tt:
		tt    = read_tt(args.tt,args.reverse)
	if args.e2f and args.f2e:
		tt    = read_tt_e2f(args.e2f,args.f2e,args.reverse)
	min_cutnalign(tt, args.input)
