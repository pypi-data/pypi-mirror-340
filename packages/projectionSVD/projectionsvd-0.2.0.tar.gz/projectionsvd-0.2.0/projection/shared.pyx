# cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
import numpy as np
cimport numpy as np
from cython.parallel import prange
from libc.stdint cimport uint8_t, uint32_t

# Expand data into full genotype matrix
cpdef void expandGeno(
		const uint8_t[:,::1] B, uint8_t[:,::1] G
	) noexcept nogil:
	cdef:
		uint8_t[4] recode = [2, 9, 1, 0]
		uint8_t mask = 3
		uint8_t byte
		uint8_t* g
		uint32_t M = G.shape[0]
		uint32_t N = G.shape[1]
		uint32_t N_b = B.shape[1]
		size_t i, j, b, bytepart
	for j in prange(M):
		i = 0
		g = &G[j,0]
		for b in range(N_b):
			byte = B[j,b]
			for bytepart in range(4):
				g[i] = recode[byte & mask]
				byte = byte >> 2
				i = i + 1
				if i == N:
					break

# Standardize batched genotype matrix
cpdef void standardizeE(
		double[:,::1] E, uint8_t[:,::1] G, const double[::1] f, const double[::1] d, const uint32_t m
	) noexcept nogil:
	cdef:
		uint8_t* g
		uint32_t M = E.shape[0]
		uint32_t N = E.shape[1]
		double a, b
		size_t i, j, k
	for j in prange(M):
		k = m + j
		a = 2.0*f[k]
		b = d[k]
		g = &G[k,0]
		for i in range(N):
			if g[i] == 9:
				E[j,i] = 0.0
			else:
				E[j,i] = (<double>g[i] - a)*b
