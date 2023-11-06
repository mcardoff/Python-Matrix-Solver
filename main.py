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


def solve_problem(text_obj, potential_choice, potential_amplitude,
                  e_vals=10, l_bnd=-5.0, r_bnd=5.0):
    """Solve the particle in a box problem given the following.

    - Potential Form
    - Potential Amplitude
    - Well Width
    - (TODO) Number of e-vals
    """
    # get infinite square well basis
    ISW = InfiniteSquareWell(energy_eigenvals=e_vals,
                             well_min=l_bnd, well_max=r_bnd)
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


def main():
    """Run the main loop of the program, handle events, etc."""
    global canvas, root

    # set up tkinter
    root = tkinter.Tk()
    root.geometry("1000x600")
    root.wm_title("1-D Schrodinger")

    # create list items & such
    potentials = [potential.name for potential in PotentialType]
    list_items = tkinter.Variable(value=potentials)
    listbox = tkinter.Listbox(
        root,
        listvariable=list_items,
        height=3,
        exportselection=False,
        selectmode=tkinter.BROWSE)
    listbox.selection_set(first=0)  # set first selection by default

    # Default choice is square well upon start
    potential_choice = PotentialType.square
    potential_amp = 0.0

    # add matplotlib hook to tk
    fig = Figure(figsize=(5, 4), dpi=100)
    subfig = fig.add_subplot(111)
    fig.suptitle(potential_choice.to_string())

    # Text containing energy values:
    e_text = tkinter.Text(root, height=3, width=20)

    # validaters for float and int
    reg_f = root.register(_validate_float)
    reg_i = root.register(_validate_int)

    # Text field containing potential amplitude
    amp_label_text = tkinter.StringVar(value="Potential Amp:")
    amp_label = tkinter.Label(root, textvariable=amp_label_text, height=2)

    amp_text = tkinter.Entry(
        root, validate="key", validatecommand=(reg_f, '%P'))
    amp_text.insert(tkinter.END, "0")

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

    # change well minimum and maximum
    min_entry = tkinter.Entry(
        root, validate="key", validatecommand=(reg_f, '%P'))
    min_entry.insert(tkinter.END, str(min(x)))

    max_entry = tkinter.Entry(
        root, validate="key", validatecommand=(reg_f, '%P'))
    max_entry.insert(tkinter.END, str(max(x)))

    # change dimension of Hamiltonian
    eig_entry = tkinter.Entry(
        root, validate="key", validatecommand=(reg_i, '%P'))
    eig_entry.insert(tkinter.END, "10")

    # listbox to pick potential
    listbox.bind('<<ListboxSelect>>',
                 lambda x: _on_item_select(
                     listbox, inc_dec, e_text, amp_text,
                     fig, min_entry, max_entry, eig_entry, x))

    # labels
    eng_label_text = tkinter.StringVar(value="Energy Values:")
    pot_label_text = tkinter.StringVar(value="1-D Potential:")
    min_label_text = tkinter.StringVar(value="Well Min:")
    max_label_text = tkinter.StringVar(value="Well Max:")
    eig_label_text = tkinter.StringVar(value="Energy Eigenvals:")
    energy_label = tkinter.Label(root, textvariable=eng_label_text, height=2)
    pot_label = tkinter.Label(root, textvariable=pot_label_text, height=2)
    min_label = tkinter.Label(root, textvariable=min_label_text, height=2)
    max_label = tkinter.Label(root, textvariable=max_label_text, height=2)
    eig_label = tkinter.Label(root, textvariable=eig_label_text, height=2)

    # pack buttons
    canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
    prev_button.pack(side=tkinter.TOP)
    next_button.pack(side=tkinter.TOP)
    potential_button.pack(side=tkinter.TOP)
    pot_label.pack(side=tkinter.TOP)
    listbox.pack(side=tkinter.TOP)
    eig_label.pack(side=tkinter.TOP)
    eig_entry.pack(side=tkinter.TOP)
    amp_label.pack(side=tkinter.TOP)
    amp_text.pack(side=tkinter.TOP)
    min_label.pack(side=tkinter.TOP)
    min_entry.pack(side=tkinter.TOP)
    max_label.pack(side=tkinter.TOP)
    max_entry.pack(side=tkinter.TOP)
    energy_label.pack(side=tkinter.TOP)
    e_text.pack(side=tkinter.TOP)
    quit_button.pack(side=tkinter.BOTTOM)

    tkinter.mainloop()


def _format_energy_text(text_obj, energy_vals):
    """Clear text currently in text_obj, replace with energy_vals."""
    text_obj.delete("1.0", "end")

    energy_string = ""
    for (i, val) in enumerate(np.sort(energy_vals)):
        num = "0{}".format(i+1) if i+1 < 10 else str(i+1)
        energy_string += "E_{} = {:.2f}\n".format(num, val)

    text_obj.insert(tkinter.END, energy_string)


def _validate_float(test):
    """Validate whether or not test is a valid floating number input."""
    # Ensure only one minus sign and decimal point
    replace_chars = ['.', '-']
    for char in replace_chars:
        test = test.replace(char, "", 1)

    return (test.isdigit() or test == "")


def _validate_int(test):
    """Validate whether or not test is a valid integer input."""
    # isdigit is siffucient
    return (test.isdigit() or test == "")


def _on_item_select(list_box, button_obj, e_text_obj, amp_text_obj,
                    fig, min_text_obj, max_text_obj, e_val_obj, event):
    """When an item in list_box is selected, recalculate the problem."""
    # global canvas, root

    potential = [enum for enum in PotentialType][list_box.curselection()[0]]
    potential_amp = float(amp_text_obj.get())
    well_min = float(min_text_obj.get())
    well_max = float(max_text_obj.get())
    e_vals = int(e_val_obj.get())

    # solve the problem... again
    x, funcs, V, vals = solve_problem(
        e_text_obj, potential, potential_amp,
        e_vals=e_vals, l_bnd=well_min, r_bnd=well_max)

    # update figure title
    fig.suptitle(potential.to_string())

    # update button class
    button_obj.update_vals(x, funcs, V)

    # update energy text
    _format_energy_text(e_text_obj, vals)


def _quit(root):
    root.quit()  # stops mainloop
    root.destroy()


if __name__ == "__main__":
    main()
