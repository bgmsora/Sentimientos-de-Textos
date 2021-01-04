# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:58:37 2020

@author: Brandon
"""
import nltk 
from nltk.corpus import wordnet
import array as arr

def ObtenerRank(f):
    text=f.read().lower()
    numero=text.find('rank="')
    numero=numero+6
    numero=text[numero]
    return numero

def ObtenerRankTextos(x):
    rank=list()
    for ubicacion in range(2,x):
        z=str(ubicacion)
        #print(z)
        try:
            f=open('./corpusCriticasCine/'+z+'.xml')
            #leo y paso a minusculas todo
            numero=ObtenerRank(f)
            rank.append(numero)
            f.close()
        except Exception:
            pass
    return rank

def stopwords(palabras):
    f=open("stopwords.txt",encoding='utf-8')
    text=f.read()
    texto=nltk.word_tokenize(text)
    for w in texto:
        try:
            palabras=list(filter(lambda x: x != w, palabras))
            #print("quite ",w)
        except Exception:
            pass
    palabras=list(filter(lambda x: x != '.', palabras))
    palabras=list(filter(lambda x: x != ',', palabras))
    palabras=list(filter(lambda x: x != ')', palabras))
    palabras=list(filter(lambda x: x != '(', palabras))
    palabras=list(filter(lambda x: x != '``', palabras))
    palabras=list(filter(lambda x: x != '?', palabras))
    palabras=list(filter(lambda x: x != '!', palabras))
    palabras=list(filter(lambda x: x != '[', palabras))
    palabras=list(filter(lambda x: x != ']', palabras))
    for i in range(0,10):
        palabras=list(filter(lambda x: x != str(i), palabras))
    return palabras

def critica(f):
    text=f.read()
    f.close()
    rows=list()
    row=' '
    for word in text:
        row=row+word
        if word == '\n':
            rows.append(row)
            row=''
    palabras=list()
    for row in rows:
        palabra=nltk.word_tokenize(row)
        try: 
            #print(palabra[1])
            palabras.append(palabra[1])
        except Exception:
            pass
    #eliminar
    t=stopwords(palabras)
    
    return t

def ObtenerCriticas(x):
    criticas=list()
    for ubicacion in range(2,x):
        z=str(ubicacion)
        try:
            f=open('./corpusCriticasCine/'+z+'.review.pos')
            text=critica(f)
            criticas.append(text)
            f.close()
        except Exception:
            pass
    return criticas

def ObtenerDiccionario():
    #contextoChido={}
    f=open('./Dic/senticon.es.xml',encoding='utf-8')
    dic=f.read()
    f.close()
    #print(dic)
    rows=list()
    row=' '
    for word in dic:
        row=row+word
        if word == '\n':
            rows.append(row)
            row=''
    #print(rows[0])
    diccionario={}
    parteOracion={}
    for row in rows:
        row=nltk.word_tokenize(row)
        try:
            #print(row[4]) parte de oracion
            parteOracion[row[15]]=row[4]
            #print(row[8])  valor de pol
            #print(row[15])  palabra
            diccionario[row[15]]=row[8]
        except Exception:
            pass
    return diccionario,parteOracion

def PolaridadCriticas(criticas,diccionario):
    polCriticas=list()
    for critica in criticas:
        suma=0.0
        cuantos=0
        for w in critica:
            try:
                suma=suma+float(diccionario[w])
                cuantos=cuantos+1
            except Exception:
                pass
        #print(suma,'/',cuantos)
        try:
            polCriticas.append(suma/cuantos)
        except Exception:
            polCriticas.append(0)
            pass
    return polCriticas

def PolaridadRank(pol,rank):
    valor = arr.array('d', [0.0,0.0,0.0,0.0,0.0,0.0]) 
    #print(valor)
    i=0
    for value in pol:
        valor[int(rank[i])]+=value
        i+=1
    for i in range(1,6):
        z=str(i)
        #print(valor[i],"/",rank.count(z))
        valor[i]=valor[i]/rank.count(z)
    #print(valor)
    return valor

def tabla(x,polRank):
    print("Total de Criticas ",x)
    print("Rank           Polaridad")
    for i in range(1,6):
        print(i,"         ",polRank[i])



if __name__ == "__main__":
    #2 a 4381
    CuantosTextos=20
    rank=ObtenerRankTextos(CuantosTextos)
    #print(rank)
    criticas=ObtenerCriticas(CuantosTextos)
    #print(criticas[3])
    diccionario,parteOracion=ObtenerDiccionario()
    print(parteOracion["zorro"])
    
    #polaridad de las criticas
    polCriticas=PolaridadCriticas(criticas,diccionario)
    #print(polCriticas)
    
    #Ahora sacar todas las polaridad con respecto al rango
    polRank=PolaridadRank(polCriticas,rank)
    x=len(criticas)
    tabla(x,polRank)