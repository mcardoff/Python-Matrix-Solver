import numpy as np

def main():
    # tests if you can generate a ISW object
    ISW = InfiniteSquareWell()

class InfiniteSquareWell:
    def __init__(self, well_width=1.0, steps=200,
                 energy_eigenvals=5, hbar=1.0, mass=1.0):
        self.well_width = well_width
        self.steps = steps
        self.energy_eigenvals = energy_eigenvals
        self.step_size = well_width / steps
        
        self.basis_funcs = []
        self.eigenvals = []
        self.xvals = []
        
        self.hbar = hbar
        self.mass = mass
        
        self.generate_basis_funcs()

    def generate_basis_funcs(self):
        # know how to generate the infinite square well basis
        PI = np.pi
        L = self.well_width
        self.xvals = np.linspace(0, L, self.steps+1)
        for n in range(1,self.energy_eigenvals):
            energy = (n * self.hbar * PI / L) ** 2 / (2.0*self.mass)
            eigenfunc = []
            
            for x in self.xvals:
                eigenfunc.append(np.sqrt(2/L)*np.sin(n*PI*x/L))

            self.eigenvals.append(energy)
            self.basis_funcs.append(eigenfunc)

if __name__ == "__main__":
    main()
