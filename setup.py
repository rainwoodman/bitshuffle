from setuptools import setup, Extension
from setuptools.command.install import install as install_
from Cython.Distutils import build_ext
#from Cython.Build import cythonize
import numpy as np
import os
import sys
from os import path
import shutil
import glob

VERSION_MAJOR = 0
VERSION_MINOR = 2
VERSION_POINT = 1

# Only unset in the 'release' branch and in tags.
VERSION_DEV = 1

VERSION = "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_POINT)
if VERSION_DEV:
    VERSION = VERSION + ".dev%d" % VERSION_DEV


COMPILE_FLAGS = ['-Ofast', '-march=native', '-std=c99', '-fopenmp']
# Cython breaks strict aliasing rules.
COMPILE_FLAGS += ["-fno-strict-aliasing"]
#COMPILE_FLAGS = ['-Ofast', '-march=core2', '-std=c99', '-fopenmp']

MACROS = [
          ('BSHUF_VERSION_MAJOR', VERSION_MAJOR),
          ('BSHUF_VERSION_MINOR', VERSION_MINOR),
          ('BSHUF_VERSION_POINT', VERSION_POINT),
          ]


ext_bshuf = Extension("bitshuffle.ext",
                   ["bitshuffle/ext.pyx", "src/bitshuffle.c", "lz4/lz4.c"],
                   include_dirs=[np.get_include(), "src/",
                                                "lz4/"],
                   depends=["src/bitshuffle.h", "src/iochain.h", "lz4/lz4.h"],
                   libraries = ['gomp'],
                   extra_compile_args=COMPILE_FLAGS,
                   define_macros=MACROS,
                   )

EXTENSIONS = [ext_bshuf]

setup(
    name = 'bitshuffle',
    version = VERSION,

    packages = ['bitshuffle'],
    scripts=[],
    ext_modules = EXTENSIONS,
    cmdclass = {'build_ext': build_ext},
    install_requires = ['numpy', 'Cython'],
    package_data={'': ['bitshuffle/tests/data/*']},

    # metadata for upload to PyPI
    author = "Kiyoshi Wesley Masui",
    author_email = "kiyo@physics.ubc.ca",
    description = "Bitshuffle filter for improving typed data compression.",
    license = "MIT",
    url = "http://github.com/kiyo-masui/bitshuffle"
)

