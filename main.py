import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import random
from potentials import PotentialType
from infinitesquarewell import InfiniteSquareWell
from generatehamiltonian import *

def main():
    # w, v = la.eig(np.diag((1, 2)))
    # get infinite square well basis
    ISW = InfiniteSquareWell()
    # choose potential
    potential = PotentialType.linear
    V = potential.get_potential(ISW)
    # compute hamiltonian matrix from the potential 
    H = compute_hamiltonian(V, ISW)
    # diagonalize hamiltonian, getting eigenvals and eigenvecs
    vecs, vals = la.eig(H)

if __name__ == "__main__":
    main()
