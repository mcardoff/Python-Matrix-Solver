from infinitesquarewell import InfiniteSquareWell
import numpy as np

def mel(psil, V, psir, ISW):
    assert(isinstance(ISW, InfiniteSquareWell))
    el = sum(l*v*r for (l,v,r) in zip(psil,V,psir))
    return float(ISW.well_width * el / ISW.steps)

def compute_hamiltonian(V, ISW):
    assert(isinstance(ISW, InfiniteSquareWell))
    hamiltonian = []
    for i in range(ISW.energy_eigenvals):
        row = [] # one row of the hamiltonian matrix
        for j in range(ISW.energy_eigenvals):
            psil, psir = ISW.basis_funcs[i], ISW.basis_funcs[j]
            el = mel(psil, V, psir, ISW)
            if i == j: # diagonal elements get kinetic
                el += ISW.eigenvals[i]
            row.append(el)
        hamiltonian.append(row)

    return hamiltonian
