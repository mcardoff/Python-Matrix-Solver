"""Create blank class to hold functions attached to buttons in main."""


class IncDecButton:
    """Class to track inc and dec of eigenfunctions."""

    def __init__(self, subfig, canvas, x, funcs, V):
        """Initialize necessary variables, attached to tkinter window."""
        self.selector = 0                   # which one do we show
        self.subfig = subfig                # where to we put it
        self.canvas = canvas                # ditto
        self.x = x                          # same x vals
        self.funcs = funcs                  # library of functions
        self.potential = V                  # potential
        self.energy_eigenvals = len(funcs)  # set in main
        self.calc_maxes()                   # x and y limits

    # plot the function func, clearing previous plot and resetting limits
    def replot(self, func):
        """Clear the plot and plot func in its place."""
        self.subfig.clear()
        self.subfig.set_xlim(0, self.x_max)
        self.subfig.set_ylim(-self.max_val, self.max_val)
        self.subfig.plot(self.x, func)
        self.canvas.draw()

    def inc_selector(self):
        """Show 'next' plot, loop to beginning at the end."""
        if self.selector < len(self.funcs)-1:
            self.selector += 1
        else:
            self.selector = 0

        self.replot(self.funcs[self.selector])

    def dec_selector(self):
        """Show 'previous' plot, loop to end if first."""
        if self.selector > 0:
            self.selector -= 1
        else:
            self.selector = len(self.funcs)-1

        self.replot(self.funcs[self.selector])

    def plot_potential(self):
        """Show potential on top of current plot."""
        self.subfig.set_xlim(0, self.x_max)
        self.subfig.set_ylim(-self.max_val, self.max_val)
        self.subfig.plot(self.x, self.potential)
        self.canvas.draw()

    def init_plot(self):
        """Show first plot in the sequence, ignore value of selector."""
        self.replot(self.funcs[0])

    def calc_maxes(self):
        """Calculate and recalculate maxes."""
        self.max_val = max(map(max, map(abs, self.funcs)))+0.1  # y limits
        self.x_max = max(self.x)           # well width determines x limit

    def update_vals(self, x, funcs, V):
        """Set values of x, funcs, V and recalculate maxes."""
        self.x = x
        self.funcs = funcs
        self.potential = V
        self.calc_maxes()
        self.init_plot()
