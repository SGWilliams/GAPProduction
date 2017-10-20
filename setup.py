from setuptools import setup

setup(
    name='GAPProduction',
    
    version='1.4',
    
    packages=['gapproduction',],
    
    author='Nathan M. Tarr',
    author_email='nmtarr@ncsu.edu',
    
    scripts=['bin/Update_Help_Files.py'],
    
    url='https://github.com/nmtarr/GAPAnalysis',
    
    license='LICENSE.txt',
    
    description='Functions for analyzing Gap Analysis Program habitat maps.',
    long_description=open('README.rst').read(),
    
    python_requires='==2.7',
        
    classifiers=['Development Status :: 3 - Alpha',
    		'Programming Language :: Python :: 2.7'],
    		
    keywords='USGS Gap Analysis Program',
     )