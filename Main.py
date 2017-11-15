from PyWANN import WiSARD as wi
import numpy as np
import Reader as r
import sys

def train_and_generate_test_prediction():
    num_bits_addr = 5
    successes = 0
    tries = 0
    X = []
    y = []
    binary, result = r.get_binary_passengers('Resources/train.csv')

    for i in range(0, len(binary) - 1):
        X.append(binary[i])
        y.append(str(result[i]))

    w = wi.WiSARD(num_bits_addr, False)
    w.fit(X, y)

    binary, result = r.get_binary_passengers('Resources/test.csv')
    passengers, res = r.get_passengers('Resources/test.csv')

    output = "PassengerId,Survived\n"
    for i in range(0, len(binary)):
        prediction = w.predict([binary[i]])
        if str(prediction[0]) == "True":
            output = output + str(passengers[i].p_id) + "," + "1\n"
        else:
            output = output + str(passengers[i].p_id) + "," + "0\n"

    f = open('Resources/result.csv','w')
    f.write(output)
    f.close()

def train_and_local_test():
    num_bits_addr = 5
    successes = 0
    tries = 0
    X = []
    y = []
    binary, result = r.get_binary_passengers('Resources/train.csv')

    order = []
    for i in range(0, len(binary) - 1):
        order.append(i)

    np.random.shuffle(order)

    for i in range(0, int(0.8*len(binary))):
        X.append(binary[order[i]])
        y.append(str(result[order[i]]))
    w = wi.WiSARD(num_bits_addr, False)
    w.fit(X, y)

    for i in range(int(0.8*len(binary)), len(binary) - 1):
        tries = tries + 1
        prediction = w.predict([binary[i]])
        if str(prediction[0]) == str(result[i]):
            successes = successes + 1

    print("====================")        
    print("Tries: " + str(tries))        
    print("Successes: " + str(successes))        
    print("Accuracy: " + str(successes * 100 / tries))        
    print("====================")

def print_usage():
    print("Usage: Main.py [T | G]")
    print("     [T]: Train with 80\%\ of training set and test on the other 20%")
    print("     [G]: Train with the entirety of the training set and test on the test set, generating a file 'result.csv' in Resources folder.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Wrong number of arguments.")
        print_usage()
        sys.exit(0)
    if str(sys.argv[1]) == "T":
        train_and_local_test()
    elif str(sys.argv[1]) == "G":
        train_and_generate_test_prediction()
    else:
        print_usage()
        sys.exit(0)