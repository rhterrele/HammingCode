# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:59:57 2021

@author: reint
"""
import random
import math
from functools import reduce

class Matrix:
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
        return Matrix(self.dim, somposities)
    
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
        return Matrix(productdim, productposities)
            
    def maak_fouten(self, aantal): #invoer is een matrix c.q. vector met de te verzenden Hamming code
        indices = random.sample(range(1, self.dim[0]+1), k=aantal) #hier wordt bepaald waar de fouten komen
        for i in indices:
            if (i,1) in self.posities:
                self.posities.remove((i,1))
            else:
                self.posities.append((i,1))
        return self #code met fouten (altijd in 1e kolom), als matrix    

def matrix_G(lencode, lenbericht):
    if lencode== 2**(lencode-lenbericht)-1: #standaard Hamming code
        G= Matrix([lencode, lenbericht])
        H_rij=1 #geeft aan welke rij de eerstvolgende is die met een rij van H correspondeert
        I_rij=1 #houdt bij de hoeveelste de volgende "identiteitsrij" is
        for rij in range(1, G.dim[0]+1):
            overgeslagen= 0
            if rij== H_rij: #rijen voor parity bits
                tweemacht=1
                primlijst=[] #geeft een lijst met elementen van een rij van H (primitief)
                for i in range(rij, G.dim[0]+1, 2*rij): #gaat elementen van rij langs
                    for j in range(i, i+rij): #maakt rij achtereenvolgende elementen 1
                        primlijst.append(j)
                for index in range(1, G.dim[0]+1):
                    if index == tweemacht:
                        tweemacht = 2 * tweemacht
                        overgeslagen+=1
                    elif index in primlijst:
                        G.posities.append((rij, index-overgeslagen))
                H_rij= 2*H_rij
            else: #identiteitsrijen
                G.posities.append((rij, I_rij))
                I_rij+=1
    elif lencode== 2**(lencode-lenbericht-1): #Hamming code met extra parity bit 
        G= matrix_G(lencode-1, lenbericht)
        G_ep= matrix_G_extra_paritybit(lencode)
        G= G_ep * G
    else:
        raise ValueError('Waardes geven geen bestaande Hammingcode')
    return G  
'
def matrix_H(lencode, lenbericht):
    if lencode== 2**(lencode-lenbericht)-1: #standaard Hamming code
        H= Matrix([lencode-lenbericht, lencode]) 
        for n in range( H.dim[0]): #gaat rijen langs
            pbit= 2**n
            for i in range(pbit, H.dim[1]+1, 2*pbit): #gaat elementen van rij n langs
                for j in range(i, i+pbit): #maakt pbit achtereenvolgende elementen 1
                    H.posities.append((n+1,j))
    elif lencode== 2**(lencode-lenbericht-1): #Hamming code met extra parity bit
        H= matrix_H(lencode-1, lenbericht)
        H.dim[0]+=1
        H.dim[1]+=1
        for i in range(1, H.dim[1]+1):
            H.posities.append((H.dim[0], i)) #vult laatste rij met enen
    else:
        raise ValueError('Waardes geven geen bestaande Hammingcode')
    return H

def matrix_R(lencode, lenbericht):
    if lencode== 2**(lencode-lenbericht)-1 or lencode== 2**(lencode-lenbericht-1): #standaard Hamming code of met extra paritybit
        R= Matrix([lenbericht, lencode], [])
        n=1
        beginwaarde=1
        for rij in range(1, R.dim[0]+1):
            for kolom in range(beginwaarde, R.dim[1]+1):
                if n == kolom: 
                    n = 2*n
                else:
                    R.posities += [(rij, kolom)]
                    beginwaarde = kolom + 1
                    break
    else:
        raise ValueError('Waardes geven geen bestaande Hammingcode')
    return R

def matrix_Ge(invoer): #Als invoer geef de lengte van de vector waarme je deze matrix mee wilt vermenigvuldigen  
    Ge = Matrix([invoer + 1, invoer], )
    for i in range(1, invoer + 1): 
        Ge.posities += [(i,i)] #Voegt op de diagonaal enen toe 
        Ge.posities += [(invoer+1, i)] #Voegt op de onderste rij enen toe
    return Ge

def matrix_He(invoer): #Als invoer geef de lengte van de vector waarme je deze matrix mee wilt vermenigvuldigen
    He = Matrix([1,invoer + 1], )
    for i in range(1, invoer + 2): 
        He.posities += [(1,i)] #Voegt op elke locatie een 1 toe
    return He 

def matrix_Re(invoer): #Als invoer geef de lengte van de vector waarme je deze matrix mee wilt vermenigvuldigen 
    Re = Matrix([invoer, invoer + 1], )
    for i in range(1, invoer + 1): 
        Re.posities += [(i,i)] #Voegt op de diagonaal enen toe 
    return Re

def codeer_extra(invoer, lenbericht, lencode): #Als invoer, geef een matrix in de vorm van een vector 
    G = matrix_G(lencode, lenbericht)
    Ge = matrix_Ge(lencode)
    return Ge*(G*invoer)  

def decodeer_extra(invoer, lencode, lenbericht): #Als invoer, geef een matrix in de vorm van een vector
    R = matrix_R(lencode, lenbericht)
    Re = matrix_Re(lencode)
    return R*(Re*invoer) 

def corrigeren_extra(invoer, lencode, lenbericht): #Als invoer, geef een vector die voorkomt uit de codeer functie met maximaal twee fouten erin 
        H = matrix_H(lencode, lenbericht)
        He = matrix_He(lencode)
        Re = matrix_Re(lencode)
        if (He*invoer).posities == Matrix([1,1], ).posities: #Als de pariteit van alle bits hetzelfde is gebleven, is geen fout gemaakt, of twee  
            if (H*(Re*invoer)).posities == Matrix([(H*(Re*invoer)).dim[0],1],).posities: 
                return invoer #Als geen bit in de vector is verandert, krijg je de invoer terug   
            else:  
                return print('Er zijn twee fouten gemaakt')
        else: 
            locatie_fout = ''
            for i in range(1, (H*(Re*invoer)).dim[0]+1): #Als er een fout is gemaakt, geeft (H*(Re*invoer)) de locatie in binair 
                if (i,1) in (H*invoer).posities: 
                    locatie_fout += '1'
                else: 
                    locatie_fout += '0'
            locatie_fout = int(locatie_fout[::-1],2) 
            invoer += Matrix([7,1],[(locatie_fout,1)]) #We tellen een vector met een 1 op de locatie van de fout op bij de invoer om de fout te corrigeren       
            return invoer 

def codeer(nibble, lencode, lenbericht): #Als invoer, geef een string met bits en de gewenste Hamming code
    nibblevector = Matrix([len(nibble), 1])
    for i in range(len(nibble)): # maakt een vector zodat matrixvermenigvuldiging kan
        if nibble[i]==1:
        nibblevector.posities.append(i+1, 1)
    G = matrix_G(lencode, lenbericht)
    return (G*nibblevector)  

def decodeer(invoer, lencode, lenbericht): #Als invoer, geef een matrix in de vorm van een vector
    R = matrix_R(lencode, lenbericht)
    nibblevector = R*invoer
    for i in range(len(invoer)): #maakt er een string bits van
        nibble = ''
        if (i, 1) in nibblevector.posities:
            nibble += '1'
        else:
            nibble += '0'
    return nibble 

def corrigeren(invoer, lencode, lenbericht): #Als invoer, geef een vector die voorkomt uit de codeer functie met maximaal 1 fout erin. 
        H = matrix_H(lencode, lenbericht)
        if (H*invoer).posities == Matrix([(H*invoer).dim[0],1],).posities: 
            return invoer #Als geen bit in de vector is verandert, krijg je de invoer terug   
        else:  
            locatie_fout = ''
            for i in range(1, (H*invoer).dim[0]+1): #Als er een fout is gemaakt, geeft (H*(Re*invoer)) de locatie in binair
                if (i,1) in (H*invoer).posities: 
                    locatie_fout += '1'
                else: 
                    locatie_fout += '0'
        locatie_fout = int(locatie_fout[::-1],2) 
        invoer += Matrix([7,1],[(locatie_fout,1)]) #We tellen een vector met een 1 op de locatie van de fout op bij de invoer om de fout te corrigeren      
        return invoer


    
    
    
    

def bits_maaklijst(bericht, m): #Zet de informatiebits op de goede plekken in een lijst, zodat op de lege plekken de parity bits kunnen staan
    lijst = [None] #De lijst met de eerste plek leeg voor de paritybit
    berichtplek = 0 #Houdt de plek in het bericht bij
    for i in range(1, 2**m):
        if math.log2(i).is_integer(): #Als i een 2-macht is, houd de plek leeg
            lijst.append(None)
        else: #Elders vul de bijbehorende waarde van het bericht in
            lijst.append(bericht[berichtplek])
            bericht += 1
    return lijst


def bits_codeer(bericht, m): #Vult de paritybits in voor een gegeven lijst. Invoer is het te versleutelen bericht en het aantal paritybits
    hammingbericht = bits_maaklijst(bericht, m) #Zet het bericht om in de goede format
    for m in range(m): #Gaat langs alle parity bits
        som = 0
        for i in range(len(hammingbericht)):
            if (i%(2**(m+1)))//(2**m) == 1 and type(hammingbericht[i]) == int: #Checkt voor de bits die horen bij de paritybit, en checkt of op die plaats een bit staat.
                som = (som + hammingbericht[i])%2
        
        hammingbericht[2**m] = som #past de paritybit aan
        
    totalesom = 0 #De som voor de paritybit die de parity van het hele bericht checkt 
    for i in range(1, len(bericht)):
        totalesom = (totalesom + bericht[i])%2
    
    bericht[0] = totalesom #De algemene paritybit wordt aangepast
    
    return bericht
    
def bits_maak_fouten(bericht, aantal): #invoer is een versleuteld bericht en het aantal gewilde fouten
    indices = random.sample(range(len(bericht)), k=aantal) #hier wordt bepaald waar de fouten komen
    for i in indices:
        bericht[i] = (bericht[i] + 1)%2 #Flipt de waarde van de bit
    return bericht #Stuurt terug het bericht met de fouten




def bits_corrigeren(bericht): #Corrigeert de mogelijke fouten in een bericht. Invoer is het versleuteld bericht
    aanbits = [] #De bits met een 1 in het bericht
    for i in range(len(bericht)):
        if bericht[i] == 1:
            aanbits.append(i)
    
    if aanbits: #checkt of aanbits niet leeg is
        fout = reduce(lambda x, y: x ^ y, aanbits) #Gaat langs de plekken met een 1 (aanbits) en voert dan steeds een xor uit.
    else:
        fout = 0
    parity = reduce(lambda x, y: (x+y)%2, bericht) #Checkt de parity van het bericht
    
    if fout != 0: #Als er een fout in het bericht wordt gedetecteerd
        if parity != 0: #Als de parity ook fout is 
            bericht[fout] = (bericht[fout] + 1)%2 #flipt de bit als daar de fout is
            print('er was ????n fout, en die is weggehaald')
        elif parity == 0: #Als er een fout is gedetecteerd, maar parity is nog steeds 0. Dan zijn er minstens twee fouten
            print('er zijn minstens twee fouten')
    else:
        print('er is geen fout')
        
    return bericht
    


def bits_decodeer(bericht): #Zet het versleuteld bericht weer om in het normale bericht. Invoer is het versleuteld bericht

    eindbericht = [] #Het bericht dat gestuurd wordt    

    for i in range(1, len(bericht)):
        if not math.log2(i).is_integer(): #Als i niet een 2-macht is, voeg die bit toe aan het eindbericht
            eindbericht.append(bericht[i])
    
    return eindbericht





def stringtobits(berichtstring): #Neemt de string van het bericht dat versleuteld moet worden, en geeft terug de string van de binaire representatie van de string van het bericht
    bitsstring = '' 
    for i in berichtstring:
        bitsstring += format(ord(i), '08b')
    return bitsstring



def bitsopdelen(bitsstring, nibblelengte): #Neemt een string van bits, en het aantal paritybits(ofwel de gewilde hammingcode), en verdeelt de bits in geschikte nibbles voor de hammingcodes
    if len(bitsstring)%(nibblelengte) != 0: #Als de lengte van de nibbles niet de lengte van de bitsstring deelt
        extrabits = ((nibblelengte) - (len(bitsstring)%(nibblelengte))) # het aantal toegevoegde bits wordt onthouden
        bitsstring += extrabits * '0' #Voegt nullen toe zodat de lengtes elkaar delen
    else:
        extrabits = 0
    
    bitslijst = [] #de lijst met de opgedeelde bits
    for i in range(len(bitsstring)): #Verdeelt alle bits in bitsstring in een lijst van lijsten
        if i%nibblelengte == 0:
            bitslijst.append([])
        bitslijst[i//nibblelengte].append(int(bitsstring[i]))
    
    return bitslijst, extrabits
            



def bitstostring(bitslijst, extrabits): #Neemt een lijst met opgedeelde bits, en voert de bijbehorende string uit
    bitsstring = ''
    for nibble in bitslijst:
        for i in nibble:
            bitsstring += str(i)
            
    bitsstring = bitsstring[:(len(bitsstring) - extrabits)] #Haalt de toegevoegde bits weg

    
    
    byteslijst = [] #Lijst met bytes van de bitsstring
    for byte in range(len(bitsstring)//8): #deelt bitsstring op in bytes, zodat die terug naar ascii karakters kunnen worden teruggezet
        byteslijst.append('')
        for i in range((byte*8), ((byte+1)*8)):
            byteslijst[byte] += bitsstring[i]
    
    
    berichtstring = ''
    for byte in byteslijst: #Voert iedere byte om naar het bijbehorende ascii karakter
        berichtstring += chr(int(byte, 2))

    return berichtstring
    
    

    

def main():
    berichtstring = input('Voer de string in: ')
    m = int(input('hoeveel paritybits? (exclusief de extra paritybit, die zit er altijd bij) '))
    methode = int(input('welke methode? 1 voor matrix, 2 voor bits:'))
    fouten = int(input('Hoeveel fouten?'))
    
    bitsstring = stringtobits(berichtstring)
    bitslijst, extrabits = (bitsopdelen(bitsstring, 2**m - m - 1))
    
    if methode == 1:
        versleuteldvectorlijst = []
        for nibble in bitslijst:
            versleuteldvectorlijst.append(codeer(nibble, len(nibble) + m, len(nibble))) #codeert alle nibbles
            
        vectorenfouten = random.choices(range(len(versleuteldvectorlijst)), k=fouten) #Kiest willekeurig in welke gecodeerde vectoren de fouten plaats zullen vinden
        for vector in vectorenfouten:
            versleuteldvectorlijst[vector] = maak_fouten(versleuteldvectorlijst[vector], 1) #Maakt voor elke vector in de willekeurig gekozen lijst 1 fout. Een vector kan meerdere fouten krijgen door meerdere keren in de lijst voor te komen
        
        for nibble in range(len(versleuteldvectorlijst)): #corrigeert de mogelijke fouten
            versleuteldvectorlijst[nibble] = corrigeren(versleuteldvectorlijst[nibble])
            
        eindbitslijst = []
        for nibblevector in versleuteldvectorlijst: #decodeert alle vectoren
            eindbitslijst.append(decodeer(nibblevector, len(nibblevector), len(nibblevector)-m))
            
    elif methode == 2:
        versleuteldbitslijst = []
        for nibble in bitslijst:
            versleuteldbitslijst.append(bits_codeer(nibble, m)) #codeert alle nibbles
        
        nibblesfouten = random.choices(range(len(versleuteldbitslijst)), k=fouten) #Kiest willekeurig in welke nibbles de fouten plaats zullen vinden
        for nibble in nibblesfouten:
            versleuteldbitslijst[nibble] = bits_maak_fouten(versleuteldbitslijst[nibble], 1) #Maakt voor elke nibble in de willekeurig gekozen lijst 1 fout. Een nibble kan meerdere fouten krijgen door meerdere keren in de lijst voor te komen
        
        for nibble in range(len(versleuteldbitslijst)): #corrigeert de mogelijke fouten
            versleuteldbitslijst[nibble] = bits_corrigeren(versleuteldbitslijst[nibble])
        
        
        eindbitslijst = []
        for nibble in versleuteldbitslijst: #Decodeert alle nibbles
            eindbitslijst.append(bits_decodeer(nibble))
        
    print('Het bericht aan het eind van het proces is: ', bitstostring(eindbitslijst, extrabits))
