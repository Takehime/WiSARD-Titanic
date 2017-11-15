import numpy as np
import sys

def hamming2(s1, s2):
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def generate_binarization(n, x):
    t = "0" * n
    s = [t]
    x = x - 1
    if n > 0:
        t = "1" * n
        s.append(t)
        x = x - 1
    d = n/2
    while x > 0:
        for v in range(1, pow(2, n) - 2):
            w = bin(v)[2:].zfill(n)
            d2 = hamming2(w, s[0])
            for i in s:
                aux = hamming2(w, i)
                if aux < d2:
                    d2 = aux
            if d == d2:
                s.append(w)
                x = x - 1
                if x == 0:
                    return s
        x = x - 1
    return []

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Wrong number of arguments.")
        sys.exit(0)
    x = int(sys.argv[1])
    n = int(sys.argv[2])
    print(generate_binarization(x, n))