from PyWANN import WiSARD as wi
import numpy as np
import Reader as r

num_bits_addr = 5

successes = 0
tries = 0
X = []
y = []
binary, result = r.get_binary_passengers()

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
