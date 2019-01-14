# xblobs
Tools to detect and analyse coherent structures in turbulence (blobs), powered by xarray.

### ToDo:

- Blob detection (using `scipy.ndimage.label`)

- `blobs` accessor to store blobs methods, e.g.

  ```python
  ds.blobs['n'].lifetimes()
  ```

- Blob plotting methods (color-coded)

- Animated blob plots using `animatplot`
