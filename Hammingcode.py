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

class Matrix1:
    '''Maakt een matrix met alleen maar 0 en 1 als elementen
    
    Keyword arguments:
    dim - De dimensie van de matrix (default 1x1)
    posities - De plekken van de matrix waar er een 1 staat
    
    '''
    
    def __init__(self, dim=[1,1], posities=[]):
        self.posities = posities
        self.dim = dim
        
    def __str__(self):
        #print de matrix door het in een grid te printen
        string = ''
        for rij in range(1, self.dim[0] + 1):
            for kolom in range(1, self.dim[1] + 1):
                if (rij, kolom) in self.posities: #Als de positie in de lijst met posities met een 1 staat, print dan een 1
                    string += '1 '
                else: #Print elders een 0
                    string += '0 '
            string += '\n'
        return string
        
    def __add__(self, other):
        # Telt twee matrices bij elkaar op doormiddel van een xor vergelijking tussen het elementen op plek (rij, kolom) van self en other, voor elke rij en elke kolom
        if self.dim == other.dim:
            somposities = []
            for rij in range(1, self.dim[0] + 1):
                for kolom in range(1, self.dim[1] + 1):
                    if ((rij, kolom) in self.posities) ^ ((rij, kolom) in other.posities):
                        somposities.append((rij, kolom))
        else:
            raise ValueError('Matrices zijn niet van dezelfde dimensie')
        return Matrix1(self.dim, somposities)
    
    def __mul__(self, other):
        #Vermenigvuldigt twee matrices met elkaar
        if self.dim[1] == other.dim[0]:
            productdim = (self.dim[0], other.dim[1])
            productposities = []
            for rij in range(1, productdim[0] + 1):
                for kolom in range(1, productdim[1] + 1):
                    som = 0
                    for i in range(1, self.dim[1]+ 1):
                        if ((rij, i) in self.posities) and ((i, kolom) in other.posities):
                            som += 1
                    if som%2 == 1:
                        productposities.append((rij, kolom))
        else:
            raise ValueError('Matrices zijn niet vermenigvuldigbaar')
        return Matrix1(productdim, productposities)
            
    def maak_fouten(self, aantal): #invoer is een matrix c.q. vector met de te verzenden Hamming code
        indices = random.sample(range(1, self.dim[0]+1), k=aantal) #hier wordt bepaald waar de fouten komen
        for i in indices:
            if (i,1) in self.posities:
                self.posities.remove((i,1))
            else:
                self.posities.append((i,1))
        return self #code met fouten (altijd in 1e kolom), als matrix    

def Hamming_matrix_H(lencode, lenbericht): #werkt met Matrix1
    if lencode== 2**(lencode-lenbericht)-1: #standaard Hamming code
        H= Matrix1([lencode-lenbericht, lencode]) 
        for n in range( H.dim[0]): #gaat rijen langs
            pbit= 2**n
            for i in range(pbit, H.dim[1]+1, 2*pbit): #gaat elementen van rij n langs
                for j in range(i, i+pbit): #maakt pbit achtereenvolgende elementen 1
                    H.posities.append((n+1,j))
    elif lencode== 2**(lencode-lenbericht-1): #Hamming code met extra parity bit
        H= Hamming_matrix_H(lencode-1, lenbericht)
        H.dim[0]+=1
        for i in range(1, H.dim[1]+1):
            H.posities.append((H.dim[0], i)) #vult laatste rij met enen
    else:
        raise ValueError('Waardes geven geen bestaande Hammingcode')
    return H           
 
def Hamming_matrices(lengcode, lengbericht): #werkt niet en is niet met Matrix1
    
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
        H = Matrix1([3,7],[(1,1),(1,3),(1,5),(1,7),(2,2),(2,3),(2,6),(2,7),(3,4),(3,5),(3,6),(3,7)])
        if (H*invoer).posities == Matrix1([(H*invoer).dim[0],1],).posities: 
            return invoer #Als geen bit in de vector is verandert, krijg je de invoer terug   
        else:  
            locatie_fout = ''
            for i in range(1, (H*invoer).dim[0]+1):  
                if (i,1) in (H*invoer).posities: 
                    locatie_fout += '1'
                else: 
                    locatie_fout += '0'
        locatie_fout = int(locatie_fout[::-1],2) 
        invoer += Matrix1([7,1],[(locatie_fout,1)])         
        return invoer 
