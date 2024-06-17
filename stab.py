

# globally accessible C functions
__stab_uniform = 0
__stab_normal  = 0
__stab_stable  = 0
__stab_uniform_fill = 0
__stab_normal_fill  = 0
__stab_stable_fill  = 0
__stab_mcculloch_fit  = 0
#__stab_qfit  = 0


# internal function to initialize the C interface
def __setup_functions():
	global __stab_uniform
	global __stab_normal
	global __stab_stable
	global __stab_uniform_fill
	global __stab_normal_fill
	global __stab_stable_fill
	global __stab_mcculloch_fit
	if __stab_uniform != 0: return

	from os.path import abspath, dirname
	from ctypes import CDLL, POINTER, c_double, c_int

	libstab = CDLL(f"{abspath(dirname(__file__))}/libstab.so")

	__stab_uniform = libstab.random_uniform
	__stab_uniform.argtypes = None
	__stab_uniform.restype = c_double

	__stab_normal = libstab.random_normal
	__stab_normal.argtypes = None
	__stab_normal.restype = c_double

	__stab_stable = libstab.random_stable
	__stab_stable.argtypes = [c_double, c_double]
	__stab_stable.restype = c_double

	__stab_uniform_fill = libstab.random_uniform_fill
	__stab_uniform_fill.argtypes = [POINTER(c_double), c_int]
	__stab_uniform_fill.restype = None

	__stab_normal_fill = libstab.random_normal_fill
	__stab_normal_fill.argtypes = [POINTER(c_double), c_int]
	__stab_normal_fill.restype = None

	__stab_stable_fill = libstab.random_stable_fill
	__stab_stable_fill.argtypes = [POINTER(c_double), c_int, c_double, c_double]
	__stab_stable_fill.restype = None

	__stab_mcculloch_fit = libstab.mcculloch_fit
	__stab_mcculloch_fit.argtypes = [POINTER(c_double), c_int,
			POINTER(c_double), POINTER(c_double),
			POINTER(c_double), POINTER(c_double) ]
	__stab_mcculloch_fit.restype = None



# API
def uniform():
	__setup_functions()
	x = __stab_uniform()
	return x

# API
def normal():
	__setup_functions()
	x = __stab_normal()
	return x

# API
def stable(α, β):
	__setup_functions()
	x = __stab_stable(α, β)
	return x

# API
def uniforms(n):
	import numpy
	from ctypes import POINTER, c_double
	__setup_functions()
	x = numpy.zeros(n)
	p = x.ctypes.data_as(POINTER(c_double))
	__stab_uniform_fill(p, n)
	return x

# API
def normals(n):
	import numpy
	from ctypes import POINTER, c_double
	__setup_functions()
	x = numpy.zeros(n)
	p = x.ctypes.data_as(POINTER(c_double))
	__stab_normal_fill(p, n)
	return x

# API
def stables(α, β, n):
	import numpy
	from ctypes import POINTER, c_double
	__setup_functions()
	x = numpy.zeros(n)
	p = x.ctypes.data_as(POINTER(c_double))
	__stab_stable_fill(p, n, α, β)
	return x

# API
def fit_quantiles(x):
	from ctypes import POINTER, c_double
	from numpy import ascontiguousarray
	__setup_functions()
	pp = ascontiguousarray(x, dtype='float64')
	p = pp.ctypes.data_as(POINTER(c_double))
	n = x.size
	α = c_double()
	β = c_double()
	c = c_double()
	z = c_double()
	__stab_mcculloch_fit(p, n, α, β, c, z)
	return α.value, β.value, c.value, z.value



# API
def read(filename):
	"""Read an image file into a numpy array of floats"""
	from ctypes import c_int
	from numpy.ctypeslib import as_array

	__setup_functions()

	w = c_int()
	h = c_int()
	d = c_int()

	p = __iio_read(filename.encode('utf-8'), w, h, d)
	x = as_array(p, (h.value, w.value, d.value)).copy()
	__libc_free(p)
	return x


# API
def write(filename, x):
	"""Write a numpy array into a named file"""
	from numpy import ascontiguousarray

	__setup_functions()

	h = x.shape[0]
	w = len(x.shape) <= 1 and 1 or x.shape[1]
	d = len(x.shape) <= 2 and 1 or x.shape[2]

	p = ascontiguousarray(x, dtype='float32')
	__iio_write(filename.encode('utf-8'), p, w, h, d)




# API
version = 2

__all__ = [
		"uniform", "normal", "stable",
		"uniforms", "normals", "stables",
		"fit_quantiles",
	"version" ]
