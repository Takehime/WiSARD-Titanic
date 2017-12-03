#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyWANN import WiSARD as wi
import Reader as r
import numpy as np
import sys

def run(key):
    num_bits_addr = key[0]
    successes = 0
    tries = 0
    X = []
    y = []
    X_test = []
    y_test = []
    binary, result = r.get_binary_passengers('Resources/train.csv', key)

    for i in range(0, int(0.8*len(binary))):
        X.append(binary[i])
        y.append(str(result[i]))

    for i in range(int(0.8*len(binary)), len(binary)):
        X_test.append(binary[i])
        y_test.append(str(result[i]))

    w = wi.WiSARD(num_bits_addr)
    w.fit(X, y)
    prediction = w.predict(X_test)

    for i in range(0, len(X_test)):
        if str(y_test[i]) == str(prediction[i]):
            successes = successes + 1

    return ("{0:.2f}").format(successes * 100 / float(len(X_test)))

max_acc = 0
max_key = []

string = ""
for porto in range(1, -1, -1):
    for genero in range(1, -1, -1):
        for idade in range(6, -1, -1):
            for fare in range(6, -1, -1):
                for cabine in range(1, -1, -1):
                    for sibsp in range(3, -1, -1):
                        for parch in range(3, -1, -1):
                            for classe in range(3, -1, -1):
                                for nba in range(1, 20):
                                    key = [nba, porto, genero, idade, fare, cabine, sibsp, parch, classe]
                                    print key
                                    acc = run(key)
                                    print acc
                                    aux = "===========================\nNUM_BITS_ADDR: " + str(nba) + " || ACCURACY: " + str(acc) + "\nPorto: " + str(porto) + "\nGênero: " + str(genero) + "\nIdade: " + str(idade) + "\nFare: " + str(fare) + "\nCabine: " + str(cabine) + "\nSibsp: " + str(sibsp) + "\nParch: " + str(parch) + "\nClasse: " + str(classe) +"\nFull Key: " + str(key)
                                    string += aux
                                    if acc > max_acc:
                                        print "New best: " + str(acc) + ", Old best: " + str(max_acc) + ", Key: " + str(key)
                                        max_acc = acc
                                        max_key = key

f = open('Resources/full_results.csv','w')
f.write(string)
f.close()