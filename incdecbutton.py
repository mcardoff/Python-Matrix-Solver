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
    def __init__(self, subfig, canvas, x, funcs, energy_eigenvals=5):
        self.selector = 0
        self.energy_eigenvals = energy_eigenvals
        self.subfig = subfig
        self.canvas = canvas
        self.funcs = funcs
        self.x = x
        self.max_val = max(map(max,map(abs,self.funcs)))+0.1
        self.x_max = max(self.x)

    def replot(self,func):
        self.subfig.clear()
        self.subfig.set_xlim(0,self.x_max)
        self.subfig.set_ylim(-self.max_val,self.max_val)
        self.subfig.plot(self.x,func)
        self.canvas.draw()

    def inc_selector(self):
        if self.selector < len(self.funcs)-1:
            self.selector += 1
        else:
            self.selector = 0
        
        self.replot(self.funcs[self.selector])

    def dec_selector(self):
        if self.selector > 0:
            self.selector -= 1
        else:
            self.selector = len(self.funcs)-1
            
        self.replot(self.funcs[self.selector])

    def plot_potential(self,V):
        self.subfig.set_xlim(0,max(self.x))
        self.subfig.set_ylim(-2,2)
        self.subfig.plot(self.x,V)
        self.canvas.draw()

    def init_plot(self):
        self.replot(self.funcs[0])
