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

cdef inline int has_occupation(fstate in_fstate, int site, int spin) nogil:
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


# annahilation operator
# returns a state and changes the norm of @result

cdef fstate apply_fannahilator_spin(fstate in_fstate, int site, int spin) nogil:
    cdef fstate result = in_fstate
    if has_occupation_spin(in_fstate, site, spin):
        result = flip_spin(in_fstate, site, spin)
        result.norm_const = in_fstate.norm_const * ((-1)**(count_ones_spin(in_fstate, site)))
    else:
        result.norm_const = result.norm_const*0
    return result


#tests
#count_ones_spin test
cdef fstate test
test.state = 4294967295
test.size = 16
test.norm_const = 1
print("expected value: 30. output:", count_ones_spin(test, 16))

# flip_spin test, spin down
cdef fstate test1
test1.state = 172
test1.size = 4
test1.norm_const = 1
print("expected state value: 44. output:", flip_spin(test1, 3, 0))

# flip_spin test, spin up
print("expected state value: 164. output:", flip_spin(test1, 1, 1))

#apply_fannahilator_spin test
cdef fstate test2
test2.state = 172
test2.size = 4
test2.norm_const = 1

#test spin down, occupation 0
print("expected value: 172. output:", apply_fannahilator_spin(test2, 2, 0))

#test spin up, occupation 0,
print("expected value: 172. output:", apply_fannahilator_spin(test2, 3, 1))

#test spin down, occupation 1
print("expected value: 140. output:", apply_fannahilator_spin(test2, 3, 0))

#test spin up, occupation 1
print("expected value: 164. output:", apply_fannahilator_spin(test2, 1, 1))

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
