import os
from setuptools import setup

name = 'xblobs'

with open('README.md') as f:
    long_description = f.read()

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(here, name, '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup(name=name,
      version=version_ns['__version__'],
      description='Making animating in matplotlib easy',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/TomNicholas/xblobs/',
      author='Tom Nicholas',
      author_email='thomas.nicholas@york.ac.uk',
      license='GPL',
      packages=['xblobs'],
      python_requires='>=3.5',
      install_requires=['xarray>=0.11.2',
                        'matplotlib>=2.2',
                        'scipy>=1.2.0',
                        'animatplot'],
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
