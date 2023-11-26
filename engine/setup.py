from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy

extensions = [
    Extension(
        name='bosons',
        sources=['bosons.pyx'],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        name='fermions',
        sources=['fermions.pyx'],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    ext_modules=cythonize(extensions),
    description='Bose Hubbard and Fermi Hubbard Hamiltonian builders.',
    install_requires=[
        'numpy',
        'itertools',
    ],
    # Specify the directory where the compiled files should be placed
    script_args=["build_ext", "--inplace", "--build-lib=build"]
)

#python setup.py build_ext --inplace