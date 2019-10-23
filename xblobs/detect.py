import numpy
import scipy.ndimage
import dask_image.ndmeasure

from xarray import apply_ufunc


from .blob import Blob


DEFAULT_THRESHOLD = 1
DEFAULT_REGION = 0

def find_blobs(da, threshold=DEFAULT_THRESHOLD, region = DEFAULT_REGION):
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
    mask = da.radial > region*da.radial[-1]
    n_selected_region  = da['n'].where(mask, 0)
    da['n_selected_region'] = n_selected_region

    # subtract profile of n
    da['n_profile'] = da['n_selected_region'].mean(dim=('time', 'binormal'))
    n_fluc =  da['n_selected_region'] - da['n_profile']

    # apply condition for blobs
    mask = n_fluc>threshold*n_fluc.std(dim='binormal')
    mask2 = n_fluc<=threshold*n_fluc.std(dim='binormal')
    #print(n_fluc.std(dim='radial').shape)
    fluctuations = n_fluc.where(mask, 0)
    fluctuations  = fluctuations.where(mask2, 1)
    da['fluctuations'] = fluctuations

    #detect coherent blob structures
    da['blob_labels'] = _detect_features(da['fluctuations'], parallel=True)

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
