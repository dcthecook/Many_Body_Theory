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
cdef int count_ones(fstate in_fstate, int in_index) nogil:
    cdef unsigned int count = 0
    cdef unsigned int mask = 1
    # Adjust the mask to consider the last site relevant digits
    mask = mask << (in_fstate.size - in_index)
    for i in range(in_index-1):
        mask = mask << 1
        if in_fstate.state & mask:
            count = count + 1
        if (2*in_fstate.state<<in_fstate.state) & mask:
            count = count + 1
    return count

#test
cdef fstate test
test.state = 33
test.size = 4
test.norm_const = 1
print(count_ones(test, 2))


# could give int overflow in the 2*in_fstate.state line
# for example a 16 site fermion system with spin can fill the entire 32bit int
# set for example
# test.state = 4294967295
# test.size = 16
# test.norm_const = whatever
# test if this actually gives overflow.
# the correct answer is 2*(16-in_index) ^-^


"""
PROPOSED CHANGES:
create 2 masks
cdef int mask1 = 1  #which is 2**0
cdef int mask2 = <int>2**in_fstate.size  #this guarantees the second mask has a 1 where the half array is
# so for size = 3 the mask2 is 001000 and mask 1 = 000001
enter for loop once and both if statements SHOULD? remain the exact same with only changing mask
    for i in range(in_index-1):
        mask1 = mask1 << 1
        if in_fstate.state & mask1:
            count = count + 1
        if in_fstate.state & mask2:
            count = count + 1
"""
#^_^ test further


"""
After finishing testing the count_ones() fx above have to move to the operators
First the has_occupation_spin() fx has to be created which is the counterpart of has_occupation(fstate in_state, int site)
It will be passed another argument (char spin) which will be either 0 or 1 from the user
If 0 the function will check if down-spin electrons exist at the given index
This means the fx has to take into account the left half of the in_state.state with regards to in_state.size
If 1 the function will check the right half if it is occupied at that index
!!Care for index algebra

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
