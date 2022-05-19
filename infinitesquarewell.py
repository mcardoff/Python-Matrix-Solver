import numpy as np

class InfiniteSquareWell:
    self.well_width = 1.0
    self.steps = 200
    self.energy_eigenvals = 5
    self.step_size = well_width / steps

    self.basis_funcs = []
    self.eigenvals = []
    self.xvals = []

    self.hbar = 1.0
    self.mass = 1.0

    def __init__(self, well_width=1.0, steps=200,
                 energy_eigenvals=5, hbar=1.0, mass=1.0):
        self.step_size=well_width / steps
        generate_basis_funcs()

    def generate_basis_funcs():
        # know how to generate the infinite square well basis
