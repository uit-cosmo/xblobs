from mpi4py import MPI
import numpy as np
from xblobs import find_blobs
from xblobs import Blob
from xstorm import open_stormdataset
import xarray as xr

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

ds = xr.open_dataset('chunk.' + str(rank)+'.nc')

ds = find_blobs(da = ds, threshold =2 ,region = 0.3)
print("dataset contains "+str(np.max(ds['blob_labels'].values)) + " blobs")

lifetime = np.zeros(np.max(ds['blob_labels'].values)-1)
t_init = np.zeros(np.max(ds['blob_labels'].values)-1)
max_amp = np.zeros(np.max(ds['blob_labels'].values)-1)
av_mass = np.zeros(np.max(ds['blob_labels'].values)-1)
av_size = np.zeros(np.max(ds['blob_labels'].values)-1)
v = np.zeros(np.max(ds['blob_labels'].values)-1)
v_x = np.zeros(np.max(ds['blob_labels'].values)-1)
v_y = np.zeros(np.max(ds['blob_labels'].values)-1)
x_init = np.zeros(np.max(ds['blob_labels'].values)-1)
y_init = np.zeros(np.max(ds['blob_labels'].values)-1)


time_step = (ds['time'].values[1] - ds['time'].values[0])
stop = np.arange(1,np.max(ds['blob_labels'].values))

for i in stop:
    tmp = Blob(ds,i)
    i-=1
    lifetime[i] = tmp.lifetime()/time_step
    t_init[i] = tmp.t_init()
    max_amp[i] = tmp.max_amplitude()
    av_mass[i] = tmp.average_mass()
    av_size[i] = np.average(tmp.size())

    v[i] = np.average(tmp.velocity())
    v_x[i] = np.average(tmp.velocity_x())
    v_y[i] = np.average(tmp.velocity_y())

    com = tmp.com()
    x_init[i] = com[0,0]
    y_init[i] = com[1,0]
    print("done with blob " + str(i))


data = xr.Dataset(
    {
        "lifetime": (("label"),lifetime),
        "t_init": (("label"),t_init),
        "max_amp": (("label"),max_amp),
        "av_mass": (("label"),av_mass),
        "av_size": (("label"),av_size),
        "v": (("label"),v),
        "v_x": (("label"),v_x),
        "v_y": (("label"),v_y),
        "x_init": (("label"),x_init),
        "y_init": (("label"),y_init),
     }
)


data.to_netcdf('blobs.'+ str(rank)+'.nc') 

