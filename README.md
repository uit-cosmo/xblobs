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

# call blob methods you are interested in
print(blob1.lifetime())
#etc
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
                
blob1 = Blob(ds,1, n_var = 'n', t_dim = 't', rad_dim = 'x',pol_dim = 'z')
```
### generic xarray dataset
For a generic xarray dataset adjust the dimensions to your needs, for example:
```Python
from xblobs import Blob
from xblobs import find_blobs

ds = load_your_dataest()

ds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,\
                threshold = 1.3 ,region = 0.0, background = 'flat', \
                n_var = 'density', t_dim = 'time', rad_dim = 'radial', pol_dim = 'poloidal')
                
blob1 = Blob(ds,1, n_var = 'density', t_dim = 'time', rad_dim = 'radial', pol_dim = 'poloidal')
```
## Input parameters
### `find_blobs()`
- `da`: xbout Dataset  

- `threshold`: threshold value expressed in terms of the chosen scale_threshold

- `scale_threshold`: following methods implemented
  - `absolute_value`: threshold is scalar value
  - `profile`: threhsold is time- and poloidal-average profile
  - `std`: threshold is standard diviation over all three dimensions
  - `std_poloidal`: threshold is standard deviation over time and radial dimension
  
- `region`: radial potition from where blobs are detected

- `background`: background that is subtracted. Options:
  - `profile`: time- amd poloidal-averaged background
  - `flat`: no background subtracted

- `n_var`: xarray variable used for blob tracking
    
- `t_dim`: xarray dimension for time

- `rad_dim`: xarray dimension for radial dimension

- `pol_dim`: xarray dimension for poloidal dimension 

### `Blob()`
- `variable`: xbout Dataset containing blob_labels
- `id`: integer between 0 and number of detected blobs 
  - 0: refers to the background
  - 1-n: detected blobs  
- other parameters equivalent to 'find_blobs'


## Blob methods
the following blob parameters are implemented:
- `t_init`: time when blob is detected 
- `lifetime`: lifetime of blob
- `com`: center of mass over time
- `velocity`: absolute blob velocity over time
- `velocity_x`: radial blob velocity over time
- `velocity_y`: poloidal blob velocity over time
- `amplitude`: blob amplitude over time
- `max_amplitude`: max amplitude of blob
- `mass`: blob mass over time
- `average_mass`: average blob mass
- `size`: blob size over time

other blob parameters are straightforward to implement

## Parallelization 
Blob detection is parallelised across any number of dimensions by `dask-image`.

## Contact
If you have questions, suggestions or other comments you can contact me under gregor.decristoforo@uit.no
