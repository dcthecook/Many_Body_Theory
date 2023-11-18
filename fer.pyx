# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:42:50 2023

@author: burbiee
"""

# Imports

cimport cython
from libc.stdlib cimport malloc, free
from cython cimport sizeof
from builtins import bin #testing
import numpy as np
cimport numpy as np
from math import comb


# The main struct for a femion state (with a function to print one)
# @state: int in a binary representation, 
# @size: the physical size of the state
# @norm_const: normalization constant (relevant for operators)
# e.g. 
# cdef fstate test
# test.state = 10
# test.size = 1
# test.norm_const = 1
# print_fstate(test)

ctypedef struct fstate:
    unsigned int state
    unsigned int size
    double norm_const
    
cpdef void print_fstate(fstate in_state):
    print(format(in_state.state, '0'+str(in_state.size)+'b'),"\n")
    
# Brian Kernighan's Algorithm (counting ones in a fstate)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef int count_ones_spin(fstate in_fstate, int in_index) nogil:
    cdef unsigned int count = 0
    cdef unsigned int mask1 = 1
    cdef unsigned int mask2 = <int>2**in_fstate.size
    # Adjust the mask1 to consider the last site relevant digits
    mask1 = mask1 << (in_fstate.size - in_index)
    mask2 = mask2 << (in_fstate.size - in_index)
    for i in range(in_index-1):
        mask1 = mask1 << 1
        mask2 = mask2 << 1
        if in_fstate.state & mask1:
            count = count + 1
        if in_fstate.state & mask2:
            count = count + 1
    return count


# has_occupation functions checks if @in_fstate has an up or down @spin at a @site
# @site is a number that starts from 1 and counts from the left
# returns 0 r 1

cdef inline int has_occupation_spin(fstate in_fstate, int site, int spin) nogil:
    if spin:
        return in_fstate.state >> (in_fstate.size - site) & 1
    else:
        return in_fstate.state >> (2*in_fstate.size - site) & 1
    

# flip_spin method returns a state with a flipped @spin at @flip_site

cdef fstate flip_spin(fstate in_fstate, int flip_site, int spin) nogil:
    cdef fstate result = in_fstate
    if spin: 
        result.state = in_fstate.state ^ ( 1 << (in_fstate.size - flip_site))
    else:
        result.state = in_fstate.state ^ ( 1 << (2*in_fstate.size - flip_site))
    return result


# annihilation operator
# returns a state and changes the norm of @result

cdef fstate apply_fannihilator_spin(fstate in_fstate, int site, int spin) nogil:
    cdef fstate result = in_fstate
    if has_occupation_spin(in_fstate, site, spin):
        result = flip_spin(in_fstate, site, spin)
        result.norm_const = in_fstate.norm_const * ((-1)**(count_ones_spin(in_fstate, site)))
    else:
        result.norm_const = result.norm_const*0
    return result


# creator operator
# returns a state

cdef fstate apply_fcreator_spin(fstate in_fstate, int site, int spin) nogil:
    cdef fstate result = in_fstate
    if has_occupation_spin(in_fstate, site, spin):
        result.norm_const = result.norm_const*0
    else:
        result = flip_spin(in_fstate, site, spin)
        result.norm_const = result.norm_const*((-1)**(count_ones_spin(in_fstate, site)))
    return result

# number operator 

cdef fstate apply_numberOp_spin(fstate in_fstate, int site, int spin) nogil:
    cdef fstate result = in_fstate
    if has_occupation_spin(in_fstate, site, spin):
        result.norm_const = result.norm_const*1.
    else:
        result.norm_const = result.norm_const*0.
    return result


# tests
cdef fstate test
test.state = 4294967295
test.size = 16
test.norm_const = 1

cdef fstate test1
test1.state = 172
test1.size = 4
test1.norm_const = 1

print("count_ones_spin test:")
print("expected value: 30. output:", count_ones_spin(test, 16))


print("flip_spin test, spin down:")
print("expected state value: 44. output:", flip_spin(test1, 3, 0))

print("flip_spin test, spin up:")
print("expected state value: 164. output:", flip_spin(test1, 1, 1))


print("apply_fannihilator_spin tests")
# test spin down, occupation 0
print("expected value: 172. output:", apply_fannihilator_spin(test1, 2, 0))

# test spin up, occupation 0,
print("expected value: 172. output:", apply_fannihilator_spin(test1, 3, 1))

# test spin down, occupation 1
print("expected value: 140. output:", apply_fannihilator_spin(test1, 3, 0))

# test spin up, occupation 1
print("expected value: 164. output:", apply_fannihilator_spin(test1, 1, 1))


print("apply_fcreator_spin tests")
# test spin down, occupation 0
print("expected value: 172. output:", apply_fcreator_spin(test1, 2, 0))

# test spin up, occupation 0,
print("expected value: 174. output:", apply_fcreator_spin(test1, 3, 1))

# test spin down, occupation 1
print("expected value: 172. output:", apply_fcreator_spin(test1, 3, 0))

# test spin up, occupation 1
print("expected value: 172. output:", apply_fcreator_spin(test1, 1, 1))


print("apply_numberOp_spin tests:")
# test spin down, occupation 0
print("expected value: 0. output:", apply_numberOp_spin(test1, 2, 0))

# test spin up, occupation 0,
print("expected value: 0. output:", apply_numberOp_spin(test1, 3, 1))

# test spin down, occupation 1
print("expected value: 1. output:", apply_numberOp_spin(test1, 3, 0))

# test spin up, occupation 1
print("expected value: 1. output:", apply_numberOp_spin(test1, 1, 1)
