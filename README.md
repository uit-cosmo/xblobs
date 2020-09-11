# xblobs
Tools to detect and analyse coherent structures in turbulence (blobs), powered by xarray.

## requirements
- Python >= 3.5
- xarray >= 0.11.2
- scipy >= 1.2.0
- dask-image >= 0.2.0
- numpy >= 1.14

Blob detection is parallelised across any number of dimensions by `dask-image`.

![Density evolution](example_gifs/turbulence_blobs.gif ) 
