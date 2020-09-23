import scipy.ndimage
import dask_image.ndmeasure
import numpy as np
from xarray import apply_ufunc

from .blob import Blob


DEFAULT_THRESHOLD = 1
DEFAULT_REGION = 0

def find_blobs(da, threshold=DEFAULT_THRESHOLD, scale_threshold = 'std', region = DEFAULT_REGION, \
                background = 'profile', n_var = 'n', t_dim = 'time', rad_dim = 'radial',pol_dim = 'binormal'):
    """
    Parameters
    ----------
    da : xbout Dataset

    threshold : double, optional
        threshold value expressed in terms of the chosen scale_threshold

    scale_threshold : string, optional
        options:
            absolute_value: threshold is scalar value
            profile: threhsold is time- and poloidal-average profile
            std: threshold is standard diviation over all three dimensions
            std_poloidal: threshold is standard deviation over poloidal dimension
            std_time: threshold is standard deviation over time dimension

    region : double, optional
        radial potition from where blobs are detected

    background : string, optional
        background that is subtracted 
        options:
            profile: time- amd poloidal-averaged background
            flat: no background subtracted

    n_var : xarray variable, optional
        xarray variable used for blob tracking
    
    t_dim : xarray dimension, optional
        xarray dimension for time

    rad_dim : xarray dimension, optional
        xarray dimension for radial dimension

    pol_dim : xarray dimenison, optional
        xarray dimension for poloidal dimension 

    Returns
    -------
    blob_labels : xarray.DataArray containing labels of features.

    """    
    # remove core region if wanted
    mask = da[rad_dim] > region*da[rad_dim][-1]

    mask1 = da[pol_dim] > 0.0*da[pol_dim][-1]
    mask2 = da[pol_dim] < 1.0*da[pol_dim][-1]

    n_selected_region  = da[n_var].where(mask, 0)
    n_selected_region  = n_selected_region.where(mask1, 0)
    n_selected_region  = n_selected_region.where(mask2, 0)

    da['n_selected_region'] = n_selected_region

    # subtract profile of n
    if background == 'profile':
        da['n_profile'] = da['n_selected_region'].mean(dim=(t_dim, pol_dim))
        n_fluc =  da['n_selected_region'] - da['n_profile']
    elif background == 'flat':
        n_fluc =  da['n_selected_region']
    else:
        raise SystemExit('Error: background must be either profile or flat')

    # apply condition for blobs
    if scale_threshold == 'std_poloidal':
        scale = n_fluc.std(dim=(pol_dim))
    if scale_threshold == 'std_time':
        scale = n_fluc.std(dim=(t_dim))
    elif scale_threshold == 'std':
        scale = n_fluc.std()
    elif scale_threshold == 'absolute_value':
        scale = 1
    elif scale_threshold == 'profile':
        scale = da['n_selected_region'].mean(dim=(t_dim, pol_dim))
    else:
        raise SystemExit('Error: chosen scale_threshold not implemented')

    mask = n_fluc>threshold*scale
    mask2 = n_fluc<=threshold*scale
    fluctuations = n_fluc.where(mask, 0)
    fluctuations  = fluctuations.where(mask2, 1)
    da['fluctuations'] = fluctuations

    #detect coherent blob structures
    blob_labels = _detect_features(da['fluctuations'], parallel=False)

    da['blob_labels'] = blob_labels
    da["blob_labels"].attrs["number_of_blobs"] = np.max(da['blob_labels'].values)
    return da
    

def _detect_features(da, parallel=False):
    """

    Parameters
    ----------
    parallel : bool, optional
        Only really for debugging by checking dask_image.ndmeasure.label
        against scipy.ndimage.label.

    Returns
    -------
    labels : xarray.DataArray containing labels of features.
    """
    if parallel:
        detector_gufunc = _dask_image_detector_gufunc
        dask = 'allowed'
    else:
        detector_gufunc = _scipy_detector_gufunc
        dask = 'allowed'

    labels = apply_ufunc(detector_gufunc, da, dask=dask, keep_attrs=True)

    return labels


def _dask_image_detector_gufunc(image):
    labels, num_features = dask_image.ndmeasure.label(image)
    return labels


def _scipy_detector_gufunc(image):
    labels, num_features = scipy.ndimage.label(image)
    return labels
