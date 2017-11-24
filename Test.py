from PyWANN import WiSARD as wi

X = [ [0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 1, 1, 1, 1, 0, 0],
       [0, 0, 1, 0, 0, 0, 1, 0],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 1, 0, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1]]

y = ['class_1A','class_1C','class_1B','class_1C','class_1C','class_1B','class_1A','class_1C']

retina_length = 64
num_bits_addr = 2

w = wi.WiSARD(num_bits_addr)

# training discriminators

w.fit([X[0], X[1]], [y[0], y[1]])

X_test = [[0, 1, 0, 0, 0, 0, 0, 0]]
# w.predict(X_test)

classes_marker = 0

for i in range(1, len(X)):
    x = X[i]
    fake_y = "1"
    rez_score, rez_classes = w.predict([X[i]])
    d_size = {}
    
    for j in range(0, len(rez_score[0])):
        was_learned = False
        minimum_score = 1
        if fake_y in rez_classes[j] and rez_score[0][j] >= minimum_score:
            if rez_classes[j] in d_size:
                d_size[rez_classes[j]] += 1
            else:
                d_size[rez_classes[j]] = 1
            
            w.fit([x], [rez_classes[j]])        
            was_learned = True
    if not was_learned:
        classes_marker += 1
        new_class = "new_class_" + str(y[i]) + "_" + str(classes_marker)
        w.fit([x], [new_class])
        d_size[new_class] = 1

X_test = [[1, 0, 0, 0, 0, 0, 0, 0]]
print w.predict(X_test)
