# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 09:59:52 2023

@author: Enea
"""
cimport cython
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt
from cython cimport sizeof
from libc.math cimport pi, exp
import numpy as np
cimport numpy as np

cdef struct primitive_gaussian:
    double alpha
    double coeff
    double[3] coordinates
    double A #norm_const
    double l1
    double l2
    double l3
    
cdef struct Atom:
    primitive_gaussian* functions
    int nr_functions
    
cdef struct Molecule:
    Atom* atoms
    int nr_atoms
    
    
cdef primitive_gaussian create_gauss(double inalpha, double incoeff, double[3] incoords) nogil:
    cdef primitive_gaussian result
    result.alpha = inalpha
    result.coeff = incoeff
    result.coordinates[0] = incoords[0]
    result.coordinates[1] = incoords[1]
    result.coordinates[2] = incoords[2]
    result.A = (2.0 * inalpha/pi)**0.75
    result.l1 = 0
    result.l2 = 0
    result.l3 = 0
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef Atom create_atom(double[::1] alphas, double[::1] coeffs, double[3] coords, int nr_gaussians) nogil:
    cdef Atom result_atom
    result_atom.functions = <primitive_gaussian*>malloc(nr_gaussians*sizeof(primitive_gaussian))
    result_atom.nr_functions = nr_gaussians
    cdef int i
    for i in range(result_atom.nr_functions):
        result_atom.functions[i] = create_gauss(alphas[i], coeffs[i], coords)
    return result_atom


@cython.boundscheck(False)
@cython.wraparound(False)
cdef Molecule create_molecule(Atom* atom_list, int total_atoms) nogil:
    cdef Molecule result_molec
    result_molec.atoms = <Atom*>malloc(total_atoms*sizeof(Atom))
    result_molec.nr_atoms = total_atoms
    cdef int i
    for i in range(result_molec.nr_atoms):
        result_molec.atoms[i] = atom_list[i]
    return result_molec

cdef void free_Atom(Atom inatom) nogil:
    free(inatom.functions)
    inatom.functions = NULL
    
cdef void free_Molecule(Molecule inmolec) nogil:
    cdef int i
    for i in range(inmolec.nr_atoms):
        free_Atom(inmolec.atoms[i])
    free(inmolec.atoms)
    inmolec.atoms = NULL

cdef void print_molecule(Molecule in_molec):
    cdef int i, j
    print(f"nr of atoms:{in_molec.nr_atoms}\n")
    for i in range(in_molec.nr_atoms):
        print("\n", i + 1, " Atom:\n~~~\n")
        for j in range(in_molec.atoms[i].nr_functions):
            print("\n####gauss-fx:", j + 1, "\n####")
            print("\nalpha:", in_molec.atoms[i].functions[j].alpha)
            print("\ncoefficient:", in_molec.atoms[i].functions[j].coeff)
            print("\ncoords:[", in_molec.atoms[i].functions[j].coordinates[0], ",", \
                  in_molec.atoms[i].functions[j].coordinates[1], ",", \
                  in_molec.atoms[i].functions[j].coordinates[2], "]\n")
                #find a way to put last print statement INSIDE the i loop without
                #accessing forbidden memory of the j index


cdef double* sub3(double[3] vec1, double[3] vec2) nogil:
    cdef double[3] result
    result[0] = vec1[0]-vec2[0]
    result[1] = vec1[1]-vec2[1]
    result[2] = vec1[2]-vec2[2]
    return result

cdef double dot3(double[3] vec1, double[3] vec2) nogil:
    cdef double result = 0
    result = result + vec1[0]*vec2[0]
    result = result + vec1[1]*vec2[1]
    result = result + vec1[2]*vec2[2]
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double** zeros(int rows, int cols) nogil: 
    cdef size_t i, j, k
    cdef double** result = <double**>malloc(rows*sizeof(double*))
    for i in range(rows):
        result[i] = <double*>malloc(cols*sizeof(double))
    for j in range(rows):
        for k in range(cols):
            result[j][k] = 0.    
    return result 


@cython.boundscheck(False)
@cython.wraparound(False)
cdef void free_2D(double** arr, int rows) nogil: 
    cdef size_t i
    for i in range(rows):
        free(arr[i])
        arr[i] = NULL
    free(arr)
    arr = NULL


@cython.boundscheck(False)
@cython.wraparound(False)
cdef void printarr(double** arr, int rows, int cols):
    for i in range(rows):
        for j in range(cols):
            print(f"{arr[i][j]:.9f}", end="\t")
        print()


@cython.boundscheck(False)
@cython.wraparound(False)
cdef double** overlap(Molecule molecule) nogil:
    cdef int i, j, k, l
    cdef int nbasis = molecule.nr_atoms
    cdef double** S = zeros(nbasis, nbasis)
    cdef int nprimitives_i, nprimitives_j 
    cdef double N, p, q, Q2
    cdef double[3] Q
    #
    for i in range(nbasis):
        for j in range(nbasis):
            nprimitives_i = (molecule.atoms[i].nr_functions)
            nprimitives_j = (molecule.atoms[j].nr_functions)
            for k in range(nprimitives_i):
                for l in range(nprimitives_j):         
                    N = molecule.atoms[i].functions[k].A * molecule.atoms[j].functions[l].A
                    p = molecule.atoms[i].functions[k].alpha + molecule.atoms[j].functions[l].alpha
                    q = molecule.atoms[i].functions[k].alpha * molecule.atoms[j].functions[l].alpha / p
                    Q = sub3(molecule.atoms[i].functions[k].coordinates, molecule.atoms[j].functions[l].coordinates)
                    Q2 = dot3(Q,Q)
                    S[i][j] += N * molecule.atoms[i].functions[k].coeff * molecule.atoms[j].functions[l].coeff * exp(-q*Q2) * (pi/p)**(3/2)
    return S

##################################################
##################################################
# Hydrogen STO-3G basis
#      alphas and coeffs
#      0.3425250914E+01       0.1543289673E+00
#      0.6239137298E+00       0.5353281423E+00
#      0.1688554040E+00       0.4446345422E+00
#create hydrogen test unit for structs
##################################################
##################################################

cdef double[3] Hcoords1 = [0,0,0]
cdef double[3] Hcoords2 = [2,0,0]
cdef double[::1] Halphas = np.array([0.3425250914E+01,0.6239137298E+00,0.1688554040E+00])
cdef double[::1] Hcoeffs = np.array([0.1543289673E+00,0.5353281423E+00,0.4446345422E+00])
cdef Atom Hydrogen1 = create_atom(Halphas, Hcoeffs, Hcoords1, 3)
cdef Atom Hydrogen2 = create_atom(Halphas, Hcoeffs, Hcoords2, 3)
cdef Atom* atomlist = <Atom*>malloc(2*sizeof(Atom))
atomlist[0] = Hydrogen1
atomlist[1] = Hydrogen2
cdef Molecule H2 = create_molecule(atomlist, 2)

cdef double** test = overlap(H2)

printarr(test, H2.nr_atoms, H2.nr_atoms)

free_Molecule(H2)
free(atomlist)
atomlist = NULL
free_2D(test, H2.nr_atoms)