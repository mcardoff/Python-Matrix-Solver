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
    def __init__(self, subfig, canvas, energy_eigenvals=5):
        self.selector = 0
        self.energy_eigenvals = energy_eigenvals
        self.subfig = subfig
        self.canvas = canvas

    def replot(self,x,func,max_val):
        self.subfig.clear()
        self.subfig.set_ylim(-max_val,max_val)
        self.subfig.plot(x,func)
        self.canvas.draw()

    def inc_selector(self,x,funcs):
        if self.selector < len(funcs)-1:
            self.selector += 1
        else:
            self.selector = 0
        
        self.subfig.set_xlim(0,max(x))
        max_val = max(map(max,funcs))
        self.replot(x,funcs[self.selector],max_val)

    def dec_selector(self,x,funcs):
        if self.selector > 0:
            self.selector -= 1
        else:
            self.selector = len(funcs)-1
            
        self.subfig.set_xlim(0,max(x))
        max_val = max(map(max,funcs))
        self.replot(x,funcs[self.selector],max_val)

    def plot_potential(self,x,V):
        global canvas
        self.subfig.set_xlim(0,max(x))
        self.subfig.set_ylim(-2,2)
        self.subfig.plot(x,V)
        self.canvas.draw()

