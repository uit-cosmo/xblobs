# xblobs
Python tool to detect and analyse coherent structures in turbulence, powered by xarray. 

The algorithm has been developed originally to detect and track coherent structures (blobs) in plasma turbulence simulations but it can be applied on any 2D xarray Dataset with a cartesian grid and constant spacing `dx`,`dy` and `dt`. An example is shown below:


![Density evolution](example_gifs/turbulence_blobs.gif ) 


## Requirements
- Python >= 3.5
- xarray >= 0.11.2
- scipy >= 1.2.0
- dask-image >= 0.2.0
- numpy >= 1.14

## Installation

Dev install:
```
git clone https://github.com/gregordecristoforo/xblobs.git
cd xblobs
pip install -e .
```

## Usage
The algorithm is based on the threshold method, i.e. all structures exceeding a defined threshold are labeled as blobs. In order to track blobs over time they have to spatially overlap in two consecutive frames. 

Applying `find_blobs` function on xarray dataset returns the dataset with a new variable called `blob_labels`. The number of blobs is added as an attribute to `blob_labels` as `number_of_blobs`. The parameters of single blobs can then be calculated with the `Blob` class. 
### xstorm
The default implementation is done for a xstorm dataset.
```Python
from xblobs import Blob
from xblobs import find_blobs
from xstorm import open_stormdataset

ds = open_stormdataset(inputfilepath='./BOUT.inp')
ds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,
                threshold = 5e18 ,region = 0.0, background = 'flat')

blob1 = Blob(ds,1)

# call blob methods you are interested in
print(blob1.lifetime())
#etc
```
### xbout
For [BOUT++ simulations](https://github.com/boutproject/BOUT-dev) using [xbout](https://github.com/boutproject/xBOUT) one has to specify the dimensions in addition.
```Python
from xblobs import Blob
from xblobs import find_blobs
from xbout import open_boutdataset

ds = open_boutdataset()
ds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,
                threshold = 1.3 ,region = 0.0, background = 'flat', 
                n_var = 'n', t_dim = 't', rad_dim = 'x', pol_dim = 'z')
                
blob1 = Blob(ds,1, n_var = 'n', t_dim = 't', rad_dim = 'x',pol_dim = 'z')
```
### generic xarray dataset
For a generic xarray dataset adjust the dimensions to your needs, for example:
```Python
from xblobs import Blob
from xblobs import find_blobs

ds = load_your_dataset()

ds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,
                threshold = 1.3 ,region = 0.0, background = 'flat', 
                n_var = 'density', t_dim = 'time', rad_dim = 'radial', pol_dim = 'poloidal')
                
blob1 = Blob(ds,1, n_var = 'density', t_dim = 'time', rad_dim = 'radial', pol_dim = 'poloidal')
```
## Input parameters
### `find_blobs()`
- `da`: xbout Dataset  

- `threshold`: threshold value expressed in terms of the chosen scale_threshold

- `scale_threshold`: following methods implemented
  - `absolute_value`: threshold is scalar value
  - `profile`: threshold is time- and poloidal-average profile
  - `std`: threshold is standard deviation over all three dimensions
  - `std_poloidal`: threshold is standard deviation over poloidal dimension
  - `std_time`: threshold is standard deviation over time dimension

- `region`: blobs are detected in the region with radial indices greater than `region`

- `background`: background that is subtracted. Options:
  - `profile`: time- and poloidal-averaged background
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
- other parameters equivalent to `find_blobs`


## Blob methods
the following blob parameters are implemented:
- `t_init`: time when blob is detected 
- `lifetime`: lifetime of blob
- `com`: center of mass, over time
- `velocity`: absolute velocity of centre of mass of blob, over time
- `velocity_x`: radial velocity of centre of mass of blob, over time
- `velocity_y`: poloidal velocity of centre of mass of blob, over time
- `amplitude`: maximum of the signal within the blob above background, over time
- `max_amplitude`: maximum of the signal within the blob above background
- `mass`: integral of signal in area where background is exceeded, over time
- `average_mass`: average blob mass
- `size`: integral of area above background, over time

other blob parameters are straightforward to implement

## Parallelization 
Blob detection is parallelised across any number of dimensions by [`dask-image`](https://docs.dask.org/en/latest/).

## Contact
If you have questions, suggestions or other comments you can contact me under gregor.decristoforo@uit.no
