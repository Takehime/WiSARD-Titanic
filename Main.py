from PyWANN import WiSARD as wi
import numpy as np
import Reader as r
import sys

def generate_test_prediction(num_bits_addr):
    X = []
    y = []
    binary, result = r.get_binary_passengers('Resources/train.csv')

    for i in range(0, len(binary) - 1):
        X.append(binary[i])
        y.append(str(result[i]))

    w = wi.WiSARD(num_bits_addr)
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

    print("====================")        
    print("Done.")
    print("====================")        

def local_test(num_bits, thorough_test):
    num_bits_addr = num_bits
    successes = 0
    tries = 0
    X = []
    y = []
    binary, result = r.get_binary_passengers('Resources/train.csv')

    for i in range(0, int(0.8*len(binary))):
        X.append(binary[i])
        y.append(str(result[i]))
    w = wi.WiSARD(num_bits_addr)
    w.fit(X, y)

    for i in range(int(0.8*len(binary)), len(binary) - 1):
        tries = tries + 1
        prediction = w.predict([binary[i]])
        if str(prediction[0]) == str(result[i]):
            successes = successes + 1

    if thorough_test:
        print("====================")        
        print("n_bits: " + str(num_bits_addr) + " | Accuracy: " + ("{0:.2f}").format(successes * 100 / float(tries)) + "%")        
    else:
        print("====================")        
        print("Tries: " + str(tries))        
        print("Successes: " + str(successes))        
        print("Accuracy: " + str(successes * 100 / float(tries)) + "%")        
        print("====================")

def local_test_cross_validation(num_bits, k_folds, fold_to_test):
    num_bits_addr = num_bits
    successes = 0
    tries = 0
    X = []
    y = []
    passengers, res = r.get_passengers('Resources/train.csv')
    binary, result = r.get_binary_passengers('Resources/train.csv')

    fold_size = int(len(binary) / k_folds)

    X_0 = []
    y_0 = []
    X_1 = []
    y_1 = []

    for i in range(0, len(passengers)):
        if str(result[i]) == "True":
            X_1.append(binary[i])
            y_1.append(result[i])
        else:
            X_0.append(binary[i])
            y_0.append(result[i])

    folds_x = []
    folds_y = []

    size_fold_0 = int(len(X_0) / k_folds)
    size_fold_1 = int(len(X_1) / k_folds)
    for i in range(0, k_folds):
        fold_x = []
        fold_y = []

        for j in range(i * size_fold_0, (i+1) * size_fold_0):
            fold_x.append(X_0[j])
            fold_y.append(y_0[j])
        for j in range(i * size_fold_1, (i+1) * size_fold_1):
            fold_x.append(X_1[j])
            fold_y.append(y_1[j])

        folds_x.append(fold_x)
        folds_y.append(fold_y)

    for i in range(0, len(folds_x)):
        if i != fold_to_test:
            X.extend(folds_x[i])
            y.extend(folds_y[i])

    w = wi.WiSARD(num_bits_addr)
    w.fit(X, y)

    prediction = w.predict(folds_x[fold_to_test])
    for j in range(0, len(prediction)):
        tries = tries + 1
        if str(prediction[j]) == str(folds_y[fold_to_test][j]):
            successes = successes + 1
        
    return tries, successes

def print_usage():
    print("Usage: Main.py [T | G]")
    print("     [T]: Train with 80% of training set and test on the other 20% (num_bits_addr: 5)")
    print("     [T*]: Same as T, but tests with every num_bits_address in the range (0, 40)")
    print("     [G -n]: Train with the entirety of the training set and test on the test set, generating a file 'result.csv' in Resources folder. Using 'n' as num_bits_addr.")

def find_percentiles():
    passengers, res = r.get_passengers('Resources/train.csv')
    ages = np.array([])
    for p in passengers:
        ages = np.append(ages, p.age)
    ages.sort()

    print str(ages)
    print "00%: " + str(np.percentile(ages, 0))
    print "20%: " + str(np.percentile(ages, 20))
    print "40%: " + str(np.percentile(ages, 40))
    print "60%: " + str(np.percentile(ages, 60))
    print "80%: " + str(np.percentile(ages, 80))
    print "100%: " + str(np.percentile(ages, 100))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Wrong number of arguments.")
        print_usage()
        sys.exit(0)
    if str(sys.argv[1]) == "T":
        local_test(20, False)
    elif str(sys.argv[1]) == "C":
        k_folds = int(sys.argv[2])
        total_tries = 0
        total_successes = 0
        for i in range(0, k_folds):
            tries, successes = local_test_cross_validation(8, k_folds, i)
            total_tries = total_tries + tries
            total_successes = total_successes + successes
        print("====================")        
        print("Tries: " + str(total_tries))        
        print("Successes: " + str(total_successes))        
        print("Accuracy: " + str(total_successes * 100 / float(total_tries)) + "%")        
        print("====================")
    elif str(sys.argv[1]) == "T*":
        for i in range(1, 20):
            local_test(i, True)
    elif str(sys.argv[1]) == "G":
        if len(sys.argv) < 3:
            print_usage()
            sys.exit(0)
        else:
            generate_test_prediction(int(sys.argv[2]))
    else:
        print_usage()
        sys.exit(0)