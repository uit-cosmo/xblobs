import numpy as np
import matplotlib.pyplot as plt 
import figure_defs
import xarray as xr 
from xstorm import open_stormdataset


axes_size = figure_defs.set_rcparams_aip(plt.rcParams, num_cols=1, ls='thin')

num_nc_files = 32

ds = xr.open_dataset('blobs.0.nc')  
for i in range(1,num_nc_files):
    ds1 = xr.open_dataset('blobs.'+str(i)+'.nc') 
    ds = xr.concat([ds, ds1],'label')
    ds1.close() 

ds = xr.concat([ds, ds1],'label')
long_ds = ds.where(ds['lifetime'] > 30)
fluc_ds = ds.where(ds['x_init'] > 0.048)

fluc_ds = ds.where(ds['x_init'] > 0.048)
sep_ds = ds.where(ds['x_init'] < 0.048)

print(ds)
print(np.count_nonzero(~np.isnan(long_ds['av_mass'].values)))

#data =  [ds]
data = [long_ds]
#data = [sep_ds,fluc_ds]
#
fig_v = plt.figure()
axv = fig_v.add_axes(axes_size)
fig_vx = plt.figure()
axvx = fig_vx.add_axes(axes_size)
fig_vy = plt.figure()
axvy = fig_vy.add_axes(axes_size)
fig_l = plt.figure()
axl = fig_l.add_axes(axes_size)
fig_mass = plt.figure()
ax_mass = fig_mass.add_axes(axes_size)
fig_size = plt.figure()
ax_size = fig_size.add_axes(axes_size)
fig_xinit = plt.figure()
ax_xinit = fig_xinit.add_axes(axes_size)
fig_v_mass = plt.figure()
ax_v_mass = fig_v_mass.add_axes(axes_size)
fig_x_mass = plt.figure()
ax_x_mass = fig_x_mass.add_axes(axes_size)

def moving_average(a, n=300) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

for i in data:
    axv.hist(i['v'],bins=50,range=(0,8000), log=True)
    axv.set_xlabel(r'$v$')

    axvx.hist(i['v_x'],bins=50,range=(-2000,8000), log=True)
    axvx.set_xlabel(r'$v_x$')

    axvy.hist(i['v_y'],bins=50,range=(-3000,3000), log=True)
    axvy.set_xlabel(r'$v_y$')

    axl.hist(i['lifetime'],range=(0,160),bins=50)
    axl.set_xlabel(r'$lifetime$')

    ax_mass.hist(i['av_mass'],bins=50,range=(0,1.5e21))
    ax_mass.set_xlabel(r'$average\, mass$')

    ax_size.hist(i['av_size'],bins=50,range=(0,300))
    ax_size.set_xlabel(r'$average\, size$')

    ax_xinit.hist(i['x_init'],bins=50,range=(0.04,0.145))
    ax_xinit.set_xlabel(r'$x\, init$')

    
    ax_v_mass.scatter(i["av_mass"],i['v_x'])
    #a = np.array([i["av_mass"],i['v']])
    '''
    a=a.T
    print(a[:, 0])
    b = a[a[:, 0].argsort()
    print(b[1])
    ax_v_mass.scatter(b[:,0],b[:,1])
    size = b[:,1].size - moving_average(b[:,1]).size
    print(size)
    axes = b[:,0]
    axes = axes[int(size):]
    print(axes.size)
    axes = axes[:int(b[:,1].size-size)]
    ax_v_mass.plot(axes,moving_average(b[:,1]),color='r')
    ax_v_mass.set_ylabel(r'$v$')
    ax_v_mass.set_xlabel(r'$average\, mass$')

    #p = np.polyfit(i["av_mass"], i['v'], 3)
    #p = np.poly1d(np.polyfit(i["av_mass"], i['v'], 3))
    #ax_v_mass.plot(i["av_mass"],p(i["av_mass"]))
    '''
    ax_x_mass.scatter(i["av_mass"],i['x_init'])
    ax_x_mass.set_ylabel(r'$x \,init$')
    ax_x_mass.set_xlabel(r'$average\, mass$')


plt.show()

