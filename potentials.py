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

def general_well(ISW,f):
    MXVAL = 10000.0

    ret = [MXVAL]

    for x in ISW.xvals[1:len(ISW.xvals)-1]:
        ret.append(f(x))
    
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
    def sqb(x):
        width = ISW.well_width
        if width * 0.4 < x and x < width * 0.6:
            return amplitude
        else:
            return 0.0
    return general_well(ISW, sqb)
    
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
    
def kronig_penney(ISW, amplitude):
    def kp(x):
        # 3 barriers -> 0.25 0.5 0.75
        num_barriers = 3
        spacing = 1 / (num_barriers + 1)
        bar_wid = (1/2.0) * spacing
        for i in range(1,num_barriers+1):
            if i*spacing - bar_wid/2 < x and x < i*spacing + bar_wid/2:
                ret = amplitude
                break
            else:
                ret = 0.0
        return ret
    return general_well(ISW, kp)
    
class PotentialType(Enum):
    square             = auto() # WORKING
    linear             = auto() # WORKING
    quadratic          = auto() # WORKING
    centered_quadratic = auto() # WORKING
    square_barrier     = auto() # WORKING
    square_plus_linear = auto() # WORKING
    triangle_barrier   = auto() # WORKING
    coupled_quadratic  = auto() # WORKING
    kronig_penney      = auto() # WORKING

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
        elif self is PotentialType.kronig_penney:
            return kronig_penney(ISW,amplitude)

if __name__ == "__main__":
    main()
