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
    def __init__(self, subfig, canvas, x, funcs):
        self.selector = 0 # which one do we show
        self.subfig = subfig # where to we put it
        self.canvas = canvas # ditto
        self.x = x # same x values for all the functions
        self.funcs = funcs # library of functions
        self.energy_eigenvals = len(funcs) # determined in main
        self.calc_max_y() 
        self.calc_max_x() # determined by well width

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
        self.subfig.plot(self.x_max,V)
        self.canvas.draw()

    # show first plot in the sequence, ignore value of selector
    def init_plot(self):
        self.replot(self.funcs[0])

    # calculate and recalculate maxes
    def calc_max_y(self):
        self.max_val = max(map(max,map(abs,self.funcs)))+0.1 # y limits

    def calc_max_x(self):
        self.x_max = max(self.x)

    def update_vals(self, x, funcs):
        self.x = x
        self.funcs = funcs
        self.calc_max_x()
        self.calc_max_y()
        self.init_plot()
