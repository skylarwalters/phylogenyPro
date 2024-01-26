UPGMA Overview
UPGMA (unweighted pair group method with arithmetic mean) is a method for 
constructing phylogenic trees from information provided in a distance matrix. 
It aims to show relation through relative distances (eg. more closely-related 
species are closer together, while less closely related species are farther 
apart).

Program Input:
To run this program as a python program, type:

python3 upgma.py <sample_distance.dist> <output_file.dot>

The file may also be run as a shell script from the terminal. To do so, use the
command:

sh upgma.sh <sample_distance.dist> <output_file.dot>

Program Output:
The output of this program is printed as a GraphViz object that can be used to 
visualize the relationship between the organisms. To see the graph itself, 
this website is helpful: 
https://dreampuf.github.io/GraphvizOnline 

There are several test files provided, including: 
mat1: Simple base case
mat2: Degenerate case (A - B - C - D), all dist = 1
mat3: Trivial 3-node test case.
mat4: medium test case, nodes = 4
mat5: medium test case, nodes = 5
mat6: medium test case, nodes = 5
mat7: Primates + bovine + mouse
mat8, mat9: blank tests