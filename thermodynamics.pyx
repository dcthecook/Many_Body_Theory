# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 08:42:21 2023

@author: Enea
"""

###############
###############
# This package focuses on getting the thermodynamic functions
# after diagonalizing the hamiltonian

# work in progress
###############
###############

import numpy as np
cimport numpy as np
cimport cython
from math cimport exp

cdef double partition_function(double beta, double[::1] eigenvalues):
    cdef double result = np.sum(exp(-beta*eigenvalues))
    return result

cdef double[:,::1] density_matrix(double part_fx, double[::1] eigenvalues, double[:,::1] eigenvectors):
    cdef double result = np.zeros()