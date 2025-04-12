import os
import ctypes

# Load the underlying shared library.
# Adjust the path and extension as needed for your platform.
_lib_dir = os.path.join(os.path.dirname(__file__))
_lib_name = "libCO2CO2.so"  # Change to "libmbCO2CO2.dylib" or "mbCO2CO2.dll" if necessary
_lib_path = os.path.join(_lib_dir, _lib_name)

try:
    lib = ctypes.CDLL(_lib_path)
except OSError as e:
    raise RuntimeError(f"Unable to load shared library {_lib_path}: {e}")

#
# Set up the function prototypes.
# We assume that the C library (mbCO2CO2) exposes three functions:
#
# double p2b(double* input);
# double p1b(double* input);
# double sapt(double* input);
#
# Adjust these prototypes as needed.
#

lib.p2b.restype = ctypes.c_double
lib.p2b.argtypes = [ctypes.POINTER(ctypes.c_double)]

lib.p1b.restype = ctypes.c_double
lib.p1b.argtypes = [ctypes.POINTER(ctypes.c_double)]

lib.sapt.restype = ctypes.c_double
lib.sapt.argtypes = [ctypes.POINTER(ctypes.c_double)]


def p2b(xyz):
    """
    Python wrapper for mbCO2CO2_p2.

    Args:
        xyz (list of float): List of numeric values to be passed to the C function.

    Returns:
        float: The return value from mbCO2CO2_p2.
    """
    xyz_array = (ctypes.c_double * len(xyz))(*xyz)
    return lib.p2b(xyz_array)


def p1b(xyz):
    """
    Python wrapper for mbCO2CO2_p1.

    Args:
        xyz (list of float): List of numeric values to be passed to the C function.

    Returns:
        float: The return value from mbCO2CO2_p1.
    """
    xyz_array = (ctypes.c_double * len(xyz))(*xyz)
    return lib.p1b(xyz_array)


def sapt(xyz):
    """
    Python wrapper for mbCO2CO2_sapt.

    Args:
        xyz (list of float): List of numeric values to be passed to the C function.

    Returns:
        float: The output value from mbCO2CO2_sapt.
    """
    xyz_array = (ctypes.c_double * len(xyz))(*xyz)
    return lib.sapt(xyz_array)