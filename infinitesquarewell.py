import numpy as np
import matplotlib.pyplot as plt

def main():
    # tests if you can generate a ISW object, plots basis 
    ISW = InfiniteSquareWell()
    for func in ISW.basis_funcs:
        plt.plot(ISW.xvals, func)
    plt.show()

class InfiniteSquareWell:
    def __init__(self, well_width=1.0, steps=200,
                 energy_eigenvals=5, hbar=1.0, mass=1.0):
        # values set by user
        self.well_width = well_width
        self.steps = steps
        self.energy_eigenvals = energy_eigenvals
        self.step_size = well_width / steps

        # used in generation
        self.basis_funcs = []
        self.eigenvals = []
        self.xvals = []

        # Set to 1 because we can
        self.hbar = hbar
        self.mass = mass

        # do everything in initializer
        self.generate_basis_funcs()

    def generate_basis_funcs(self):
        # know how to generate the infinite square well basis, base everything off that

        # Quick pneumonics
        PI = np.pi
        L = self.well_width
        
        # all wavefunction values are in the same box
        self.xvals = np.linspace(0, L, self.steps+1)
        # ISW eigenvalues are natural numbers
        for n in range(1,self.energy_eigenvals+1):
            # analytic formulae
            energy = (n * self.hbar * PI / L) ** 2 / (2.0*self.mass)

            eigenfunc = []
            for x in self.xvals:
                eigenfunc.append(np.sqrt(2/L)*np.sin(n*PI*x/L))

            # Add to lists
            self.eigenvals.append(energy)
            self.basis_funcs.append(eigenfunc)

if __name__ == "__main__":
    main()
