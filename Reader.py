#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

class Passenger:
    age = -1
    t_class = 0
    surname = "SURNAME"
    name = "NAME"
    gender = 0
    sibsp = 0
    parch = 0
    ticket = 0
    fare = 0.0
    cabin = ""
    port = ""
    survived = False
    
    def __init__(self, p_id, t_class, age, surname, name, gender, 
        sibsp, parch, ticket, fare, cabin, port, survived):
        self.p_id = p_id
        self.t_class = t_class
        self.age = age
        self.surname = surname
        self.name = name
        self.gender = gender
        self.sibsp = int(sibsp)
        self.parch = int(parch)
        self.ticket = ticket
        self.fare = fare
        self.cabin = cabin
        self.port = port
        self.survived = survived

    def __str__(self):
        string = ""
        string = string + "[ID: " + str(self.p_id)
        string = string + "; Age: " + str(self.age)
        string = string + "; Class: " + str(self.t_class)
        string = string + "; Name: " + str(self.name)
        string = string + "; Surname: " + str(self.surname)
        string = string + "; Gender: " + str(self.gender)
        string = string + "; Siblings/Spouses: " + str(self.sibsp)
        string = string + "; Parents/Children: " + str(self.parch)
        string = string + "; Ticket #: " + str(self.ticket)
        string = string + "; Fare: " + str(self.fare)
        string = string + "; Cabin: " + str(self.cabin)
        string = string + "; Port: " + str(self.port) + "]"
        return string

    def binarize(self, key):
        string = ""

        #Porto de Embarque
        if key[1] == 1:
            if self.port == "Q":
                string = string + "000011"
            elif self.port == "C":
                string = string + "001100"
            else: #1st class
                string = string + "110000"

        #Gênero
        if key[2] == 1:
            if self.gender == "male":
                string = string + "000000"
            else:
                string = string + "111111"
        
        #Idade
        if key[3] == 1: #acumulado, absoluto
            if self.age < 10:
                string = string + "000001"
            elif self.age < 20:
                string = string + "000011"
            elif self.age < 30:
                string = string + "000111"
            elif self.age < 40:
                string = string + "001111"
            else:
                string = string + "011111"
        elif key[3] == 2: #acumulado, genetico
            if self.age < 1:
                string = string + "000001"
            elif self.age < 5:
                string = string + "000011"
            elif self.age < 28:
                string = string + "000111"
            elif self.age < 30:
                string = string + "001111"
            else:
                string = string + "011111"
        elif key[3] == 3: #acumulado, percentil
            if self.age < 5:
                string = string + "000001"
            elif self.age < 20:
                string = string + "000011"
            elif self.age < 28:
                string = string + "000111"
            elif self.age < 38:
                string = string + "001111"
            else:
                string = string + "011111"
        elif key[3] == 4: #discriminado, absoluto
            if self.age < 10:
                string = string + "000000"
            elif self.age < 20:
                string = string + "000111"
            elif self.age < 30:
                string = string + "011001"
            elif self.age < 40:
                string = string + "101010"
            else:
                string = string + "110100"
        elif key[3] == 5: #discriminado, genetico
            if self.age < 1:
                string = string + "000000"
            elif self.age < 5:
                string = string + "000111"
            elif self.age < 28:
                string = string + "011001"
            elif self.age < 30:
                string = string + "101010"
            else:
                string = string + "110100"
        elif key[3] == 6: #discriminado, percentil
            if self.age < 10:
                string = string + "000000"
            elif self.age < 20:
                string = string + "000111"
            elif self.age < 30:
                string = string + "011001"
            elif self.age < 40:
                string = string + "101010"
            else:
                string = string + "110100"

        #Fare
        if key[4] == 1: #acumulado, absoluto
            if self.fare < 10:
                string = string + "000001"
            elif self.fare < 20:
                string = string + "000011"
            elif self.fare < 50:
                string = string + "000111"
            elif self.fare < 100:
                string = string + "001111"
            else:
                string = string + "011111"
        elif key[4] == 2: #acumulado, genetico
            if self.fare < 1:
                string = string + "000001"
            elif self.fare < 7:
                string = string + "000011"
            elif self.fare < 15:
                string = string + "000111"
            elif self.fare < 51:
                string = string + "001111"
            else:
                string = string + "011111"
        elif key[4] == 3: #acumulado, percentil
            if self.fare < 7:
                string = string + "000001"
            elif self.fare < 10:
                string = string + "000011"
            elif self.fare < 21:
                string = string + "000111"
            elif self.fare < 39:
                string = string + "001111"
            else:
                string = string + "011111"
        elif key[4] == 4: #discriminado, absoluto
            if self.fare < 10:
                string = string + "000000"
            elif self.fare < 20:
                string = string + "000111"
            elif self.fare < 50:
                string = string + "011001"
            elif self.fare < 100:
                string = string + "101010"
            else:
                string = string + "110100"
        elif key[4] == 5: #discriminado, genetico
            if self.fare < 1:
                string = string + "000000"
            elif self.fare < 7:
                string = string + "000111"
            elif self.fare < 15:
                string = string + "011001"
            elif self.fare < 51:
                string = string + "101010"
            else:
                string = string + "110100"
        elif key[4] == 6: #discriminado, percentil
            if self.fare < 7:
                string = string + "000000"
            elif self.fare < 10:
                string = string + "000111"
            elif self.fare < 21:
                string = string + "011001"
            elif self.fare < 39:
                string = string + "101010"
            else:
                string = string + "110100"
        
        #Cabine
        if key[5] == 1:
            if self.cabin == "":
                string = string + "111111"
            else:
                string = string + "000000"
        
        #Sibsp
        if key[6] == 1: #acumulado, absoluto
            if self.sibsp == 0:
                string = string + "000000"
            elif self.sibsp < 3:
                string = string + "000111"
            else:
                string = string + "111111"
        elif key[6] == 2: #discriminado, absoluto
            if self.sibsp == 0:
                string = string + "000000"
            elif self.sibsp < 3:
                string = string + "000111"
            else:
                string = string + "111000"
        elif key[6] == 3: #binario
            if self.sibsp == 0:
                string = string + "000000"
            else:
                string = string + "111111"

        #Parch
        if key[7] == 1: #acumulado, absoluto
            if self.parch == 0:
                string = string + "000000"
            elif self.parch < 3:
                string = string + "000111"
            else:
                string = string + "111111"
        elif key[7] == 2: #discriminado, absoluto
            if self.parch == 0:
                string = string + "000000"
            elif self.parch < 3:
                string = string + "000111"
            else:
                string = string + "111000"
        elif key[7] == 3: #binario
            if self.parch == 0:
                string = string + "000000"
            else:
                string = string + "111111"

        #Classe
        if key[8] == 1: #acumulado, absoluto
            if self.t_class == "3":
                string = string + "000000"
            elif self.t_class == "2":
                string = string + "000111"
            else: #1st class
                string = string + "111111"
        elif key[8] == 2: #discriminado, absoluto
            if self.t_class == "3":
                string = string + "000000"
            elif self.t_class == "2":
                string = string + "000111"
            else: #1st class
                string = string + "111000"
        elif key[8] == 3: #binario
            if self.t_class != "1":
                string = string + "000000"
            else: #1st class
                string = string + "111111"

        return string, self.survived

def get_data(filename):
    people = []
    
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        skip_first = True
        for row in reader:
            if skip_first:
                skip_first = False
                continue

            i = 0
            p_id = row[i]

            survived = None
            if "train" in filename:
                i = i + 1
                if row[i] == "1":
                    survived = True
                else:
                    survived = False

            i = i + 1
            t_class = row[i]

            i = i + 1
            name = row[i]

            i = i + 1
            surname = row[i]

            i = i + 1
            gender = row[i]

            i = i + 1
            age = row[i]

            if "." in age:
                age = int(age.split(".")[0])
            elif age == "":
                age = 0
            else:
                age = int(age)

            i = i + 1
            sibsp = row[i]

            i = i + 1
            parch = row[i]

            i = i + 1
            ticket = row[i]

            i = i + 1
            fare = row[i]
            if "." in fare:
                fare = int(fare.split(".")[0])
            elif fare == "":
                fare = 0
            else:
                fare = int(fare)

            i = i + 1
            cabin = row[i]

            i = i + 1
            port = row[i]

            people.append(Passenger(
                p_id,
                t_class,
                age,
                surname,
                name,
                gender,
                sibsp,
                parch,
                ticket,
                fare,
                cabin,
                port,
                survived,
            ))
    
    return people

def get_binary_passengers(filename, key=[17, 1, 1, 6, 6, 1, 3, 2, 3]):
    output = []
    result = []
    data = get_data(filename)
    for p in data:
        string, survived = p.binarize(key)
        output.append(binary_string_to_int_array(string))
        result.append(survived)
    return output, result

def get_passengers(filename):
    output = []
    result = []
    data = get_data(filename)
    for p in data:
        output.append(p)
        result.append(str(p.survived))
    return output, result

def binary_string_to_int_array(string):
    output = []
    for s in string:
        if s == "0":
            output.append(0)
        else:
            output.append(1)
    return output

def print_passengers(filename):
    for p in get_data(filename):
        print(p.binarize())

if __name__ == "__main__":
    print_passengers('Resources/test.csv')