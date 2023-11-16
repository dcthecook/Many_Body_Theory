##########
##########
# Imports
##########
##########
cimport cython
from libc.stdlib cimport malloc, free
from cython cimport sizeof
from builtins import bin #testing
import numpy as np
cimport numpy as np
from math import comb


##########
##########
# The main struct for a state. with a function to print one.
# The struct holds an int with a binary representation, the physical size of the state
# and the normalization constant relevant for operators
# e.g. cdef fstate test
# e.g test.state = 10
# test.size = 1
# test.norm_const = 1
# print_fstate(test)
##########
##########
ctypedef struct fstate:
    unsigned int state
    unsigned int size
    double norm_const
    
cpdef void print_fstate(fstate in_state):
    print(format(in_state.state, '0'+str(in_state.size)+'b'),"\n")
    
# Brian Kernighan's Algorithm
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

#test
cdef fstate test
test.state = 4294967295
test.size = 16
test.norm_const = 1
print("expected value: 30. output:", count_ones_spin(test, 16))

##########
##########
# The functions checks if @in_fstate has an up or down @spin at a @site
# @site is a number that starts from 1 and counts from the left
##########
##########

cdef inline int has_occupation(fstate in_fstate, int site, int spin) nogil:
    if spin:
        return in_fstate.state >> (in_fstate.size - site) & 1
    else:
        return in_fstate.state >> (2*in_fstate.size - site) & 1

#test
print(has_occupation(test, 16, "bob"))



"""
The 3 basic operators in the spinless code are
apply_fannahilator_nospin(fstate in_state, int site)
apply_fcreator_nospin(fstate in_state, int site)
number_operator(fstate in_state, int site)

these need duplicates for the spin system counterpart

apply_fannahilator_spin(fstate in_state, int site, char spin)
apply_fcreator_spin(fstate in_state, int site, char spin)
number_operator_spin(fstate in_state, int site, char spin)

where char is an 8-bit mem block
ideally we can use int and represent the spin as 0 or 1 but because these fx
will be called millions of times you can save 8x more registry memory with temp variables
another way, because these are meant to be read and not modified
is to make the input a char* pointer. Passing by reference instead of by value is much faster

so you create globals
cdef char down_representation = 0
cdef char up_representation = 1
cdef char* down = &down_representation
cdef char* up = &up_representation

and then you can for example do has_occupation(fstate=test_state, index=6, spin=down)
this may need more troubleshooting

"""
