from xarray import Dataset, DataArray, \
    register_dataset_accessor, register_dataarray_accessor

from .detect import find_blobs


@register_dataset_accessor('blobs')
class BlobsDatasetAccessor:
    """
    Allows you to create a BlobSet instance from a xarray.Dataset by `ds.blobs`
    """

    def __init__(self, ds):
        self._ds = ds

    def __new__(cls, ds):
        return BlobSet(ds)

    def __getitem__(self, var):
        da = self._ds[var]
        return BlobArray(da)


@register_dataarray_accessor('blobs')
class BlobsDataArrayAccessor:
    """
    Allows you to create a BlobArray instance from a xarray.DataArray by
    `da.blobs`
    """

    def __init__(self, da):
        self._da = da

    def __new__(cls, da):
        return BlobArray(da)


class BlobSet:
    """
    All blobs in a dataset, across all variables.

    Created with `ds.blobs`
    """
    def __init__(self, ds):
        if not isinstance(ds, Dataset):
            raise TypeError

    def __getitem__(self, var):
        return BlobArray(var)



class BlobArray:
    """
    All blobs found, but for a single variable.

    Created with ds[var].blobs
    """

    def __init__(self, da):
        # TODO how can we pass a threshold argument to this?
        if not isinstance(da, DataArray):
            raise TypeError
        else:
            self.da = da

        self.find_blobs()

    def find_blobs(self):
        self._blob_list = find_blobs(self.da)

    def __iter__(self):
        yield from self._blob_list



class Blob:
    """
    A single blob.

    Accessed by `for blob in BlobArray`
    """

    def lifetime(self):
        """


        Returns
        -------
        lifetime : np.scalar
        """
        raise NotImplementedError

    def com(self):
        raise NotImplementedError

    def velocity(self):
        raise NotImplementedError

    def trajectory(self):
        """

        Returns
        -------
        trajectory : xarray.DataArray
            DataArray of positions over time?
        """
        raise NotImplementedError

    def amplitude(self):
        raise NotImplementedError

    def mass(self):
        raise NotImplementedError
