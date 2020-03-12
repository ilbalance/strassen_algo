from math import ceil,log
import numpy as np
import random

random.seed(0)

def createRandomMatrix(n):
    maxVal = 1000
    matrix = []
    for i in range(n):
        matrix.append([random.randint(0, maxVal) for el in range(n)])
    return matrix

def saveMatrix(A, B, filename):
    f = open(filename, 'w')
    for i, matrix in enumerate([A, B]):
        if i != 0:
            f.write('\n')
        for line in matrix:
            f.write('\t'.join(map(str, line)) + '\n')

n = int(input("n = "))
matrixA = createRandomMatrix(n)
matrixB = createRandomMatrix(n)
saveMatrix(matrixA,matrixB,input("save in: "))
print('Matrix A: \n', np.matrix(matrixA))
print('\n')
print('Matrix B: \n', np.matrix(matrixB))

def read(filename):
    lines=open(filename, 'r').read().splitlines()
    A = []
    B = []
    matrix = A
    for line in lines:
        if line != '':
            matrix.append([int(x) for x in line.split('\t')])
        else:
            matrix = B
    return A, B

def printMatrix(matrix):
    for line in matrix:
        print('\t'.join(map(str, line)))

def ikjMatrixProduct(A, B):
    n = len(A)
    C = [[0 for j in range(n)] for j in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def add(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def substract(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def strassenR(A, B):
    n = len(A)
    if n <= LEAF_SIZE:
        return ikjMatrixProduct(A, B)
    else:
        newSize = n / 2
        a11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        a12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        a21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        a22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        b11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        b12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        b21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        b22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        aResult = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        bResult = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
        
        for i in range(0, newSize):
            for j in range(0, newSize):
                a11[i][j] = A[i][j]
                a12[i][j] = A[i][j + newSize]
                a21[i][j] = A[i + newSize][j]
                a22[i][j] = A[i + newSize][j + newSize]
                b11[i][j] = B[i][j]
                b12[i][j] = B[i][j + newSize]
                b21[i][j] = B[i + newSize][j]
                b22[i][j] = B[i + newSize][j + newSize] 
        aResult = add(a11, a22)
        bResult = add(b11, b22)
        p1 = strassenR(aResult, bResult)
        
        aResult = add(a21, a22)
        p2 = strassenR(aResult, b11)
        
        bResult = substract(b12, b22)
        p3 = strassenR(a11, bResult)
        
        bResult = substract(b21, b11)
        p4 = strassenR(a22, bResult)
        
        aResult = add(a11, a12)
        p5 = strassenR(aResult, b22)
        
        aResult = substract(a21, a11)
        bResult = add(b11, b12)
        p6 = strassenR(aResult, bResult)
        
        aResult = substract(a12, a22)
        bResult = add(b21, b22)
        p7 = strassenR(aResult, bResult)
        
        c12 = add(p3, p5)
        c21 = add(p2, p4)
        
        aResult = add(p1, p4)
        bResult = add(aResult, p7)
        c11 = substract(bResult, p5)

        aResult = add(p1, p3)
        bResult = add(aResult, p6)
        c22 = substract(bResult, p2)
        
        C = [[0 for j in range(0, n)] for i in range(0, n)]
        for i in range(0, newSize):
            for j in range(0, newSize):
                C[i][j] = c11[i][j]
                C[i][j + newSize] = c12[i][j]
                C[i + newSize][j] = c21[i][j]
                C[i + newSize][j + newSize] = c22[i][j]
        return C

def strassen(A, B):
    assert type(A) == list and type(B) == list
    assert len(A) == len(A[0]) == len(B) == len(B[0])
    
    nextPowerOfTwo = lambda n:2**int(ceil(log(n, 2)))
    n = len(A)
    m = nextPowerOfTwo(n)
    APrep = [[0 for i in range(m)] for j in range(m)]
    BPrep = [[0 for i in range(m)] for j in range(m)]
    for i in range(n):
        for j in range(n):
            APrep[i][j] = A[i][j]
            BPrep[i][j] = B[i][j]
    CPrep = strassenR(APrep,BPrep)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = CPrep[i][j]
    return C

def saveMatrix(matrixA, filename):
    f = open(filename, 'w')
    for i, matrix in enumerate([matrixA]):
        if i != 0:
            f.write('\n')
        for line in matrix:
            f.write('\t'.join(map(str, line)) + '\n')

LEAF_SIZE = int(input("leaf size: "))
A, B = read(input('path to file: '))
C = strassen(A, B)
print('Matrix A: \n', np.matrix(A), '\n')
print('Matrix B: \n', np.matrix(B), '\n')
print('Matrix C = A * B: \n', np.matrix(C))
saveMatrix(C, input("save file: "))
