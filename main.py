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
from incdecbutton import *

def solve_problem(potential_choice):
    # get infinite square well basis
    ISW = InfiniteSquareWell(energy_eigenvals=10)
    # choose potential
    potential = potential_choice
    V = potential.get_potential(ISW,100)
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
    
    return (x,sorted_newfuncs,V)

def main():
    global canvas, root

    # set up tkinter
    root = tkinter.Tk()
    root.wm_title("1-D Schrodinger")

    # create list items & such
    list_items = tkinter.Variable(value=[potential.name for potential in PotentialType])
    listbox = tkinter.Listbox(root, listvariable=list_items,height=3,selectmode=tkinter.BROWSE)
    potential_choice = PotentialType.square

    # add matplotlib hook to tk
    fig = Figure(figsize=(5, 4), dpi=100)
    subfig = fig.add_subplot(111)
    fig.suptitle(potential_choice.name)
    
    # solve the problem with initial choice
    x,funcs,V = solve_problem(potential_choice)

    # connect matplotlib hook to tk root
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    
    # Toolbar widgets
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    # buttons
    # Quit button
    quit_button = tkinter.Button(master=root, text="Quit", command=lambda: _quit(root))

    # Helper class that has button functions
    inc_dec = IncDecButton(subfig,canvas,x,funcs,V)
    inc_dec.init_plot()

    # prev eigenfunction
    prev_button = tkinter.Button(master=root, text="Prev Plot", command=lambda: inc_dec.dec_selector())

    # next eigenfunction
    next_button = tkinter.Button(master=root, text="Next Plot", command=lambda: inc_dec.inc_selector())

    # plot the potential
    potential_button = tkinter.Button(master=root, text="Plot Potential", command=lambda: inc_dec.plot_potential(V))

    listbox.bind('<<ListboxSelect>>', lambda x : on_item_select(listbox, inc_dec, fig, x))

    # pack buttons
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    quit_button.pack(side=tkinter.LEFT)
    prev_button.pack(side=tkinter.LEFT)
    next_button.pack(side=tkinter.LEFT)
    potential_button.pack(side=tkinter.LEFT)
    listbox.pack(side=tkinter.RIGHT)

    tkinter.mainloop()

def on_item_select(listbox, button_obj, fig, event):
    pot_vals = [enum for enum in PotentialType]
    selected_potential = pot_vals[listbox.curselection()[0]]
    structure_window(selected_potential, button_obj, fig)

def structure_window(potential_choice, button_obj, fig):
    global canvas, root
    # solve the problem
    x,funcs,V = solve_problem(potential_choice)

    # update figure title
    fig.suptitle(potential_choice.name)

    # update button class
    button_obj.update_vals(x, funcs, V)
    

def _quit(root):
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

if __name__ == "__main__":
    main()
