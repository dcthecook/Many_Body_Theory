# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:24:29 2023

@author: Enea
"""




import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
plt.style.use('dark_background')
import tkinter as tk
import time
import numpy as np
from tkinter import scrolledtext
import tkinter.filedialog as filedialog
import scipy as sp
from engine.bose_hubbard import Bose_Hubbard, basis_size_python


############
############
# Initialize global variables
############
############
model = 'Bose-Hubbard'
models = [
    'Bose-Hubbard', 'Fermi-Hubbard', 't-J Model', 'External Field Ising Model', '2Q Jordan-Wigner Ising', 'Anderson Model',
    'Heisenberg Model', 'XXY model'
]
particles = 3
sites = 3
interaction_potential = -0.18  # Default value as float
chemical_potential = 0.04     # Default value as float
t = 1.0                      # Default value as float
hamiltonian = None #initialize empty global
eigenvalues = None #empty global
eigenvectors = None #empty global
truncate = 9
has_run = False
has_diagonalized = False
basis_size = 0
total_elements = 0
color_scheme = 'terrain'
color_schemes = [
    "gist_rainbow", "coolwarm", "viridis", "plasma", "inferno", "magma",
    "twilight", "YlOrBr", "RdGy", "copper",
    "nipy_spectral", "cividis", "ocean", "terrain", "gnuplot", "jet",
    "Set1", "Set2", "Set3", "Pastel1", "Pastel2",
]
format_options = [
    "Dense Numpy format",
    "Sparse SciPy CSR format"
]
format_t = "Sparse SciPy CSR format"


# Create functions to set global variables and validate user input
def apply_all():
    global particles, sites, interaction_potential, chemical_potential, t
    new_particles = particles_entry.get()
    new_sites = sites_entry.get()
    new_interaction_potential = interaction_potential_entry.get()
    new_chemical_potential = chemical_potential_entry.get()
    new_t = t_entry.get()
    
    try:
        if new_particles:
            particles = int(new_particles)
        if new_sites:
            sites = int(new_sites)
        if new_interaction_potential:
            interaction_potential = float(new_interaction_potential)
        if new_chemical_potential:
            chemical_potential = float(new_chemical_potential)
        if new_t:
            t = float(new_t)

        # Update the labels
        particles_label.config(text=f"Particles: {particles}")
        sites_label.config(text=f"Sites: {sites}")
        interaction_potential_label.config(text=f"Interaction Potential: {interaction_potential}")
        chemical_potential_label.config(text=f"Chemical Potential: {chemical_potential}")
        t_label.config(text=f"Hopping Term: {t}")

        # Update the "Current Numbers" label
        update_current_numbers_label()
        stuff = "\nNumbers were successfully updated!"
        update_information(stuff)

    except ValueError:
        message = "\nError!: Invalid input detected!\nPlease check if all the inputs for the Constants are numbers!"
        update_information(message)
        raise ValueError(message)
        

        
        
def set_truncation():
    global truncate
    new_truncate = truncate_entry.get()
    try:
        truncate = int(new_truncate)
        truncate_label.config(text=f"first k eigenvalues: {truncate}")
        update_information(f"\nCalculating first k = {truncate} eigenpairs")
    except ValueError:
        raise ValueError('Input should be a valid number')
        tk.messagebox.showinfo("ERROR", "Input should be a valid number.")

# Function to update the "Current Numbers" label
def update_current_numbers_label():
    current_numbers_label.config(text=f"Current Numbers:\n Particles: {particles}\n Sites: {sites} \n Hopping Term: {t} \n Interaction Potential: {interaction_potential}\n Chemical Potential: {chemical_potential}")

    
def update_eigval_plot_size(event):
    eig_val_canvas.get_tk_widget().config(width=event.width, height=event.height)
    

    
#main event
def get_hamiltonian():
    global hamiltonian
    global has_run
    global basis_size
    global total_elements
    #current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    #info = f"\n[{current_time}]\nStarting Matrix calculation...\n.\n.\n.\n"
    #text_area.insert(tk.INSERT, info)
    start_time = time.time()
    hamiltonian = Bose_Hubbard(particles, sites, t, interaction_potential, chemical_potential)
    end_time = time.time()
    elapsed_time = end_time - start_time
    has_run = True
    basis_size = hamiltonian.shape[0]
    total_elements = basis_size**2
    if elapsed_time != 0:
        fetch_rate = int(total_elements/elapsed_time)
    else:
        fetch_rate = "~~time interval too short~~"
    message = f"\nElements Fetched in:\n{elapsed_time:.6f} seconds.\nFetch rate: {fetch_rate} elements/sec\nTotal nr of elements: {total_elements}\nBasis Size: {basis_size_python(particles, sites)}"
    #info = f"Successfully Updated Hamiltonian Matrix in {elapsed_time:.6f} seconds"
    #tk.messagebox.showinfo("Calculation Complete", message)
    update_information(message)

def diagonalize():
    global hamiltonian
    global eigenvalues
    global eigenvectors
    global truncate
    global has_diagonalized
    global format_t
    global particles
    global sites
    
    if has_run == False:
        update_information("Fatal Error!: No Hamiltonian present in global memory. Ending function...")
        return
    elif truncate == 0:
        update_information("Error!: The k first Eigenpairs constant is set to 0. It has to be between 1 and the basis size\nEnding function...")
        return
    elif truncate >= basis_size_python(particles, sites):
        msg = f"k value of: {truncate} is too large. It has to be smaller than the basis size of {basis_size_python(particles, sites)}"
        update_information(msg)
        return

    if format_t == "Sparse SciPy CSR format":
        sparse_ham = sp.sparse.csr_matrix(hamiltonian)
        truncate = truncate
        start_time = time.time()
        eigenvalues, eigenvectors = sp.sparse.linalg.eigsh(sparse_ham, k=truncate, which='SA')
        end_time = time.time()
        elapsed_time = end_time - start_time
        has_diagonalized = True
        message = f"\nEigenpairs Calculated in\n {elapsed_time:.6f} \nseconds."
        update_information(message)
        has_diagonalized = True
    else:
        start_time = time.time()
        eigenvalues, eigenvectors = np.linalg.eig(hamiltonian)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:,idx]
        end_time = time.time()
        elapsed_time = end_time - start_time
        has_diagonalized = True
        message = f"\nEigenpairs Calculated in\n {elapsed_time:.6f} \nseconds."
        update_information(message)
        has_diagonalized = True
        
    
    
    


def display_hamiltonian():
    global hamiltonian
    if has_run == False:
        message = "No Hamiltonian present in global memory. Please Calculate the Hamiltonian Matrix first!\nFunction Terminating..."
        update_information(message)
        return
    ax.clear()
    ax.imshow(hamiltonian, cmap=color_scheme)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    canvas.draw()
    canvas.get_tk_widget().place(x=200, y=0)
    
# Function to display eigenvalues
# Function to display eigenvalues
def display_eigenvalues():
    global eigenvalues, has_diagonalized
    
    if not has_diagonalized:
        message = "No Hamiltonian present in global memory. Please Calculate the Hamiltonian Matrix first!\nFunction Terminating..."
        update_information(message)
        return
    
    def display_eigenvalues_list():
        if eigenvalues is not None:
            eig_val_area.delete(1.0, tk.END)  # Clear the text area
            eig_val_area.insert(tk.END, "Output:\nEigenvalues List:\n")
            for i, eigenvalue in enumerate(eigenvalues):
                eig_val_area.insert(tk.END, f"Eigenvalue {i}: {eigenvalue}\n")
        else:
            eig_val_area.delete(1.0, tk.END)  # Clear the text area
            eig_val_area.insert(tk.END, "No eigenvalues available. Please run diagonalization.")

    def export_eigenvalues():
        global eigenvalues
    
        if eigenvalues is None:
            message = "No eigenvalues to export. Please calculate eigenvalues first."
            update_information(message)
            return
    
        # Open a file dialog to choose the save directory and file name
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    
        if file_path:
            with open(file_path, "w") as file:
                for i, eigenvalue in enumerate(eigenvalues):
                    file.write(f"{eigenvalue}\n")
        
            message = f"\nEigenvalues have been exported to {file_path}"
            update_information(message)
    # Create a new window for plotting eigenvalues
    eigenvalues_window = tk.Toplevel(root)
    eigenvalues_window.title("Eigenvalues Plot")
    eigenvalues_window.geometry("1400x1152")
    
    # Create a new figure for the eigenvalues plot
    eig_val_fig = plt.figure(figsize=(11,11))
    plt.bar(range(len(eigenvalues)), eigenvalues)
    plt.xlabel("Eigenvalue Index")
    plt.ylabel("Eigenvalue Value")
    plt.title("Eigenvalues Plot")
    
    # Create a separate canvas for the new figure
    eig_val_canvas = FigureCanvasTkAgg(eig_val_fig, master=eigenvalues_window)
    eig_val_canvas.get_tk_widget().pack(anchor='nw')
    #eig_val_canvas.get_tk_widget().bind("<Configure>", update_plot_size)
    eig_val_canvas.draw()
    eig_val_area_frame = tk.Frame(eigenvalues_window)
    eig_val_area_frame.place(x=1100, y=0, width=300, height=1100)
    eig_val_area = scrolledtext.ScrolledText(eig_val_area_frame, wrap=tk.WORD)
    eig_val_area.pack(expand=1, fill='both')
    default_text = "Output:\n~~~~~~~~~~\n"
    eig_val_area.insert(tk.INSERT, default_text)
    
    display_list_button = tk.Button(eigenvalues_window, text="Display as List", command=display_eigenvalues_list, width=50)
    display_list_button.pack(anchor='nw')

    export_button = tk.Button(eigenvalues_window, text="Export", command=export_eigenvalues, width=50)
    export_button.pack(anchor='nw')


    
##
# Function to display eigenvectors
def display_eigenvectors():
    global eigenvectors, has_diagonalized
    
    if not has_diagonalized:
        message = "No Hamiltonian present in global memory. Please Calculate the Hamiltonian Matrix first!\nFunction Terminating..."
        update_information(message)
        return
    
    def export_eigenvectors():
        global eigenvectors

        if eigenvectors is None:
            message = "No eigenvectors to export. Please calculate eigenvectors first."
            update_information(message)
            return

        # Open a file dialog to choose the save directory and file name
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, "w") as file:
                for i in range(eigenvectors.shape[1]):
                    file.write(f"Eigenvector {i + 1}:\n")
                    for j in range(eigenvectors.shape[0]):
                        file.write(f"{eigenvectors[j, i]}\n")
                    file.write("\n")

            message = f"Eigenvectors have been exported to {file_path}"
            update_information(message)
    
    # Create a new window for plotting eigenvectors
    eigenvectors_window = tk.Toplevel(root)
    eigenvectors_window.title("Eigenvectors Plot")

    # Create a subplot for each eigenvector
    num_eigenvectors = min(9, eigenvectors.shape[1])  # Display up to 9 eigenvectors
    fig, axs = plt.subplots(num_eigenvectors, 1, figsize=(12, 12))
    
    for i in range(num_eigenvectors):
        axs[i].plot(eigenvectors[:, i])
        axs[i].set_title(f"Eigenvector {i + 1}")
    
    plt.tight_layout()

    # Embed the Matplotlib plot in the Tkinter window
    eig_vec_canvas = FigureCanvasTkAgg(plt.gcf(), master=eigenvectors_window)
    eig_vec_canvas.get_tk_widget().pack()
    eig_vec_canvas.draw()
    
    export_button = tk.Button(eigenvectors_window, text="Export", command=export_eigenvectors, width=50, height=5)
    export_button.pack(anchor='nw')



def update_information(message):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    full_message = f'[{current_time}] Out:\n{message}\n~~~~~~~~~~\n'
    text_area.insert(tk.INSERT, full_message)
    text_area.see(tk.END)  # Scroll to the end
    
def update_color_scheme(*args):
    global color_scheme
    color_scheme = color_var.get()
    display_hamiltonian()
    
    
def update_model(*args):
    global model
    model = model_var.get()
    message = f"\nCurrent Model was set to: {model}"
    update_information(message)
    #fx 

def update_format(*args):
    global format_t
    format_t = format_t_var.get()
    message = f"\nExport format changed to: {format_t}"
    update_information(message)
    #fx 
    
    
    
###########
###########
# Create the main window
###########
###########
root = tk.Tk()
root.title("Quantum Sail ver1.0")
root.geometry("1880x1250")


############
############
# Create the central plot from TkAgg and matplotlib's backend
############
############
fig, ax = plt.subplots(figsize=(12,12))
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
canvas.get_tk_widget().place(x=200, y=0)




############
############
# Area on the Right for Output Prompt. Uses tkinters Scrolledtext module
############
############
text_area_frame = tk.Frame(root)
text_area_frame.place(x=1401, y=0, width=470, height=1000)
text_area = scrolledtext.ScrolledText(text_area_frame, wrap=tk.WORD)
text_area.pack(expand=1, fill='both', anchor='nw')
default_text = "Welcome! \nQuantum Many-Body Theory Calculator\nCurrent Ver: 1.0\nAuthor: Enea Çobo\nCurrent \
release date: 25 October 2023\nThe Following Software comes with Backend functionality from Matplotlib's graphing Capabilities \
as well as Tkinter for its GUI. It is currently capable of diagonalizing with scipy's modules, plotting Eigenvalues \
or Eigenvectors and explicitly importing or exporting Hamiltonian Operators in matrix format to undergo analysis. \
The current functioning models are the Bose and Fermi Hubbard models. Other quantum systems will be added in later \
patches. These will also include Classical analysis like Spin lattices through Monte Carlo methods such as Metropolis-Hastings \
or TDGL equations. Enjoy !\n.    .    .    .    .    .    .    .    .    .    .    .\n.    .    .    .    .    .    .    .    .    .    .    .\n~~~~~~~~~~\n"
text_area.insert(tk.INSERT, default_text)



############
############
# Chose the Model you want to compute
############
############

# Create a variable to store the selected model scheme
model_var = tk.StringVar()
model_var.set(model)  # Set the default model scheme which is model = 'Bose-Hubbard'

# Create the OptionMenu widget
model_option_menu = tk.OptionMenu(root, model_var, *models)
model_option_menu.pack(anchor='nw')

# Configure the width of the OptionMenu button
model_option_menu.config(width=25)  # Adjust the width as needed

# Attach a trace to update the model
model_var.trace("w", update_model)



############
############
# Create entry fields for bosons, sites, interaction potential, chemical potential, and hopping term
############
############
particles_label = tk.Label(root, text=f"Particles: {particles}")
particles_label.pack(anchor='nw')
particles_entry = tk.Entry(root)
particles_entry.pack(anchor='nw')

sites_label = tk.Label(root, text=f"Sites: {sites}")
sites_label.pack(anchor='nw')
sites_entry = tk.Entry(root)
sites_entry.pack(anchor='nw')

t_label = tk.Label(root, text=f"Hopping Term: {t}")
t_label.pack(anchor='nw')
t_entry = tk.Entry(root)
t_entry.pack(anchor='nw')

interaction_potential_label = tk.Label(root, text=f"Interaction Potential: {interaction_potential}")
interaction_potential_label.pack(anchor='nw')
interaction_potential_entry = tk.Entry(root)
interaction_potential_entry.pack(anchor='nw')

chemical_potential_label = tk.Label(root, text=f"Chemical Potential: {chemical_potential}")
chemical_potential_label.pack(anchor='nw')
chemical_potential_entry = tk.Entry(root)
chemical_potential_entry.pack(anchor='nw')






############
############
# Create "Apply" buttons for setting variables and get+plot hamiltonian
############
############
apply_all_button = tk.Button(root, text="Apply All Numbers", command=apply_all, width=20)
apply_all_button.pack(anchor='nw')
#
get_hamiltonian_button = tk.Button(root, text="Get Hamiltonian", command=get_hamiltonian, width=20)
get_hamiltonian_button.pack(anchor='nw')
#
display_button = tk.Button(root, text="Display Hamiltonian", command=display_hamiltonian, width=20)
display_button.pack(anchor='nw')
# Create a label to display the current numbers
state_text = f"Current Numbers:\n Particles: {particles}\n Sites: {sites} \n Hopping Term: {t} \n Interaction Potential: {interaction_potential}\n Chemical Potential: {chemical_potential}"
current_numbers_label = tk.Label(root, text=state_text)
current_numbers_label.pack(anchor='nw')


############
############
#Eigenpair commands and buttons
############
############

truncate_label = tk.Label(root, text=f"first k eigenpairs:")
truncate_label.pack(anchor='nw')
truncate_entry = tk.Entry(root)
truncate_entry.pack(anchor='nw')
#
apply_truncation_button = tk.Button(root, text="Apply k value", command=set_truncation, width=20)
apply_truncation_button.pack(anchor='nw')

diagonalize_button = tk.Button(root, text="diagonalization", command=diagonalize, width=20)
diagonalize_button.pack(anchor='nw')
#
display_eigenvalues_button = tk.Button(root, text="display eigenvalues", command=display_eigenvalues, width=20)
display_eigenvalues_button.pack(anchor='nw')
#
display_eigenvectors_button = tk.Button(root, text="display eigenvectors", command=display_eigenvectors, width=20)
display_eigenvectors_button.pack(anchor='nw')
#



###########
###########
#Buttons for plot manipulations and external options
###########
###########

# Create a variable to store the selected color scheme
color_var = tk.StringVar()
color_var.set(color_scheme)
color_option_menu = tk.OptionMenu(root, color_var, *color_schemes)
color_option_menu.pack()
color_option_menu.place(x=198, y=1200) 
color_option_menu.config(width=25)
color_var.trace("w", update_color_scheme)

#~~~

format_t_var = tk.StringVar()
format_t_var.set(format_t)
format_t_option_menu = tk.OptionMenu(root, format_t_var, *format_options)
format_t_option_menu.pack()
format_t_option_menu.place(x=390, y=1200)
format_t_option_menu.config(width=25)
format_t_var.trace("w", update_format)


#
##
###
####
# Start the GUI loop
####
###
##
#
root.mainloop()