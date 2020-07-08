import os
from setuptools import setup

name = 'xblobs'

with open('README.md') as f:
    long_description = f.read()

here = os.path.abspath(os.path.dirname(__file__))

setup(name=name,
      description='Tracking coherent structures in turbulence',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/gregordecristoforo/xblobs/tree/master/xblobs',
      author='Gregor Decristoforo',
      author_email='gregor.decristoforo@uit.no',
      license='GPL',
      version='1.0',
      packages=['xblobs'],
      python_requires='>=3.5',
      install_requires=['xarray>=0.11.2',
                        'matplotlib>=2.2',
                        'scipy>=1.2.0',
                        'dask-image>=0.2.0',
                        'animatplot'],
      tests_require=['pytest',
                     'numpy'],
      classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Visualization',
      ],
      zip_safe=False)
