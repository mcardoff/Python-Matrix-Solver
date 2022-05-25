# libraries
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
# files
from potentials import PotentialType
from infinitesquarewell import InfiniteSquareWell
from generatehamiltonian import *

def main():
    # get infinite square well basis
    ISW = InfiniteSquareWell()
    # choose potential
    potential = PotentialType.linear
    V = potential.get_potential(ISW,100.0)
    # compute hamiltonian matrix from the potential 
    H = compute_hamiltonian(V, ISW)
    # diagonalize hamiltonian, getting eigenvals and eigenvecs
    vals, vecs = la.eig(H)
    # new functions are the eigenvectors time the eigenfunctions of ISW
    newfuncs = []
    for col in np.transpose(vecs):
        lin_combination = np.zeros(len(ISW.basis_funcs[0]))
        for (i,val) in enumerate(col):
            lin_combination += np.multiply(ISW.basis_funcs[i],val)
        newfuncs.append(lin_combination)

    x = ISW.xvals
    plt.xlim(0, 1)
    plt.ylim(-2, 2)
    plt.plot(x,V,'black')
    for func in newfuncs:
        plt.plot(x, func)

    plt.show()

if __name__ == "__main__":
    main()
