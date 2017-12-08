from PyWANN import WiSARD as wi
import numpy as np
import Reader as r
import sys

key = None

def generate_test_prediction(num_bits_addr):
    global key

    binary, result = r.get_binary_passengers('Resources/train.csv', key)

    X = []
    y = []
    w = wi.WiSARD(key[0])
    for i in range(0, len(binary) - 1):
        X.append(binary[i])
        y.append(str(result[i]))
    w.fit(X, y)

    binary, result = r.get_binary_passengers('Resources/test.csv', key)
    passengers, res = r.get_passengers('Resources/test.csv')

    output = "PassengerId,Survived\n"
    for i in range(0, len(binary)):
        prediction = str(w.predict([binary[i]])[0])
        if prediction == "True":
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
    global key
    num_bits_addr = key[0]
    successes = 0
    tries = 0
    X = []
    y = []
    binary, result = r.get_binary_passengers('Resources/train.csv', key)

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
    global key
    num_bits_addr = key[0]
    successes = 0
    tries = 0
    X = []
    y = []
    passengers, res = r.get_passengers('Resources/train.csv')
    binary, result = r.get_binary_passengers('Resources/train.csv', key)

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

    w = wi.WiSARD(key[0])
    w.fit(X, y)

    output = {"pT_cF": 0, "pT_cT": 0, "pF_cF": 0, "pF_cT": 0}

    prediction = w.predict(folds_x[fold_to_test])
    for j in range(0, len(prediction)):
        tries = tries + 1
        if str(prediction[j]) == "True" and str(folds_y[fold_to_test][j]) == "True":
            output["pT_cT"] += 1
        elif str(prediction[j]) == "True" and str(folds_y[fold_to_test][j]) == "False":
            output["pT_cF"] += 1
        elif str(prediction[j]) == "False" and str(folds_y[fold_to_test][j]) == "False":
            output["pF_cF"] += 1
        elif str(prediction[j]) == "False" and str(folds_y[fold_to_test][j]) == "True":
            output["pF_cT"] += 1

        if str(prediction[j]) == str(folds_y[fold_to_test][j]):
            successes = successes + 1
        
    return tries, successes, output

def print_usage():
    print("Usage: Main.py [T | G]")
    print("     [T (key)]: Train with 80% of training set and test on the other 20%")
    print("     [T* (key*)]: Same as T, but tests with every num_bits_address in the range (0, 20)")
    print("     [G (key)]: Train with the entirety of the training set and test on the test set, generating a file 'result.csv' in Resources folder.")
    print("     [C (num_of_folds) (key)]: Cross-Validation with the given number of folds.")
    print("     Key format: [num_bits_addr, (0, 1), (0, 1), (0, 6), (0, 6), (0, 1), (0, 3), (0, 3), (0, 3)] ")    
    print("     Key* format: [(0, 1), (0, 1), (0, 6), (0, 6), (0, 1), (0, 3), (0, 3), (0, 3)] ")    

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
    elif str(sys.argv[1]) == "T":
        if len(sys.argv) < 11:
            print("Wrong number of arguments.")
            print_usage()
            sys.exit(0)
        else:
            k1 = int(sys.argv[2])
            k2 = int(sys.argv[3])
            k3 = int(sys.argv[4])
            k4 = int(sys.argv[5])
            k5 = int(sys.argv[6])
            k6 = int(sys.argv[7])
            k7 = int(sys.argv[8])
            k8 = int(sys.argv[9])
            k9 = int(sys.argv[10])
            key = [k1, k2, k3, k4, k5, k6, k7, k8, k9]
            local_test(k1, False)
    elif str(sys.argv[1]) == "C":
        if len(sys.argv) < 12:
            print("Wrong number of arguments.")
            print_usage()
            sys.exit(0)
        else:
            k_folds = int(sys.argv[2])
            k1 = int(sys.argv[3])
            k2 = int(sys.argv[4])
            k3 = int(sys.argv[5])
            k4 = int(sys.argv[6])
            k5 = int(sys.argv[7])
            k6 = int(sys.argv[8])
            k7 = int(sys.argv[9])
            k8 = int(sys.argv[10])
            k9 = int(sys.argv[11])
            key = [k1, k2, k3, k4, k5, k6, k7, k8, k9]            
            total_tries = 0
            total_successes = 0
            output = {"pT_cF": 0, "pT_cT": 0, "pF_cF": 0, "pF_cT": 0}
            for i in range(0, k_folds):
                tries, successes, op = local_test_cross_validation(8, k_folds, i)
                total_tries = total_tries + tries
                total_successes = total_successes + successes
                output["pT_cT"] += op["pT_cT"]
                output["pF_cF"] += op["pF_cF"]
                output["pF_cT"] += op["pF_cT"]
                output["pT_cF"] += op["pT_cF"]

        print("====================")        
        print("Tries: " + str(total_tries))        
        print("Successes: " + str(total_successes))        
        print("Accuracy: " + str(total_successes * 100 / float(total_tries)) + "%")
        print output        
        print("Dos nao-sobreviventes, " + str((output["pF_cF"])  * 100 / float(output["pT_cF"] + output["pF_cF"])) + "% foram corretamente classificados")
        print("Dos sobreviventes, " + str((output["pT_cT"])  * 100 / float(output["pT_cT"] + output["pF_cT"])) + "% foram corretamente classificados")
        print("====================")
    elif str(sys.argv[1]) == "T*":
        if len(sys.argv) < 10:
            print("Wrong number of arguments.")
            print_usage()
            sys.exit(0)
        else:
            k1 = int(sys.argv[2])
            k2 = int(sys.argv[3])
            k3 = int(sys.argv[4])
            k4 = int(sys.argv[5])
            k5 = int(sys.argv[6])
            k6 = int(sys.argv[7])
            k7 = int(sys.argv[8])
            k8 = int(sys.argv[9])
        for i in range(1, 20):
            key = [i, k1, k2, k3, k4, k5, k6, k7, k8]
            local_test(i, True)
    elif str(sys.argv[1]) == "G":
        if len(sys.argv) < 11:
            print("Wrong number of arguments.")
            print_usage()
            sys.exit(0)
        else:
            k1 = int(sys.argv[2])
            k2 = int(sys.argv[3])
            k3 = int(sys.argv[4])
            k4 = int(sys.argv[5])
            k5 = int(sys.argv[6])
            k6 = int(sys.argv[7])
            k7 = int(sys.argv[8])
            k8 = int(sys.argv[9])
            k9 = int(sys.argv[10])
            key = [k1, k2, k3, k4, k5, k6, k7, k8, k9]
            generate_test_prediction(k1)
    else:
        print_usage()
        sys.exit(0)