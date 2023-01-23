"""Solve the particle in a box problem via diagonalization."""
# libraries
import numpy as np
import numpy.linalg as la
import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

# files
from potentials import PotentialType
from incdecbutton import IncDecButton
from infinitesquarewell import InfiniteSquareWell
from generatehamiltonian import compute_hamiltonian


def solve_problem(text_obj, potential_choice, potential_amplitude):
    """Solve the particle in a box problem given the following.

    - Potential Form
    - Potential Amplitude
    - Well Width (TODO)
    """
    # get infinite square well basis
    ISW = InfiniteSquareWell(energy_eigenvals=10, well_max=5.0)
    # choose potential
    potential = potential_choice
    V = potential.get_potential(ISW, potential_amplitude)
    # compute hamiltonian matrix from the potential
    H = compute_hamiltonian(V, ISW)
    # diagonalize hamiltonian, getting eigenvals and eigenvecs
    vals, vecs = la.eig(H)
    # new functions are the eigenvectors time the eigenfunctions of ISW
    newfuncs = []
    for col in np.transpose(vecs):
        lin_combination = np.zeros(len(ISW.basis_funcs[0]))
        for (i, val) in enumerate(col):
            lin_combination += np.multiply(ISW.basis_funcs[i], val)
        newfuncs.append(lin_combination)

    x = ISW.xvals

    # sort by eigenval
    zipped = zip(vals, newfuncs)
    sorted_zip = sorted(zipped)
    sorted_newfuncs = [func for _, func in sorted_zip]

    _format_energy_text(text_obj, vals)

    return (x, sorted_newfuncs, V, vals)


def _format_energy_text(text_obj, energy_vals):
    # clear text currently in object
    text_obj.delete("1.0", "end")

    energy_string = ""
    for (i, val) in enumerate(np.sort(energy_vals)):
        num = str(i+1)
        if i+1 < 10:
            num = "0{}".format(i+1)
        energy_string += "E_{} = {:.2f}\n".format(num, val)

    text_obj.insert(tkinter.END, energy_string)


def on_item_select(listbox, button_obj, e_text_obj, amp_text_obj, fig, event):
    """When an item in listbox is selected, recalculate the problem."""
    global canvas, root

    pot_vals = [enum for enum in PotentialType]
    potential = pot_vals[listbox.curselection()[0]]
    potential_amp = float(amp_text_obj.get("1.0", tkinter.END))

    # solve the problem
    x, funcs, V, vals = solve_problem(e_text_obj, potential, potential_amp)

    # update figure title
    fig.suptitle(potential.name)

    # update button class
    button_obj.update_vals(x, funcs, V)

    # update energy text
    _format_energy_text(e_text_obj, vals)


def _quit(root):
    root.quit()  # stops mainloop
    root.destroy()


def main():
    """Run the main loop of the program, handle events, etc."""
    global canvas, root

    # set up tkinter
    root = tkinter.Tk()
    root.geometry("800x600")
    root.wm_title("1-D Schrodinger")

    # create list items & such
    potentials = [potential.name for potential in PotentialType]
    list_items = tkinter.Variable(value=potentials)
    listbox = tkinter.Listbox(
        root,
        listvariable=list_items,
        height=3,
        selectmode=tkinter.BROWSE)

    # Default choice is square well upon start
    potential_choice = PotentialType.square
    potential_amp = 0.0

    # add matplotlib hook to tk
    fig = Figure(figsize=(5, 4), dpi=100)
    subfig = fig.add_subplot(111)
    fig.suptitle(potential_choice.name)

    # Text containing energy values:
    e_text = tkinter.Text(root, height=3, width=20)

    # Text field containing potential amplitude
    label_text = tkinter.StringVar()
    label_text.set("Potential Amp:")
    label_dir = tkinter.Label(root, textvariable=label_text, height=2)

    amp_text = tkinter.Text(root, height=1, width=10)
    amp_text.insert(tkinter.END, str(potential_amp))

    # solve the problem with initial choice
    x, funcs, V, vals = solve_problem(e_text, potential_choice, potential_amp)

    # connect matplotlib hook to tk root
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    # Toolbar widgets
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    # buttons
    # Quit button
    quit_button = tkinter.Button(
        master=root, text="Quit", command=lambda: _quit(root))

    # Helper class that has button functions
    inc_dec = IncDecButton(subfig, canvas, x, funcs, V)
    inc_dec.init_plot()

    # prev eigenfunction
    prev_button = tkinter.Button(
        master=root, text="Prev Plot", command=lambda: inc_dec.dec_selector())

    # next eigenfunction
    next_button = tkinter.Button(
        master=root, text="Next Plot", command=lambda: inc_dec.inc_selector())

    # plot the potential
    potential_button = tkinter.Button(
        master=root,
        text="Plot Potential",
        command=lambda: inc_dec.plot_potential())

    listbox.bind('<<ListboxSelect>>',
                 lambda x: on_item_select(
                     listbox, inc_dec, e_text, amp_text, fig, x))

    # pack buttons
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    quit_button.pack(side=tkinter.LEFT)
    prev_button.pack(side=tkinter.LEFT)
    next_button.pack(side=tkinter.LEFT)
    potential_button.pack(side=tkinter.LEFT)
    listbox.pack(side=tkinter.RIGHT)
    e_text.pack(side=tkinter.RIGHT)
    amp_text.pack(side=tkinter.RIGHT)
    label_dir.pack(side=tkinter.RIGHT)

    tkinter.mainloop()


if __name__ == "__main__":
    main()
