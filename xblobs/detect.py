import numpy
import scipy.ndimage
import dask_image.ndmeasure

from xarray import apply_ufunc

from .blob import Blob


DEFAULT_THRESHOLD = 1
DEFAULT_REGION = 0

def find_blobs(da, threshold=DEFAULT_THRESHOLD, scale_treshold = 'std', region = DEFAULT_REGION, background = 'profile', norm_density = False):
    """
    Parameters
    ----------
    da : xbout Dataset
    threshold : double, optional
        threshold value in density fluctitions
    region: double, optional
        radial potition from where blobs are detected

    Returns
    -------
    labels : xarray.DataArray containing labels of features.

    """    
    # remove core region if wanted

        # normalize density
    if norm_density:
        da['n2'] = da['n']**2
        n_mean = da['n'].mean(dim=('time')).values
        n_mean2 = da['n2'].mean(dim=('time')).values
        n_rms = numpy.sqrt(n_mean2)
        da['n_norm'] = (da['n'] - n_mean)/n_rms

    mask = da.radial > region*da.radial[-1]

    #remove borders because of periodicity 
    mask1 = da.binormal > 0.0*da.binormal[-1] 
    mask2 = da.binormal < 1.0*da.binormal[-1]

    if norm_density:
        n_selected_region  = da['n_norm'].where(mask, 0)
        n_selected_region  = n_selected_region.where(mask1, 0)
        n_selected_region  = n_selected_region.where(mask2, 0)
    else:
        n_selected_region  = da['n'].where(mask, 0)
        n_selected_region  = n_selected_region.where(mask1, 0)
        n_selected_region  = n_selected_region.where(mask2, 0)


    da['n_selected_region'] = n_selected_region

    # subtract profile of n
    if background == 'profile':
        da['n_profile'] = da['n_selected_region'].mean(dim=('time', 'binormal'))
        n_fluc =  da['n_selected_region'] - da['n_profile']
    elif background == 'flat':
        n_fluc =  da['n_selected_region']
    else:
        print('background must be either profile or flat')

    # apply condition for blobs
    if scale_treshold == 'std_binormial':
        scale = n_fluc.std(dim='binormal')
    elif scale_treshold == 'std':
        scale = n_fluc.std()
    elif scale_treshold == 'absolute_value':
        scale = 1
    elif scale_treshold == 'profile':
        scale = da['n_selected_region'].mean(dim=('time', 'binormal'))

    mask = n_fluc>threshold*scale
    mask2 = n_fluc<=threshold*scale
    #print(n_fluc.std(dim='radial').shape)
    fluctuations = n_fluc.where(mask, 0)
    fluctuations  = fluctuations.where(mask2, 1)
    da['fluctuations'] = fluctuations

    #detect coherent blob structures
    blob_labels = _detect_features(da['fluctuations'], parallel=True)

    da['blob_labels'] = blob_labels
    # TODO instead return list of Blob objects?
    return da
    

def _detect_features(da, dim=None, parallel=True):
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
    if dim:
        raise NotImplementedError("Currently always detects blobs across all "
                                  "dimensions")

    if parallel:
        #detector_gufunc = _dask_image_detector_gufunc
        detector_gufunc = _scipy_detector_gufunc
        dask = 'allowed'
    else:
        detector_gufunc = _scipy_detector_gufunc
        dask = 'forbidden'

    labels = apply_ufunc(detector_gufunc, da, dask=dask, keep_attrs=True)

    return labels


def _dask_image_detector_gufunc(image):
    labels, num_features = dask_image.ndmeasure.label(image)
    return labels


def _scipy_detector_gufunc(image):
    labels, num_features = scipy.ndimage.label(image)
    return labels
