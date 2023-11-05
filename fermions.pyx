# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 00:15:25 2023

@author: Enea Çobo

The following Code is intended as a package for Quantum Calculations
regarding fermionic systems in second quantization form. Currently present are
3 functions for 3 specific Hamiltonians. The general Fermi-Hubbard model, the general
Heisenberg model and the XXX model with an interaction in the z axis 
potential.
"""
##########
##########
# Imports
##########
##########
cimport cython
from libc.stdlib cimport malloc, free
from cython cimport sizeof
from builtins import bin
import numpy as np
cimport numpy as np
from math import comb


##########
##########
# The main struct for a state. with a function to print one.
# The struct holds an int with a binary representation, the physical size of the state
# and the normalization constant relevant for operators
##########
##########
ctypedef struct fstate:
    unsigned int state
    unsigned int size
    double norm_const
    
cpdef void print_fstate(fstate in_state):
    print(format(in_state.state, '0'+str(in_state.size)+'b'),"\n")
    

    
##########
##########
# The functions that perform checks and operations on bits of states
# -has_occupation checks if a certain site in a string of bits is a 1 or a 0
# the site is a number that starts from 1 not 0 and counts from the left
# like in the bra-ket notation

# -flip simply flips a 1 or a 0 to its opposite in a certain position in braket notation
##########
##########
cdef inline char has_occupation(fstate in_state, int site) nogil:
    #remember the bitwise transposition below starts from the left hence the minus operation. it gives the output in improper index (starts from 1 not 0)
    return (in_state.state >> (in_state.size - site) & 1)



# Brian Kernighan's Algorithm
@cython.boundscheck(False)
@cython.wraparound(False)
cdef int count_ones(fstate in_state, int in_index) nogil:
    cdef unsigned int count = 0
    cdef unsigned int mask = 1
    # Adjust the mask to consider the last site relevant digits
    mask = mask << (in_state.size - in_index)
    for i in range(in_index-1):
        mask = mask << 1
        if in_state.state & mask:
            count = count + 1
    return count


cdef fstate flip(fstate in_state, int flip_site) nogil:
    cdef fstate result
    result.norm_const = in_state.norm_const
    result.size = in_state.size
    result.state = in_state.state ^ ( 1 << (in_state.size - flip_site))
    return result






##########
##########
# The function to get the ordered fermion basis
# It takes a while to explain this one so take it for granted
##########
##########
@cython.boundscheck(False)
@cython.wraparound(False)
cdef fstate* get_basis(int nr_fermions, int nr_sites):
    cdef unsigned int basis_size = comb(nr_sites, nr_fermions)
    cdef fstate* basis = <fstate*>malloc(sizeof(fstate) * basis_size)
    cdef unsigned int i, state
    # Initialize state with the first combination of nr_fermions set bits
    state = (1 << nr_fermions) - 1
    cdef unsigned int x, y
    # Generate the basis states
    for i in range(basis_size):
        basis[i].state = state
        basis[i].size = nr_sites
        basis[i].norm_const = 1.0
        x = state & -state
        y = state + x
        state = ((state & ~y) // x) >> 1 | y
    return basis





##########
##########
# The functions for the main creation annahilation operators + others
# Very simply return a state depending on which operator acts on it
# The results are taken from Schwabl Quantum Mechanics II
##########
##########
cdef fstate apply_fcreator_nospin(fstate in_state, int site) nogil:
    cdef fstate result = in_state
    if has_occupation(in_state, site):
        result.norm_const = 0
    else:
        result.norm_const = (-1)**(count_ones(in_state, site))
        result.state = result.state ^ ( 1 << (result.size - site) )
    return result


cdef fstate apply_fannahilator_nospin(fstate in_state, int site) nogil:
    cdef fstate result = in_state
    if not (has_occupation(in_state, site)):
        result.norm_const = 0
    else:
        result.norm_const = (-1)**(count_ones(in_state, site))
        result.state = result.state ^ ( 1 << (result.size - site) )
    return result
    

cdef fstate number_operator(fstate in_state, int site) nogil:
    cdef fstate result = in_state
    if has_occupation(in_state, site):
        result.norm_const = 1.
    else:
        result.norm_const = 0.
    return result


cdef double contract_fstates(fstate in_state1, fstate in_state2) nogil:
    cdef double result = in_state1.norm_const * in_state2.norm_const
    if in_state1.state == in_state2.state:
        return result
    else:
        return 0.



##################################################
##################################################
# Here we will define methods and functions for the full Heisenberg model
# These simply include get methods for the tensort products of the pauli matrices
##################################################
##################################################

cdef double[:,:] get_paulix_j(int j, int N):
    cdef double[:,:] paulix = np.array([[0,1],[1,0]], dtype=np.double)
    cdef double[:,:] result
    if (j == 1):
        result = np.kron(paulix, np.identity(2**(N-1), dtype=np.double))
    elif (j!=1 and j!=N):
        result = np.kron(np.identity(2**(j-1), dtype=np.int64), paulix)
        result = np.kron(result, np.identity(2**(N-j), dtype=np.double))
    else:
        result = np.kron(np.identity(2**(N-1), dtype=np.int64), paulix)
    return result


cdef double complex[:,:] get_pauliy_j(int j, int N):
    cdef double complex[:,:] pauliy = np.array([[0.0 + 0.0j, 0.0 - 1.0j], [0.0 + 1.0j, 0.0 + 0.0j]], dtype=np.cdouble)
    cdef double complex[:,:] result
    if (j == 1):
        result = np.kron(pauliy, np.identity(2**(N-1), dtype=np.cdouble))
    elif (j != 1 and j != N):
        result = np.kron(np.identity(2**(j-1), dtype=np.int64), pauliy)
        result = np.kron(result, np.identity(2**(N-j), dtype=np.cdouble))
    else:
        result = np.kron(np.identity(2**(N-1), dtype=np.int64), pauliy)
    return result



cdef double[:,:] get_pauliz_j(int j, int N):
    cdef double[:,:] pauliz = np.array([[1,0],[0,-1]], dtype=np.double)
    cdef double[:,:] result
    if (j == 1):
        result = np.kron(pauliz, np.identity(2**(N-1), dtype=np.double))
    elif (j!=1 and j!=N):
        result = np.kron(np.identity(2**(j-1), dtype=np.double), pauliz)
        result = np.kron(result, np.identity(2**(N-j), dtype=np.double))
    else:
        result = np.kron(np.identity(2**(N-1), dtype=np.int64), pauliz)
    return result





##########
##########
# The main getter method for the hamiltonian and its CPython call function for future imports
# fermi_hamiltonian simply takes a matrix as input and iterates through the elements
# It then changes them according to which basis states are contracted with the Hamiltonian operator
# The summation over the Hopping term and Potential term are added for each element.

# The Fermi_Hubbard() creates the MeMview and starts a np array. It then runs the function above to edit it
# The basis pointer is then freed and set to NULL

# Below it the main call functions for the Full Heisenberg model and
# the XXX model in  a Z potential
##########
##########
@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline void fermi_hamiltonian(double[:,::1] arr, fstate* basis, int nr_fermions, int nr_sites, double t, double U, int basis_size) nogil:
    cdef size_t i, j
    cdef int k
    for i in range(basis_size):
        for j in range(basis_size):
            for k in range(nr_sites):
                arr[i, j] = arr[i, j] +\
                t*contract_fstates(basis[i], apply_fcreator_nospin(apply_fannahilator_nospin(basis[j], (k+2)%nr_sites), (k+1)%nr_sites)) +\
                t*contract_fstates(basis[i], apply_fcreator_nospin(apply_fannahilator_nospin(basis[j], (k+1)%nr_sites), (k+2)%nr_sites)) +\
                U*contract_fstates(basis[i], number_operator(basis[j], k+1))
                
                
cpdef double[:,::1] Fermi_Hubbard(int fermions, int sites, double t, double U):
    cdef fstate* basis = get_basis(fermions, sites)
    cdef int f_size = comb(sites, fermions)
    cdef double[:,::1] result = np.zeros((f_size, f_size), dtype=np.float64)
    fermi_hamiltonian(result, basis, fermions, sites, t, U, f_size)
    free(basis)
    basis = NULL
    return result


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double[:,::1] Heisenberg(double Jx, double Jy, double Jz, double hx, double hy, double hz, int N):
    cdef double[:,::1] result = np.zeros((<int>2**N, <int>2**N), dtype=np.cdouble)
    cdef int j, nr_sites
    nr_sites = N
    for j in range(nr_sites):
        result = result +\
            Jx*np.matmul(get_paulix_j((j%N)+1, N), get_paulix_j((j+1)%N+1, N)) +\
            Jy*np.matmul(get_pauliy_j((j%N)+1, N), get_pauliy_j((j+1)%N+1, N)) +\
            Jz*np.matmul(get_pauliz_j((j%N)+1, N), get_pauliz_j((j+1)%N+1, N)) +\
            np.multiply(hx, get_paulix_j(j+1, N)) +\
            np.multiply(hy, get_pauliy_j(j+1, N)) +\
            np.multiply(hz, get_pauliz_j(j+1, N))                      
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double[:,::1] XXX(double Jx, double hz, int N):
    cdef double[:,::1] result = np.zeros((<int>2**N, <int>2**N), dtype=np.double)
    cdef int j, nr_sites
    nr_sites = N
    for j in range(nr_sites):
        result = result +\
            Jx*np.matmul(get_paulix_j((j%N)+1, N), get_paulix_j((j+1)%N+1, N)) +\
            np.multiply(hz, get_pauliz_j(j+1, N))
    return result


