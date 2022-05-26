# libraries
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import tkinter

from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg,
                                              NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# files
from potentials import PotentialType
from infinitesquarewell import InfiniteSquareWell
from generatehamiltonian import *
from window_events import *

def solve_problem():
        # get infinite square well basis
    ISW = InfiniteSquareWell()
    # choose potential
    potential = PotentialType.linear
    V = potential.get_potential(ISW,100.0)
    # compute hamiltonian matrix from the potential 
    H = compute_hamiltonian(V, ISW)
    # diagonalize hamiltonian, getting eigenvals and eigenvecs
    vals, vecs = la.eig(H)
    # new functions are the eigenvectors time the eigenfunctions of ISW
    newfuncs = []
    for col in np.transpose(vecs):
        lin_combination = np.zeros(len(ISW.basis_funcs[0]))
        for (i,val) in enumerate(col):
            lin_combination += np.multiply(ISW.basis_funcs[i],val)
        newfuncs.append(lin_combination)

    x = ISW.xvals

    # plt.xlim(0, 1)
    # plt.ylim(-2, 2)
    # plt.plot(x,V,'black')
    # for func in newfuncs:
        # plt.plot(x, func)

    # plt.show()
    
    return (x,newfuncs)

def main():
    global canvas,toolbar,selector
    root = tkinter.Tk()
    root.wm_title("1-D Schrodinger")

    selector = 0

    x,funcs = solve_problem()

    fig = Figure(figsize=(5, 4), dpi=100)
    
    subfig = fig.add_subplot(111)
    subfig.set_xlim(0,max(x))
    subfig.set_ylim(-2,2)

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)

    selector_button = tkinter.Button(master=root, text="Next Plot",
            command=lambda: inc_selector(subfig,x,funcs))
    selector_button.pack(side=tkinter.BOTTOM)
    
    tkinter.mainloop()

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def inc_selector(subfig,x,funcs):
    global canvas,selector
    subfig.clear()
    subfig.set_xlim(0,max(x))
    subfig.set_ylim(-2,2)
    subfig.plot(x,funcs[selector])
    if selector < len(funcs)-1:
        selector += 1
    else:
        selector = 0
    canvas.draw()
    
if __name__ == "__main__":
    main()
