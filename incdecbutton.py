# libraries
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import tkinter

from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg,
                                              NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class IncDecButton:
    def __init__(self, subfig, canvas, x, funcs, V):
        self.selector = 0 # which one do we show
        self.subfig = subfig # where to we put it
        self.canvas = canvas # ditto
        self.x = x # same x values for all the functions
        self.funcs = funcs # library of functions
        self.potential = V # potential 
        self.energy_eigenvals = len(funcs) # determined in main
        self.calc_maxes() # x and y limits

    # plot the function func, clearing previous plot and resetting limits
    def replot(self,func):
        self.subfig.clear()
        self.subfig.set_xlim(0,self.x_max)
        self.subfig.set_ylim(-self.max_val,self.max_val)
        self.subfig.plot(self.x,func)
        self.canvas.draw()

    # show 'previous' plot, loop to end if first
    def inc_selector(self):
        if self.selector < len(self.funcs)-1:
            self.selector += 1
        else:
            self.selector = 0
        
        self.replot(self.funcs[self.selector])

    # show 'next' plot, loop to beginning at the end
    def dec_selector(self):
        if self.selector > 0:
            self.selector -= 1
        else:
            self.selector = len(self.funcs)-1
            
        self.replot(self.funcs[self.selector])

    # show potential on top of current plot
    def plot_potential(self,V):
        self.subfig.set_xlim(0,self.x_max)
        self.subfig.set_ylim(-self.max_val,self.max_val)
        self.subfig.plot(self.x,V)
        self.canvas.draw()

    # show first plot in the sequence, ignore value of selector
    def init_plot(self):
        self.replot(self.funcs[0])

    # calculate and recalculate maxes
    def calc_maxes(self):
        self.max_val = max(map(max,map(abs,self.funcs)))+0.1 # y limits
        self.x_max = max(self.x) # well width determines x limit

    def update_vals(self, x, funcs, V):
        self.x = x
        self.funcs = funcs
        self.potential = V
        self.calc_maxes()
        self.init_plot()
