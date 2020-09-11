# xblobs
Python tool to detect and analyse coherent structures in turbulence, powered by xarray. 

The algorithm has been developed originally to detect and track coherent structures (blobs) in plasma turbulence simulations but it can be applied on any 2D xarray Dataset. An example is shown below:


![Density evolution](example_gifs/turbulence_blobs.gif ) 


## Requirements
- Python >= 3.5
- xarray >= 0.11.2
- scipy >= 1.2.0
- dask-image >= 0.2.0
- numpy >= 1.14

## Instalation (pip and conda installation not enabled yet)
`pip install xblobs`
or with using conda
`conda install xblobs -c conda-forge`

Dev install:
```
git clone git@github.com:gregordecristoforo/xblobs.git
pip install -e .
```

## Usage
Applying `find_blobs` function on xarray dataset returns the dataset with a new variable called `blob_lables`. The parameters of single blobs can then be calculated with the `Blob` class. 
### xstorm
The default implementation is done for a xstorm dataset.
```Python
from xblobs import Blob
from xblobs import find_blobs
from xstorm import open_stormdataset

ds = open_stormdataset(inputfilepath='./BOUT.inp')
ds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,\
                threshold = 5e18 ,region = 0.0, background = 'flat')

blob1 = Blob(ds,1)
```
### xbout
For xbout one has to specify the dimenons in addition.
```Python
from xblobs import Blob
from xblobs import find_blobs
from xbout import open_boutdataset

ds = open_boutdataset()
ds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,\
                threshold = 1.3 ,region = 0.0, background = 'flat', \
                n_var = 'n', t_dim = 't', rad_dim = 'x', pol_dim = 'z')
                
tmp = Blob(ds,1, n_var = 'n', t_dim = 't', rad_dim = 'x',pol_dim = 'z')
```
### generic xarray dataset
For a generic xarray dataset adjust the dimensions to your needs, for example:
```Python
from xblobs import Blob
from xblobs import find_blobs

ds = load_your_dataest()

ds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,\
                threshold = 1.3 ,region = 0.0, background = 'flat', \
                n_var = 'density'= 'time', rad_dim = 'radial', pol_dim = 'poloidal')
                
tmp = Blob(ds,1, n_var = 'density', t_dim = 'time', rad_dim = 'radial', pol_dim = 'poloidal')
```

## Parallelization 
Blob detection is parallelised across any number of dimensions by `dask-image`.
