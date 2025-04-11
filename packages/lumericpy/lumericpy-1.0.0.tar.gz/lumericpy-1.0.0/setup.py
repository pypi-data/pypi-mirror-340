from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'LumericPy: A Python package for Lumerical FDTD and MODE Solutions'
LONG_DESCRIPTION = 'LumericPy is a Python package designed to facilitate the use of Lumerical FDTD and MODE Solutions software. It provides a set of tools and functions to streamline the process of simulating and analyzing photonic devices using these powerful simulation tools.'

# Setting up
setup(
        name="lumericpy", 
        version=VERSION,
        author="Ameya Velankar",
        author_email="<velankar@uw.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy","matplotlib"], 

        keywords=['python', 'lumerical','importlib','sys','lumapi'],
        classifiers= []
)