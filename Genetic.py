import Main as m
from random import randint
import numpy as np

gen = [1, 20, 28, 38, 80]
best_accuracy = 0
best_gen = list(gen)
for i in range(0, 500):
    while True:
        random_index = randint(0, 4)
        modifier = randint(-5, 5)
        valid = True
        gen = list(best_gen)

        if random_index > 0 and (gen[random_index] + modifier <= gen[random_index - 1]):
            valid = False
        if random_index < len(gen) - 1 and (gen[random_index] + modifier >= gen[random_index + 1]):
            valid = False
        if gen[random_index] + modifier < 0:
            valid = False
            
        if valid == True:
            gen[random_index] = gen[random_index] + modifier
            break

    accuracy = m.local_test(8, False, gen)
    print "Gen: "+ str(gen)
    print "Best Gen: "+ str(best_gen)
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_gen = list(gen)
        
print "Best accuracy: " + str(best_accuracy)
print "Best gen: " + str(best_gen)