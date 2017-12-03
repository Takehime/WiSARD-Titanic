from PyWANN import WiSARD as wi
import numpy as np
import Reader as r
import sys

key = [17, 1, 1, 6, 6, 1, 3, 2, 3]

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
        prediction = str(w.predict([binary[i]])[2][0])
        if str(prediction) == "True":
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
        prediction = w.predict([binary[i]])[2]
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

def cluswisard(nba, growth, score):
    successes = 0
    tries = 0
    binary, result = r.get_binary_passengers('Resources/train.csv')
    passengers, result_2 = r.get_passengers('Resources/train.csv')

    w = wi.WiSARD(num_bits_addr = nba)
    w.fit([binary[0], binary[1]], [str(result[0]), str(result[1])])

    classes_marker = 0
    gamma = 100
    d_size = {str(result[0]): 1, str(result[1]): 1}

    for i in range(1, int(0.8*(len(binary)))):
        # print "Passenger #" + str(passengers[i].p_id)
        x = binary[i]
        fake_y = result[i]
        rez_score, rez_classes, f_result = w.predict([binary[i]])
        result_sum = np.sum(rez_score, dtype=np.float32)
        rez_proba = np.array(rez_score)/result_sum

        was_learned = False
        for j in range(0, len(rez_score[0])):
            gamma = float(growth)
            if str(rez_classes[j]) not in d_size:
                size = 0
            else:
                size = d_size[str(rez_classes[j])]

            minimum_score = min(1, score + size / gamma)

            # print "y: " + str(fake_y)
            # print "rez_classes[j]: " + str(rez_classes[j])
            # print "rez_proba[0][j]: " + str(rez_proba[0][j])
            # print "minimum_score:" + str(minimum_score)
            # print "============"

            if str(fake_y) in str(rez_classes[j]) and rez_proba[0][j] >= minimum_score:
                if str(rez_classes[j]) in d_size:
                    d_size[str(rez_classes[j])] += 1
                else:
                    d_size[str(rez_classes[j])] = 1
                
                # print "w.fit([x], [rez_classes[j]]). || [x] = " + str([x]) + "; || [rez_classes[j]] = " + str([rez_classes[j]])
                w.fit_one([x], [str(rez_classes[j])])        
                was_learned = True
                break
        if not was_learned:
            # print ">> New class learned!"
            # print passengers[i]
            classes_marker += 1
            new_class = str(result[i]) + "_" + str(classes_marker)
            w.fit([x], [new_class])
            d_size[new_class] = 1
            # print d_size

    tries = 0
    successes = 0

    for i in range(int(0.8*(len(binary))), len(binary)):
        score, classes, result = w.predict([binary[i]])
        # prediction = w.predict([binary[i]])
        tries += 1
        if "True" in str(result[0]) and "True" in str(result_2[i]):
            successes += 1
        if "False" in str(result[0]) and "False" in str(result_2[i]):
            successes += 1

    print "===================="
    print "Generated #" + str(classes_marker) + " new classes."
    print "Successes: " + str(successes) + " || Tries: " + str(tries)
    print "Accuracy: " + str(("{0:.2f}").format(successes * 100 / float(tries)) + "%") + "%"

    binary, result = r.get_binary_passengers('Resources/test.csv')
    passengers, res = r.get_passengers('Resources/test.csv')

    output = "PassengerId,Survived\n"
    for i in range(0, len(binary)):
        score, classes, result = w.predict([binary[i]])
        # prediction = w.predict([binary[i]])
        d_size[str(result[0])] += 1
        if "True" in str(result[0]):
            output = output + str(passengers[i].p_id) + "," + "1\n"
        else:
            output = output + str(passengers[i].p_id) + "," + "0\n"

    f = open('Resources/result.csv','w')
    f.write(output)
    f.close()
    print d_size

    print("====================")        
    print("Done.")
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

    prediction = w.predict(folds_x[fold_to_test])[2]
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
    print("     [T]: Train with 80% of training set and test on the other 20% (num_bits_addr: 5)")
    print("     [T*]: Same as T, but tests with every num_bits_address in the range (0, 40)")
    print("     [G (n)]: Train with the entirety of the training set and test on the test set, generating a file 'result.csv' in Resources folder. Using 'n' as num_bits_addr.")
    print("     [CW (n) (g) (s)]: ClusWiSARD test. n: num_bits_addr; g: growth coefficient; s: minimum score")

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
        local_test(int(sys.argv[2]), False)
    elif str(sys.argv[1]) == "CW":
        cluswisard(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
    elif str(sys.argv[1]) == "C":
        k_folds = int(sys.argv[2])
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