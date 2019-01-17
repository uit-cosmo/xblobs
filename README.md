# xblobs
Tools to detect and analyse coherent structures in turbulence (blobs), powered by xarray.
Blob detection is parallelised across any number of dimensions by `dask-image`.

### ToDo:

- Blob detection (using `scipy.ndimage.label`)

- `blobs` accessor to store blobs methods, e.g.

  ```python
  ds.blobs['n'].lifetimes()
  ```

- Blob plotting methods (color-coded)

- Animated blob plots using `animatplot`
