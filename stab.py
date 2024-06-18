

# globally accessible C functions
__stab_uniform = 0
__stab_normal  = 0
__stab_stable  = 0
__stab_stable4 = 0
__stab_uniform_fill  = 0
__stab_normal_fill   = 0
__stab_stable_fill   = 0
__stab_stable4_fill  = 0
__stab_mcculloch_fit = 0
#__stab_qfit  = 0


# internal function to initialize the C interface
def __setup_functions():
	global __stab_uniform
	global __stab_normal
	global __stab_stable
	global __stab_stable4
	global __stab_uniform_fill
	global __stab_normal_fill
	global __stab_stable_fill
	global __stab_stable4_fill
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

	__stab_stable4 = libstab.random_stable4
	__stab_stable4.argtypes = [c_double, c_double, c_double, c_double]
	__stab_stable4.restype = c_double

	__stab_uniform_fill = libstab.random_uniform_fill
	__stab_uniform_fill.argtypes = [POINTER(c_double), c_int]
	__stab_uniform_fill.restype = None

	__stab_normal_fill = libstab.random_normal_fill
	__stab_normal_fill.argtypes = [POINTER(c_double), c_int]
	__stab_normal_fill.restype = None

	__stab_stable_fill = libstab.random_stable_fill
	__stab_stable_fill.argtypes = [POINTER(c_double), c_int,
				c_double, c_double]
	__stab_stable_fill.restype = None

	__stab_stable4_fill = libstab.random_stable4_fill
	__stab_stable4_fill.argtypes = [POINTER(c_double), c_int,
				 c_double, c_double, c_double, c_double]
	__stab_stable4_fill.restype = None

	__stab_mcculloch_fit = libstab.mcculloch_fit
	__stab_mcculloch_fit.argtypes = [POINTER(c_double), c_int,
			POINTER(c_double), POINTER(c_double),
			POINTER(c_double), POINTER(c_double) ]
	__stab_mcculloch_fit.restype = None



# API
def uniform():
	""" Return a U(0,1) pseudorandom sample """
	__setup_functions()
	x = __stab_uniform()
	return x

# API
def normal():
	""" Return a N(0,1) pseudorandom sample """
	__setup_functions()
	x = __stab_normal()
	return x

# API
def stable(α, β):
	""" Return a S(α,β,1,0) pseudorandom sample, α∈[2,0[, β∈[-1,1] """
	__setup_functions()
	x = __stab_stable(α, β)
	return x

# API
def stable4(α, β, c, μ):
	""" Return a S(α,β,c,μ) pseudorandom sample, α∈[2,0[, β∈[-1,1] """
	__setup_functions()
	x = __stab_stable4(α, β, c, μ)
	return x

# API
def uniforms(n):
	""" Return a vector with n pseudorandom samples i.i.d. U(0,1) """
	from numpy import zeros
	from ctypes import POINTER, c_double
	__setup_functions()
	x = zeros(n)
	p = x.ctypes.data_as(POINTER(c_double))
	__stab_uniform_fill(p, n)
	return x

# API
def normals(n):
	""" Return a vector with n pseudorandom samples i.i.d. N(0,1) """
	from numpy import zeros
	from ctypes import POINTER, c_double
	__setup_functions()
	x = zeros(n)
	p = x.ctypes.data_as(POINTER(c_double))
	__stab_normal_fill(p, n)
	return x

# API
def stables(α, β, n):
	""" Return a vector with n stable samples i.i.d. S(α,β,1,0) """
	from numpy import zeros
	from ctypes import POINTER, c_double
	__setup_functions()
	x = zeros(n)
	p = x.ctypes.data_as(POINTER(c_double))
	__stab_stable_fill(p, n, α, β)
	return x

# API
def stables4(α, β, c, μ, n):
	""" Return a vector with n stable samples i.i.d. S(α,β,c,μ) """
	from numpy import zeros
	from ctypes import POINTER, c_double
	__setup_functions()
	x = zeros(n)
	p = x.ctypes.data_as(POINTER(c_double))
	__stab_stable4_fill(p, n, α, β, c, μ)
	return x

# API
def fit_quantiles(x):
	""" Fit stable parameters using McCulloch's quantile method """
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
version = 5

__all__ = [
		"uniform", "normal", "stable", "stable4",
		"uniforms", "normals", "stables", "stables4"
		"fit_quantiles",
	"version" ]
