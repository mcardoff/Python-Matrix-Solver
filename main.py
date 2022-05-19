import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import random

def main():
    # insert code here
    w, v = la.eig(np.diag((1, 2)))
    print(w[1] * v[1] == np.matmul(np.diag((1, 2)), v[1]))
    

if __name__ == "__main__":
    main()
