# Molecule Potential Energy Library

This project provides a high-performance C++ library for calculating the potential energy of a CO₂ molecular system. The C++ routines are exposed to Python via both a ctypes-based wrapper and a (optional) pybind11 module, allowing you to leverage the speed of C++ with the ease-of-use of Python.

## Project Structure

```
molecule-potential/            # Root directory
├── src/                     # C++ source files
│   ├── mbCO2CO2.cpp         # Implements the energy routines and exports functions
│   ├── mbCO2CO2.h           # Declarations for the energy routine functions:
│   │                         //   double p1b(double* xyz);
│   │                         //   double p2b(double* xyz);
│   │                         //   double sapt(double* xyz);
│   └── ... (other files)
├── python/                  # (Optional) pybind11 C++ binding module source
│   └── module.cpp           # Implements a Python module using pybind11
├── wrapper.py               # Python wrapper using ctypes to load the shared library
├── CMakeLists.txt           # CMake configuration to build the shared libraries
├── setup.py                 # Setup script for building and packaging the project for PyPI
├── README.md                # This file
└── LICENSE                  # License file (e.g., MIT License)
```

## Installation

### Prerequisites

- A C++ compiler and [CMake](https://cmake.org/) (version 3.10 or above)
- [Python 3.6+](https://www.python.org/) with pip

### Build the C++ Shared Library

This project uses CMake to build two targets:
- **potential_energy**: The core shared library built from all C++ source files in the `src/` directory.
- **molecule_module**: A Python module (using pybind11) that links against `potential_energy` (optional if you prefer the ctypes wrapper).

To build the shared library:

1. Open a terminal in the project root and create a build directory:

   ```bash
   mkdir build
   cd build
   ```

2. Run CMake and build:

   ```bash
   cmake ..
   make
   ```

   The `molecule_module` shared library will be placed in `build/python` as defined in the `CMakeLists.txt`. The core shared library built from your `src/` files will be named (for example) `libCO2CO2.so`.

### Install the Package

The project can be installed as a Python package using pip. The provided `setup.py` script calls a custom build command to build the C++ shared library before packaging.

From the project root, run:

```bash
pip install .
```

This process will:
- Build the C++ shared library (via CMake or Makefile as configured).
- Package the Python wrapper (and optionally the pybind11 module) along with the shared library so that they can be imported in Python.

## Usage

You can access the energy routines through the `wrapper.py` interface (which uses ctypes to load the shared library). For example:

```python
from wrapper import p1b, p2b, sapt

# Example coordinates for 6 atoms (each atom has 3 coordinates);
# adjust these values as required by your application:
xyz = [
    0.0,  0.0,  0.000,   # Atom 1 (C)
    0.0,  0.0, -1.162,   # Atom 2 (O)
    0.0,  0.0,  1.162,   # Atom 3 (O)
    7.0,  0.0,  0.000,   # Atom 4 (C)
    7.0,  0.0, -1.162,   # Atom 5 (O)
    7.0,  0.0,  1.162    # Atom 6 (O)
]

energy_p1 = p1b(xyz)
energy_p2 = p2b(xyz)
energy_sapt = sapt(xyz)

print("Energy from p1b:", energy_p1)
print("Energy from p2b:", energy_p2)
print("Energy from sapt:", energy_sapt)
```

> **Note:** If you built the pybind11 module (from `python/module.cpp`), you can alternatively import the module (e.g., `import co2_potential`) and call its functions (provided they are bound similarly to the ctypes wrappers).

## Functionality

The library calculates the potential energy of a CO₂ system using multiple routines:

- **p1b:** Computes a portion of the potential energy (using routines from `x1b`).
- **p2b:** Computes another portion of the potential energy (using routines from `x2b`).
- **sapt:** Calculates energy contributions based on SAPT (Symmetry-Adapted Perturbation Theory) components.

The core computations are implemented in C++ for performance.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.