import scipy.ndimage
import dask_image.ndmeasure

from xarray import apply_ufunc


from .blob import Blob


DEFAULT_THRESHOLD = 0.2


def find_blobs(da, threshold=DEFAULT_THRESHOLD):

    # Set all values below threshold to zero

    blob_labels_name = da.name + "_blobs"
    da[blob_labels_name] = _detect_features(da, parallel=True)

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
        detector_gufunc = _dask_image_detector_gufunc
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
