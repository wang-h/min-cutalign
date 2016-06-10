/*
 * partitionize.c
 *
 *  Created on: 2 Jun 2016
 *      Author: hao
 */
/* File :partitionize.c */
#include "partitionize.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef max
#define max(a, b)            (((a) > (b)) ? (a) : (b))
#define INT_DIGITS 19		/* enough for 64 bit integer */
#endif

/* for debug */
void printMatrice(MATRIX *matrix, int numberOfLines, int numberOfColumns) {
	int row, columns;
	for (row = 0; row < numberOfLines; row++)
	{
	    for(columns = 0; columns < numberOfColumns; columns++)
	         printf("%f     ", matrix->mat[row][columns]);
	    printf("\n");
	 }
}
void printList(LIST **list_head) {
	LIST *conductor = *list_head;
	while ( conductor != NULL ) {
	       printf( "%d-%d\n", conductor->i , conductor->j);
	       conductor = conductor->next;
	}
}


char *itoa(int i){
  /* Room for INT_DIGITS digits, - and '\0'  standard C library does not include itoa function !!!!*/
  static char buf[INT_DIGITS + 2];
  char *p = buf + INT_DIGITS + 1;	/* points to terminating '\0' */
  if (i >= 0) {
    do {
      *--p = '0' + (i % 10);
      i /= 10;
    } while (i != 0);
    return (p);
  }
  else {			/* i < 0 */
    do {
      *--p = '0' - (i % 10);
      i /= 10;
    } while (i != 0);
    *--p = '-';
  }
  return (p);
}

/* function for LIST data structure*/
void list_update(LIST **head, int i, int j){
	LIST * current = (LIST *)malloc(sizeof(LIST));
	current->i = i;
	current->j = j;
	current->next =  *head;
	*head = current;

 }

void list_update_range(LIST **head, int i_start, int i_end, int j_start, int j_end){
	int i, j;
	for(i = i_start; i < i_end; i++){
		for(j = j_start; j < j_end; j++){
			list_update(head, i, j);
		}
	}
}
void destoryMatrix(MATRIX *T){
	int i;
	for (i=0; i<T->m; i++)
	{
		free(T->mat[i]);
	}
	free(T->mat);
 }
void destoryLinklist(LIST *head){
	LIST * node = head;
	while (  node   != NULL) {
		LIST * temp =  node ;
		node   =  node ->next;
		free (temp);
	}
	head = NULL;
}

/* main code */
TUPLE fmeasure_xy(int i1, int j1, int i2, int j2, int i3, int j3, MATRIX *matrix){
	double WAB, WA_B, W_AB, W_A_B = 0.0;
	double W_ABA_B ,W_A_BAB, score, score_ = 0.0;
	double Pi1j1 = matrix->mat[i1][j1];
	double Pi1j2 = matrix->mat[i1][j2];
	double Pi1j3 = matrix->mat[i1][j3];
	double Pi2j1 = matrix->mat[i2][j1];
	double Pi2j2 = matrix->mat[i2][j2];
	double Pi2j3 = matrix->mat[i2][j3];
	double Pi3j1 = matrix->mat[i3][j1];
	double Pi3j2 = matrix->mat[i3][j2];
	double Pi3j3 = matrix->mat[i3][j3];

	WAB 	= Pi2j2 + Pi1j1 - Pi2j1 - Pi1j2;
	W_A_B	= Pi3j3 + Pi2j2 - Pi2j3 - Pi3j2;
	W_AB	= Pi2j3 + Pi1j2 - Pi1j3 - Pi2j2;
	WA_B	= Pi3j2 + Pi2j1 - Pi3j1 - Pi2j2;
	W_ABA_B =  WA_B + W_AB;
	W_A_BAB =  W_A_B + WAB;
	TUPLE scores;
	score   =  WAB /(W_ABA_B + 2 * WAB ) + W_A_B/(W_ABA_B + 2 * W_A_B );
	score_  =  W_AB/(W_A_BAB + 2 * W_AB) + WA_B /(W_A_BAB + 2 * WA_B );
	scores.left = score;
	scores.right = score_;
	return (scores);
}
PARTITION search_best_partition(int i1, int j1, int i3, int j3, MATRIX *matrix){
	double bestScore = -2.0;
	double score, score_, current_score;
	PARTITION bestPartition;
	int i2,j2;
	for(i2 = i1 + 1; i2 < i3; i2++){
		for(j2 = j1 + 1 ; j2 < j3; j2++){
			TUPLE scores = fmeasure_xy(i1, j1, i2, j2, i3, j3, matrix);
			score  = scores.left;
			score_ = scores.right;
			current_score = max(score, score_);
			if(current_score > bestScore){
				bestScore =  current_score;
				bestPartition.i = i2;
				bestPartition.j = j2;
				bestPartition.direction = ( score >= score_)? true: false;
			}
		}
	}
	return (bestPartition);
}

int partitionize(int i1, int j1, int i2, int j2, MATRIX *matrix, LIST **head)
{


	if(i2 - i1 <= 1 || j2 - j1 <= 1){
		list_update_range(head, i1, i2, j1, j2);
		return (1);
	}
	PARTITION best_partition;
	best_partition = search_best_partition(i1, j1, i2, j2, matrix);
	int i = best_partition.i;
	int j = best_partition.j;
	bool mainDiag = best_partition.direction;
	if(i == i1 || i == i2 || j == j1 || j == j2){
		list_update_range(head,i1, i2, j1, j2);
		return (1);
	}
	if(mainDiag){
		partitionize(i1, j1, i, j, matrix, head);
		partitionize(i, j, i2, j2, matrix, head);
		return (1);
	}
	else{
		partitionize(i, j1, i2, j, matrix, head);
		partitionize(i1, j, i, j2, matrix, head);
		return (1);
	}
	return (1);
 }
MATRIX accumulated_alignment_matrix(double** matrix, int m, int n)
{
	int i,j;
	MATRIX  SAT;
	SAT.m = m+1;
	SAT.n = n+1;
	SAT.mat = (double**)malloc(SAT.m*sizeof(double*));
	SAT.mat[0]=(double*)malloc(SAT.n*sizeof(double));
	for(j=0;j<SAT.n;j++){
		SAT.mat[0][j]= 0.0;
	}
	for(i=1;i<SAT.m;i++){
		SAT.mat[i]=(double*)malloc(SAT.n*sizeof(double));
		SAT.mat[i][0]= 0.0;
		for(j=1;j<SAT.n;j++){
			SAT.mat[i][j]= _MIN_;
		}
	}
	/* SAT: summed area table */
	for(i=1;i < SAT.m; i++){
		for(j=1;j < SAT.n; j++){
			SAT.mat[i][j] =  SAT.mat[i][j-1] +  SAT.mat[i-1][j] -  SAT.mat[i-1][j-1] +  matrix[i-1][j-1] ;
		}
	}

	return (SAT);
 }




/* function for LIST data structure to string*/
void list2str(char *alignments, LIST **list){
	LIST *conductor = *list;
	while ( conductor != NULL ) {
	       strcat(alignments,  itoa(conductor->i));
	       strcat(alignments, "-");
	       strcat(alignments,  itoa(conductor->j));
	       if ( conductor->next != NULL ){
	    	   strcat(alignments, " ");
	       }
	       conductor = conductor->next;

		}
}
 char * partitionize_in_C(double **matrix, int lx, int ly){
		LIST *list_head;
		list_head = NULL;
		static char alignmentsBuff[400];
		MATRIX SAT = accumulated_alignment_matrix(matrix, lx, ly);
		partitionize(0, 0, lx, ly, &SAT, &list_head);
		destoryMatrix(&SAT);
		alignmentsBuff[0] = '\0';
		list2str(alignmentsBuff, &list_head);
		destoryLinklist(list_head);
		return (alignmentsBuff);

}


