# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 09:59:52 2023

@author: Enea
"""
cimport cython
from libc.stdlib cimport malloc, free
from libc.math cimport sqrt
from cython cimport sizeof
from libc.math cimport pi
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
    for i in range(i):
        free_Atom(inmolec.atoms[i])
    free(inmolec.atoms)
    inmolec.atoms = NULL

cdef void print_molecule(Molecule in_molec):
    cdef int i = 0
    cdef int j = 0
    print(f"nr of atoms:{in_molec.nr_atoms}\n")
    for i in range(in_molec.nr_atoms):
        print("\n",i+1 ," Atom:\n~~~\n")
        print("\ncoords:[", in_molec.atoms[i].functions[j].coordinates[0],",",\
              in_molec.atoms[i].functions[j].coordinates[1],",",\
                in_molec.atoms[i].functions[j].coordinates[2],"]\n")
        for j in range(in_molec.atoms[i].nr_functions):
            print("\n####gauss-fx:", j+1,"\n####")
            print("\nalpha:", in_molec.atoms[i].functions[j].alpha)
            print("\ncoefficient:", in_molec.atoms[i].functions[j].coeff)
            
            print("\nnorm_const=",in_molec.atoms[i].functions[j].A)
            #print l1 l2 l3 statemtns
            


    

##################################################
##################################################
# Hydrogen STO-3G basis
#      alphas and coeffs
#      0.3425250914E+01       0.1543289673E+00
#      0.6239137298E+00       0.5353281423E+00
#      0.1688554040E+00       0.4446345422E+00
##################################################
##################################################
#create hydrogen test unit for structs

cdef double[3] Hcoords1 = [0,0,0]
cdef double[3] Hcoords2 = [0,0,1.4]
cdef double[::1] Halphas = np.array([0.3425250914E+01,0.6239137298E+00,0.1688554040E+00])
cdef double[::1] Hcoeffs = np.array([0.1543289673E+00,0.5353281423E+00,0.4446345422E+00])
cdef Atom Hydrogen1 = create_atom(Halphas, Hcoeffs, Hcoords1, 3)
cdef Atom Hydrogen2 = create_atom(Halphas, Hcoeffs, Hcoords2, 3)
cdef Atom* atomlist = <Atom*>malloc(2*sizeof(Atom))
atomlist[0] = Hydrogen1
atomlist[1] = Hydrogen2
cdef Molecule H2 = create_molecule(atomlist, 2)

print_molecule(H2)
free_Molecule(H2)
free(atomlist)
atomlist = NULL