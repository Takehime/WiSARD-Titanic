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
        self.sibsp = sibsp
        self.parch = parch
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

    def binarize(self):
        string = ""
        if self.age < 10:
            string = string + "000000"
        elif self.age < 20:
            string = string + "111111"
        elif self.age < 30:
            string = string + "000111"
        elif self.age < 40:
            string = string + "011001"
        elif self.age < 50:
            string = string + "101010"
        else: #if self.age < 80:
            string = string + "110100"
            
        if self.gender == "male":
            string = string + "000000"
        else:
            string = string + "111111"

        if self.t_class == "1":
            string = string + "000000"
        elif self.t_class == "2":
            string = string + "111111"
        else: #if self.t_class == "2":
            string = string + "000111"

        if self.port == "C":
            string = string + "000000"
        elif self.port == "Q":
            string = string + "111111"
        else: #if self.port == "S":
            string = string + "000111"

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

def get_binary_passengers(filename):
    output = []
    result = []
    data = get_data(filename)
    for p in data:
        string, survived = p.binarize()
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