# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 02:30:21 2023

@author: Enea
"""

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

