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

def solve_problem():
    # get infinite square well basis
    ISW = InfiniteSquareWell(energy_eigenvals=5)
    # choose potential
    potential = PotentialType.square_plus_linear
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

    # sort by eigenval
    zipped = zip(vals,newfuncs)
    sorted_zip = sorted(zipped)
    sorted_newfuncs = [func for _,func in sorted_zip]

    # plt.xlim(0, 1)
    # plt.ylim(-2, 2)
    # plt.plot(x,V,'black')
    # for func in newfuncs:
        # plt.plot(x, func)

    # plt.show()
    
    return (x,sorted_newfuncs,V)

def main():
    global canvas,toolbar,selector
    root = tkinter.Tk()
    root.wm_title("1-D Schrodinger")

    selector = 0

    x,funcs,V = solve_problem()

    fig = Figure(figsize=(5, 4), dpi=100)
    subfig = fig.add_subplot(111)
    
    subfig.plot(x,funcs[0])

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # buttons
    quit_button = tkinter.Button(master=root, text="Quit",
            command=lambda: _quit(root))
    quit_button.pack(side=tkinter.LEFT)

    prev_button = tkinter.Button(master=root, text="Prev Plot",
            command=lambda: dec_selector(subfig,x,funcs))
    prev_button.pack(side=tkinter.LEFT)

    next_button = tkinter.Button(master=root, text="Next Plot",
            command=lambda: inc_selector(subfig,x,funcs))
    next_button.pack(side=tkinter.LEFT)

    potential_button = tkinter.Button(master=root, text="Plot Potential",
            command=lambda: plot_potential(subfig,x,V))
    potential_button.pack(side=tkinter.LEFT)
    
    tkinter.mainloop()

def _quit(root):
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def replot(subfig,x,func,max_val):
    global canvas
    subfig.clear()
    subfig.set_ylim(-max_val,max_val)
    subfig.plot(x,func)
    canvas.draw()

def inc_selector(subfig,x,funcs):
    global canvas,selector
    if selector < len(funcs)-1:
        selector += 1
    else:
        selector = 0
        
    subfig.set_xlim(0,max(x))
    max_val = max(map(max,funcs))
    replot(subfig,x,funcs[selector],max_val)


def dec_selector(subfig,x,funcs):
    global canvas,selector
    if selector > 0:
        selector -= 1
    else:
        selector = len(funcs)-1
    
    subfig.set_xlim(0,max(x))
    max_val = max(map(max,funcs))
    replot(subfig,x,funcs[selector])

def plot_potential(subfig,x,V):
    global canvas
    # subfig.clear()
    subfig.set_xlim(0,max(x))
    subfig.set_ylim(-2,2)
    subfig.plot(x,V)
    canvas.draw()
    
if __name__ == "__main__":
    main()
