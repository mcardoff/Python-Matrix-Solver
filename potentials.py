import numpy as np
from enum import Enum, auto
from infinitesquarewell import InfiniteSquareWell

MXVAL = 10000.0

def general_well(ISW,f):
    ret = [MXVAL]
    
    ret.append(f(x) for x in np.arange(ISW.step_size, ISW.well_width-ISW.step_size,ISW.step_size))
    
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
    ret = [MXVAL]
    step = ISW.step_size
    width = ISW.well_width

    for x in np.arange(step, width * 0.5, step):
        ret.append(0.0)

    for x in np.arange(width * 0.5, width-step, step):
        ret.append(amplitude * (x - (width / 2.0)))

    ret.append(MXVAL)

    return ret

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
    ret = [MXVAL]
    step = ISW.step_size
    width = ISW.well_width

    for x in np.arange(step, width * 0.5, step):
        ret.append(amplitude * ((x - (width / 4)) ** 2))

    for x in np.arange(width * 0.5, width-step, step):
        ret.append(amplitude * ((x - (width - (width / 4))) ** 2))

    ret.append(MXVAL)

    return ret
    
# def coupled_square_plus_field(ISW):
    
# def kronig_penney(ISW):
    
class PotentialType(Enum):
    square = auto()
    linear = auto()
    quadratic = auto()
    centered_quadratic = auto()
    square_barrier = auto()
    square_plus_linear = auto()
    triangle_barrier = auto()
    # coupled_quadratic = auto()
    # coupled_square_plus_field = auto()
    # kronig_penney = auto()

    def get_potential(self, ISW):
        assert(isinstance(ISW, InfiniteSquareWell))
        if self is PotentialType.square:
            return square(ISW)
        elif self is PotentialType.linear:
            return linear(ISW)
        elif self is PotentialType.quadratic:
            return quadratic(ISW)
        elif self is PotentialType.centered_quadratic:
            return centered_quadratic(ISW)
        elif self is PotentialType.square_barrier:
            return square_barrier(ISW)
        elif self is PotentialType.square_plus_linear:
            return square_plus_linear(ISW)
        elif self is PotentialType.triangle_barrier:
            return triangle_barrier(ISW)
        # elif self is PotentialType.coupled_quadratic:
        #     return coupled_quadratic(ISW)
        # elif self is PotentialType.coupled_square_plus_field:
        #     return coupled_square_plus_field(ISW)
        # elif self is PotentialType.kronig_penney:
        #     return kronig_penney(ISW)
