import numpy as np
import matplotlib.pyplot as plt
from enum import Enum, auto
from infinitesquarewell import InfiniteSquareWell

def main():
    ISW = InfiniteSquareWell()
    potential = PotentialType.linear
    V = potential.get_potential(ISW,1.0)
    plt.plot(ISW.xvals, V)
    plt.show()

MXVAL = 10000.0

def general_well(ISW,f):
    ret = [MXVAL]

    for x in ISW.xvals[1:len(ISW.xvals)-1]:
        ret.append(f(x))
    # ret.append(f(x) for x in np.arange(ISW.step_size, ISW.well_width-ISW.step_size,ISW.step_size))
    
    ret.append(MXVAL)

    return ret

def square(ISW, amplitude):
    assert(isinstance(ISW, InfiniteSquareWell))
    return general_well(ISW, lambda x: amplitude)

def linear(ISW, amplitude):
    assert(isinstance(ISW, InfiniteSquareWell))
    return general_well(ISW, lambda x: amplitude * x)

def quadratic(ISW, amplitude):
    assert(isinstance(ISW, InfiniteSquareWell))
    return general_well(ISW, lambda x: amplitude * x * x)
    
def centered_quadratic(ISW, amplitude):
    assert(isinstance(ISW, InfiniteSquareWell))
    def centered(x):
        mid = ISW.well_width / 2.0
        if x > 0.5 * mid and x < 1.5 * mid:
            offset = x - mid
            return amplitude * offset * offset
        else:
            return 0
    return general_well(ISW, centered)
    
def square_barrier(ISW, amplitude):
    ret = [MXVAL]
    step = ISW.step_size
    width = ISW.well_width

    for x in np.arange(step, width * 0.4, step):
        ret.append(0.0)

    for x in np.arange(width * 0.4, width * 0.6, step):
        ret.append(amplitude)

    for x in np.arange(width * 0.6, width, step):
        ret.append(0.0)

    ret.append(MXVAL)

    return ret
    
def square_plus_linear(ISW, amplitude):
    width = ISW.well_width
    def spl(x):
        if x < width * 0.5:
            return 0.0
        else:
            return amplitude * (x - (width / 2.0))
    return general_well(ISW, spl)

def triangle_barrier(ISW, amplitude):
    width = ISW.well_width
    def triangle(x):
        if ((0.4*width < x) and (x < width / 2.0)):
            return amplitude * (x - 0.4*width)
        elif (x >= width / 2.0 and x <= 0.6*width):
            return -amplitude * (x - 0.6*width)
        else:
            return 0.0

    return general_well(ISW, triangle)
    
def coupled_quadratic(ISW, amplitude):
    width = ISW.well_width
    def cq(x):
        if x < width * 0.5:
            return amplitude * ((x - (width / 4)) ** 2)
        if x >= width * 0.5:
            return amplitude * ((x - (width - (width / 4))) ** 2)

    return general_well(ISW, cq)

    
# def kronig_penney(ISW):
    
class PotentialType(Enum):
    square             = auto() # WORKING
    linear             = auto() # WORKING
    quadratic          = auto() # WORKING
    centered_quadratic = auto() # WORKING
    square_barrier     = auto() # WORKING
    square_plus_linear = auto() # WORKING
    triangle_barrier   = auto() # WORKING
    coupled_quadratic  = auto() # WORKING
    # kronig_penney = auto()

    def get_potential(self, ISW, amplitude):
        assert(isinstance(ISW, InfiniteSquareWell))
        if self is PotentialType.square:
            return square(ISW,amplitude)
        elif self is PotentialType.linear:
            return linear(ISW,amplitude)
        elif self is PotentialType.quadratic:
            return quadratic(ISW,amplitude)
        elif self is PotentialType.centered_quadratic:
            return centered_quadratic(ISW,amplitude)
        elif self is PotentialType.square_barrier:
            return square_barrier(ISW,amplitude)
        elif self is PotentialType.square_plus_linear:
            return square_plus_linear(ISW,amplitude)
        elif self is PotentialType.triangle_barrier:
            return triangle_barrier(ISW,amplitude)
        elif self is PotentialType.coupled_quadratic:
            return coupled_quadratic(ISW,amplitude)
        # elif self is PotentialType.kronig_penney:
        #     return kronig_penney(ISW)

if __name__ == "__main__":
    main()
