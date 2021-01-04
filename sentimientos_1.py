# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:45:37 2020
@author: Brandon
"""

import nltk 
import numpy as np
from nltk.corpus import wordnet
import mord as m
from sklearn.feature_extraction.text import CountVectorizer

def get_wordnet(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def get_vector(msg, voc):
    vector = list()
    #frecuencia
    for w in voc:
        vector.append(msg.count(w))
    #probabilidad
    nsum = np.sum(vector)
    for i in range(0,len(vector)):
        vector[i] = vector[i]/nsum
    return vector

def quitarCaracter(cadena,letra):
	return cadena.replace(letra," ")

def eliminarEtiquetas_ObtenerRank(f):
    text=f.read().lower()
    numero=text.find('rank="')
    numero=numero+6
    numero=text[numero]
    text=quitarCaracter(text,"<review")
    text=quitarCaracter(text,"</review>")
    text=quitarCaracter(text,"<body>")
    text=quitarCaracter(text,"</body>")
    text=quitarCaracter(text,"<review")
    text=quitarCaracter(text,"\n")
    text=quitarCaracter(text,"\t")
    text=quitarCaracter(text,"author=")
    text=quitarCaracter(text,"source=")
    text=quitarCaracter(text,".")
    text=quitarCaracter(text,",")
    text=quitarCaracter(text,"(")
    text=quitarCaracter(text,")")
    for i in range(0,10):
        text=quitarCaracter(text,str(i))
    return text,numero

def splt_y(matriz):
    t=matriz.T
    y=t[-1]
    t=t[0:-1]
    return t.T, np.asarray(y).T

if __name__ == "__main__":
    #2 a 4381
    #ubicacion="2"
    criticas=list()
    rank=list()
    for ubicacion in range(2,11):
        z=str(ubicacion)
        #print(z)
        try:
            f=open('./corpusCriticasCine/'+z+'.xml')
            #leo y paso a minusculas todo
            text,numero=eliminarEtiquetas_ObtenerRank(f)
            rank.append(numero)
            text=nltk.word_tokenize(text)
            text = " ".join(text)
            criticas.append(text)
            f.close()
        except Exception as e:
            print("archivo : ",e)
            pass
    print(type(text))
    print("Total de criticas: ",len(criticas))
    #print(criticas[7])
    #print(rank)
    
    tag_criticas = list()
    for msg in criticas:
        aux_msg=list()
        aux = nltk.pos_tag(msg)
        for token in aux:
            aux_msg.append(list(token))
        tag_criticas.append(aux_msg)
    
    lema_criticas=list()
    lemmatizer=nltk.WordNetLemmatizer()
    for msg in tag_criticas:
        aux_msg=list()
        for token in msg:
            if(get_wordnet(token[1])!=''):
                aux_msg.append(lemmatizer.lemmatize(token[0],get_wordnet(token[1])))
            else:
                aux_msg.append(lemmatizer.lemmatize(token[0]))
        lema_criticas.append(aux_msg)
    
    vocabulary = list()
    for msg in lema_criticas:
        for token in msg:
            vocabulary.append(token)
    vocabulary=list(set(vocabulary))
    vocabulary.sort()
    print("vocabulario: ",len(vocabulary))
    
    vectors=list()
    for critica in lema_criticas:
        vectors.append(get_vector(critica, vocabulary))
    vectores=np.array(vectors)
    #print(vectores[:3])
    #vectores es x and y es rank
    #--------------------------------prueba---------------
    y=np.array(rank)
    #anexo su y al final de cada vector, y adjunto un grupo de 1's al inicio
    vectores=np.c_[vectores, y.T]
    #vectores=np.c_[np.ones((len(vectores),1)),vectores]
    
    #vectores=np.c_[vectores,y]
    #ramdon
    np.random.shuffle(vectores)
    split=int(len(vectores)*.7)
    
    #separamos nuestra matriz de su 'y' y cortamos la matriz principal hasta el split
    x_train, y_train=splt_y(vectores[0:split])
    test, y_test=splt_y(vectores[split:])
    
    for x in x_train:
        z=x
    
    #y_train=y_train.astype(np.float)
    #x_train=x_train.astype(np.float)
    
    print(x_train)
    print(len(x_train),type(x_train))
    print(y_train)
    print(len(y_train),type(y_train))
    print(type(z))
    for w in z:
        rr=w
    print(type(rr))
    '''
    vectorizer=CountVectorizer()
    x=vectorizer.fit_transform(criticas).toarray()
    x=np.c_[x,rank]
    np.random.shuffle(x)
    split=int(len(x)*.7)
    
    
    x_train, y_train=splt_y(x[0:split])
    test, y_test=splt_y(x[split:])
    '''
    c = m.LogisticIT()
    #c.fit(x_train,y_train)
    #c.predict(np.array(x_train[0]))
    