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
