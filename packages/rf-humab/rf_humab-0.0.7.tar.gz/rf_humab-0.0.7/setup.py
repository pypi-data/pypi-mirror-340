from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Humanization tool for IgG heavy chain sequences'
LONG_DESCRIPTION = 'Humanization tool for IgG heavy chain sequences based on the paper at https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8760955/.'

# Setting up
setup(
        name="rf_humab", 
        version=VERSION,
        author="Lydia Stone",
        author_email="<lstone@g.hmc.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        ],
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        include_package_data=True,
)