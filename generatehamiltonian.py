"""Generate the hamiltonian given a basis and potential."""
from infinitesquarewell import InfiniteSquareWell
import numpy as np


def mel(psil, V, psir, ISW):
    """Compute matrix element using average value theorem."""
    assert(isinstance(ISW, InfiniteSquareWell))
    # discrete inner product: < left | V | right >
    mel_array = np.fromiter((l*v*r for (l, v, r) in zip(psil, V, psir)), float)
    el = np.mean(mel_array)
    # readjust for avg val thm
    return float(ISW.well_width * el)


def compute_hamiltonian(V, ISW):
    """Compute discretized hamiltonian."""
    assert(isinstance(ISW, InfiniteSquareWell))
    hamiltonian = []
    for i in range(ISW.energy_eigenvals):
        row = []  # one row of the hamiltonian matrix
        for j in range(ISW.energy_eigenvals):
            psil, psir = ISW.basis_funcs[i], ISW.basis_funcs[j]
            el = mel(psil, V, psir, ISW)
            if i == j:  # diagonal elements get kinetic term
                el += ISW.eigenvals[i]
            row.append(el)
            el = 0.0
        hamiltonian.append(row)
    return hamiltonian
