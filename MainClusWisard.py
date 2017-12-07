from PyWANN import WiSARD as wi
import numpy as np
import Reader as r
import sys

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
                w.fit([x], [str(rez_classes[j])])        
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

    # print "===================="
    # print "Generated #" + str(classes_marker) + " new classes."
    # print "Successes: " + str(successes) + " || Tries: " + str(tries)
    # print "Accuracy: " + str(("{0:.2f}").format(successes * 100 / float(tries)) + "%") + "%"

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

    # print("====================")        
    # print("Done.")
    # print("====================")  

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Wrong number of arguments.")
    elif str(sys.argv[1]) == "CW":
        cluswisard(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
    else:
        print("     [CW (n) (g) (s)]: ClusWiSARD test. n: num_bits_addr; g: growth coefficient; s: minimum score")