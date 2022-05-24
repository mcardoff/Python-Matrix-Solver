# libraries
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
# files
from potentials import PotentialType
from infinitesquarewell import InfiniteSquareWell
from generatehamiltonian import *

def main():
    # w, v = la.eig(np.diag((1, 2)))
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
    for vec in vecs:
        lin_combination = []
        first_run = True
        for (i,val) in enumerate(vec):
            if first_run:
                # need to build up list
                for (j,basis_val) in enumerate(ISW.basis_funcs[i]):
                    lin_combination.append(vec[i] * ISW.basis_funcs[i][j])
                first_run = False
            else:
                for (j,basis_val) in enumerate(ISW.basis_funcs[i]):
                    lin_combination[j] += vec[i] * basis_val

        # one linear combination is built
        newfuncs.append(lin_combination)

    # for func in newfuncs:
    plt.plot(ISW.xvals, newfuncs[0])

    plt.show()

if __name__ == "__main__":
    main()
