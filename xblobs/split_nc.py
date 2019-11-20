import numpy as np
from xstorm import open_stormdataset
import xarray as xr
from boutdata import squashoutput

ds = open_stormdataset(inputfilepath='./BOUT.inp')
length = int(ds['time'].values.size)

number_of_processors = 2
chunk_size = (int(length))/number_of_processors

for i in range(number_of_processors):
    start = int(i*chunk_size)
    stop = int((i+1)*chunk_size)
    ds_chunk = ds.isel(time=slice( start,stop))

    data = xr.Dataset(
        {
            "t_array": (("time"),ds_chunk["t_array"].values),
            "dx": (("radial"),ds_chunk["dx"].values),
            "n": (("time","radial","binormal"),ds_chunk["n"].values),
            "dz": (("binormal"), np.ones(ds_chunk.binormal.values.size)*ds_chunk.metadata['dz']),
        },
        coords={"time": ds_chunk.time.values,"radial": ds_chunk.radial.values,"binormal": ds_chunk.binormal.values}
    )
    data.to_netcdf('chunk.'+str(i)+'.nc')
    ds_chunk.close()
    print('done with chunk '+ str(i))
ds.close()
