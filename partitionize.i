/* partitionize.i */
 %module partitionize
 %{
 /* Put header files here or function declarations like below */
 #include "partitionize.h" 
 extern char* partitionize_in_C(double **matrix, int lx, int ly);
 %}
 
 %typemap(in) double ** {
	int row = PyList_Size($input);
	int col = PyList_Size(PyList_GetItem($input,0));
	$1 = (double **) malloc((row+1)*sizeof(double *));
	int i,j;
	for (i = 0; i < row; ++i) {
		j = 0;
		$1[i] = (double *) malloc((col+1)*sizeof(double));
		for (j = 0; j < col; ++j){
			$1[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem($input,i),j));  
		}
	}
 }
 
// This cleans up the double ** we malloc'd before the function call
%typemap(freearg) double** {
	 free((double **) $1);
} 
 extern char* partitionize_in_C(double **matrix, int lx, int ly);
