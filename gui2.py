# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 18:50:18 2023

@author: Enea
"""



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
