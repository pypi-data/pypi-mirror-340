from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'LumericPy: A Python package for Lumerical FDTD and MODE Solutions'
LONG_DESCRIPTION = 'LumericPy is a Python package designed to facilitate the use of Lumerical FDTD and MODE Solutions software. It provides a set of tools and functions to streamline the process of simulating and analyzing photonic devices using these powerful simulation tools.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="lumericpy", 
        version=VERSION,
        author="Ameya Velankar",
        author_email="<velankar@uw.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy","matplotlib"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'lumerical'],
        classifiers= []
)