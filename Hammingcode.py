# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:59:57 2021

@author: reint
"""
import random

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

    def matrixappend(self, n, m):
        nieuwmatrix = []
        print(self.matrix)
        for kolom in range(self.dim[1]):
            nieuwmatrix.append([])
            for rij in range(self.dim[0]):
                if kolom == m and rij == n:
                    nieuwmatrix[kolom].append(1)
                else:
                    nieuwmatrix[kolom].append(self.matrix[kolom][rij])
    
        return Matrix(nieuwmatrix)
    


    def maak_fouten(self, aantal): #invoer is een matrix c.q. vector met de te verzenden Hamming code
        indices = random.sample(range(self.dim[0]), k=aantal) #hier wordt bepaald waar de fouten komen
        for i in indices:
            if self.rijen[i][0]==0:
                self.rijen[i][0]=1
            else:
                self.rijen[i][0]=0
        return self #code met fouten, als matrix

t = nulmatrix(5,6)

print(matrixappend(t, 2,3))


    
 def Hamming_matrices(lengcode, lengbericht): #Ga ervanuit dat standaardmatrices geïmplementeerd zijn
    
    H= Matrix(lengcode-lengbericht, lengcode) #nulmatrix
    for n in range(H.dim[0]): #gaat rijen langs
        pbit= 2**n
        for i in range(pbit, H.dim[1], 2*pbit): #gaat elementen van rij n langs
            for j in range(i, i+pbit): #maakt pbit achtereenvolgende elementen 1
                H.rijen[n][j]=1
    """Ik denk dat H werkt als de opzet van de klasse anders is, 
    ik heb het nog niet getest."""
    
    G= Matrix(lengcode, lengbericht)
    n=0 #houdt aantal keer pbit bij = rij van H
    j=0 #houdt aantal keer databit bij
    for k in range(lengcode):#ofwel aantal rijen
        if k==2**n:
            macht_in_rij=1
            i_H=0
            for i in range(lengbericht): #ofwel aantal kolommen
                while i <= macht_in_rij:
                    macht_in_rij = macht_in_rij * 2
                    i_H+=1
                G.rijen[k][i]=H.rijen[n][i_H]
                    
            """Denk dat G en H ongeveer kloppen, 
            nog niet heel goed nagekeken of getest."""
            n+=1
        else:
            for i in range(lengbericht):
                if i==j:
                    G.rijen[k][i]=1 #anders blijft 0, "eenheid"
                j+=1
    return G, H

def codeer(invoer): #Als invoer, geen een vector van 4 binaire getallen
    G = Matrix([[1,1,1,0,0,0,0],[1,0,0,1,1,0,0],[0,1,0,1,0,1,0],[1,1,0,1,0,0,1]])
    return G*invoer #Als uitvoer krijg je een vector met 7 binaire getallen, de originele 4 en de drie pariteitbits 

def decodeer(invoer): #Als invoer, geef een vector van 7 binaire getallen
    D = Matrix([[0,0,0,0],[0,0,0,0],[1,0,0,0],[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    return D*invoer #Als uitvoer worden het eerste, tweede en vierde getal verwijdert

def corrigeren(invoer): #Als invoer, geef een vector van 7 getallen die voorkomt uit de codeer functie waar maximaal 1 bit in is veranderd 
    H = Matrix([[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]])
    Nul = Matrix([lengte = len((H*invoer).matrix [0])*[0]])
    if (H*invoer).matrix == Nul.matrix: 
        return invoer #Als geen bit in de vector is verandert, krijg je de invoer terug   
    else:  
        locatie_fout = int(str((H*invoer).matrix[0][2]) + str((H*invoer).matrix[0][1]) + str((H*invoer).matrix[0][0]), 2)
        herstelling = Matrix([(locatie_fout-1)*[0]+[1]+(7-locatie_fout)*[0]])
        return invoer + herstelling #Als er ergens een fout is gemaakt, wordt de locatie van deze fout gevonden en gecorrigeert
