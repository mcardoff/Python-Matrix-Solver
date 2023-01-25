"""Class to organize and work with various potentials easily."""
import matplotlib.pyplot as plt
from enum import Enum, auto
from infinitesquarewell import InfiniteSquareWell


def main():
    """Test If potential plot is correct."""
    ISW = InfiniteSquareWell()
    potential = PotentialType.linear
    V = potential.get_potential(ISW, 1.0)
    plt.plot(ISW.xvals, V)
    plt.show()


def general_well(ISW, f):
    """Place an infinite barrier at bounds, evals func provided elsewhere."""
    MXVAL = 10000.0

    ret = [MXVAL]

    for x in ISW.xvals[1:len(ISW.xvals)-1]:
        # print('x: {}, f(x): {}'.format(x, f(x)))
        ret.append(f(x))

    ret.append(MXVAL)
    return ret


def square(ISW, amplitude):
    """Particle in a box."""
    assert(isinstance(ISW, InfiniteSquareWell))
    return general_well(ISW, lambda x: amplitude)


def linear(ISW, amplitude):
    """Particle in an electric field."""
    assert(isinstance(ISW, InfiniteSquareWell))
    return general_well(ISW, lambda x: amplitude * x)


def quadratic(ISW, amplitude):
    """Half-harmonic oscillator potential."""
    assert(isinstance(ISW, InfiniteSquareWell))
    return general_well(ISW, lambda x: amplitude * x * x)


def centered_quadratic(ISW, amplitude):
    """Quadratic potential barrier in the center of the well."""
    assert(isinstance(ISW, InfiniteSquareWell))

    def centered(x):
        width = ISW.well_width
        mid = (ISW.well_max - abs(ISW.well_min)) / 2.0
        offset = x - mid
        if abs(offset) < 0.25 * width:
            return amplitude * offset * offset
        else:
            return 0
    return general_well(ISW, centered)


def square_barrier(ISW, amplitude):
    """Square-shaped potential barrier."""
    def sqb(x):
        width = ISW.well_width
        mid = (ISW.well_max - abs(ISW.well_min)) / 2.0
        offset = x - mid
        if abs(offset) < 0.2 * 0.5 * width:
            return amplitude
        else:
            return 0.0
    return general_well(ISW, sqb)


def square_plus_linear(ISW, amplitude):
    """Flat Potential that turns linear after a bit."""
    def spl(x):
        mid = (ISW.well_max + ISW.well_min) / 2.0
        offset = x - mid
        if offset < 0:
            return 0.0
        else:
            return amplitude * (offset)
    return general_well(ISW, spl)


def triangle_barrier(ISW, amplitude):
    """Triangle-Shaped Potential barrier."""
    def triangle(x):
        width = ISW.well_width
        mid = (ISW.well_max + ISW.well_min) / 2.0
        offset = x - mid
        if abs(offset) < 0.25*width:
            return -amplitude*(abs(offset) - 0.25*width)
        else:
            return 0.0
    return general_well(ISW, triangle)


def coupled_quadratic(ISW, amplitude):
    """Multiple quadratic potentials next to each other."""
    def cq(x):
        width = ISW.well_width
        mid = (ISW.well_max + ISW.well_min) / 2.0
        offset = x - mid
        if abs(offset) < 0.25 * width:
            return amplitude * (abs(offset) - 0.125*width) ** 2
        else:
            return 0.0
    return general_well(ISW, cq)


def kronig_penney(ISW, amplitude):
    """Kronig-Penney Potential to model solids."""
    def kp(x):
        # 3 barriers -> 0.25 0.5 0.75
        offset = x - ISW.well_min
        num_barriers = 5
        spacing = ISW.well_width / (num_barriers + 1)
        bar_wid = 2 / ((num_barriers + 1))
        # n bars of wid d equally spaced between min and max
        # positions of bars determined by width / (num_barriers+1)
        # if (x - left_lim) = w / (n+1), delta site
        for i in range(1, num_barriers+1):
            if i*spacing - bar_wid < offset and offset < i*spacing + bar_wid:
                return amplitude
        else:
            return 0
    return general_well(ISW, kp)


class PotentialType(Enum):
    """Enumeration which contains all working potential types."""

    square = auto()              # WORKING
    linear = auto()              # WORKING
    quadratic = auto()           # WORKING
    centered_quadratic = auto()  # WORKING
    square_barrier = auto()      # WORKING
    square_plus_linear = auto()  # WORKING
    triangle_barrier = auto()    # WORKING
    coupled_quadratic = auto()   # WORKING
    kronig_penney = auto()       # WORKING

    def get_potential(self, ISW, amplitude):
        """From enum type, return the proper potential to compute."""
        assert(isinstance(ISW, InfiniteSquareWell))
        if self is PotentialType.square:
            return square(ISW, amplitude)
        elif self is PotentialType.linear:
            return linear(ISW, amplitude)
        elif self is PotentialType.quadratic:
            return quadratic(ISW, amplitude)
        elif self is PotentialType.centered_quadratic:
            return centered_quadratic(ISW, amplitude)
        elif self is PotentialType.square_barrier:
            return square_barrier(ISW, amplitude)
        elif self is PotentialType.square_plus_linear:
            return square_plus_linear(ISW, amplitude)
        elif self is PotentialType.triangle_barrier:
            return triangle_barrier(ISW, amplitude)
        elif self is PotentialType.coupled_quadratic:
            return coupled_quadratic(ISW, amplitude)
        elif self is PotentialType.kronig_penney:
            return kronig_penney(ISW, amplitude)


if __name__ == "__main__":
    main()
