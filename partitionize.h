/*
 * cutnalign.h
 *
 *  Created on: 2 Jun 2016
 *      Author: hao
 */

#ifndef PARTITIONIZE_H_
#define PARTITIONIZE_H_

#define _MIN_ 10e-7
typedef enum { false, true } bool;
/* File : example.h */
/* Copyright (c) 2017, Yves Lepage, Chonlathorn Kwankajornkiet and Hao Wang*/
typedef struct _LIST{
	int i;
	int j;
	struct _LIST * next;
}LIST;


typedef struct _TREE_AND_LINK{
	struct _LIST *head;
 	struct _TREE *root;
}TREE_AND_LINK;

typedef struct _MATRIX
{

	int m,n;
	double **mat;
}MATRIX;

typedef struct _TUPLE{
	double left;
	double right;
}TUPLE;


typedef struct _PARTITION{
 	int i;
 	int j;
 	bool direction;
}PARTITION;


#endif /* PARTITIONIZE_H_ */
