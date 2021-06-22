# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:59:57 2021

@author: reint
"""

class Matrix:
    '''matrix'''
    
    def __init__(self, lijst=[]):
        self.matrix = lijst
        self.dim = (len(lijst[0]), len(lijst))
        self.kolommen = lijst
        self.rijen =[]
        for rij in range(self.dim[0]):
            self.rijen.append([])
            for i in range(self.dim[1]):
                self.rijen[rij].append(lijst[i][rij])
    
        
    def __str__(self):
        string = ''
        for rij in self.rijen:
            for i in rij:
                string += str(i) + ' '
            string += '\n'
        
        return string
    
    def __add__(self, other):
        
        if self.dim == other.dim:
            som = []
            for i in range(self.dim[1]):
                som.append([])
                for j in range(self.dim[0]):
                    som[i].append((self.matrix[i][j] + other.matrix[i][j]) % 2)
        else:
            raise ValueError('Matrices zijn niet van dezelfde dimensie')
        return Matrix(som)
        
    def __mul__(self, other):
        if int(self.dim[1]) == int(other.dim[0]):
            product = []
            
            for kolom in range(other.dim[1]):
                product.append([])
                for rij in range(self.dim[0]):
                    ijproduct = 0
                    for i in range(self.dim[1]):
                        ijproduct += self.rijen[rij][i] * other.kolommen[kolom][i]
                    product[kolom].append(ijproduct%2)
        else:
            raise ValueError('Matrices zijn niet vermenigvuldigbaar')
        
        return Matrix(product)
        
    
def nulmatrix(n, m):
    kolommen = n * [0]
    nulmatrix = m * [kolommen]
    return Matrix(nulmatrix)

def matrixappend(matrix, n, m):
    nieuwmatrix = []
    print(matrix.matrix)
    for kolom in range(matrix.dim[1]):
        nieuwmatrix.append([])
        for rij in range(matrix.dim[0]):
            if kolom == m and rij == n:
                nieuwmatrix[kolom].append(1)
            else:
                nieuwmatrix[kolom].append(matrix.matrix[kolom][rij])
    
    return Matrix(nieuwmatrix)


t = nulmatrix(5,6)

print(matrixappend(t, 2,3))

def codeer(invoer): #Als invoer, geen een vector van 4 binaire getallen
    C = Matrix([[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
    return C*invoer #Als uitvoer krijg je een vector met 7 binaire getallen, de originele 4 en de drie pariteitbits 

def decodeer(invoer): #Als invoer, geef een vector van 7 binaire getallen
    D = Matrix([[0,0,0,0],[0,0,0,0],[1,0,0,0],[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    return D*invoer #Als uitvoer worden het eerste, tweede en vierde getal verwijdert

def corrigeren(invoer): #Als invoer, geef een vector van 7 getallen die voorkomt uit de codeer functie waar maximaal 1 bit in is veranderd 
    R = Matrix([[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]])
    lijst = (R*invoer).matrix 
    lengte = len(lijst[0])
    Nul = Matrix([lengte*[0]])
    if (R*invoer).matrix == Nul.matrix: 
        return invoer #Als geen bit in de vector is verandert, krijg je de invoer terug   
    else:  
        locatie_fout = int(str((R*invoer).matrix[0][2]) + str((R*invoer).matrix[0][1]) + str((R*invoer).matrix[0][0]), 2)
        herstelling = Matrix([(locatie_fout-1)*[0]+[1]+(7-locatie_fout)*[0]])
        return invoer + herstelling #Als er ergens een fout is gemaakt, wordt de locatie van deze fout gevonden en gecorrigeert
