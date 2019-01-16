from xarray import Dataset, DataArray, \
    register_dataset_accessor, register_dataarray_accessor

from .detect import find_blobs, DEFAULT_THRESHOLD


@register_dataset_accessor('blobs')
class BlobsDatasetAccessor:
    """
    Allows you to create a BlobSet instance from a xarray.Dataset by
    `ds.blobs()`
    """

    def __init__(self, ds):
        self._ds = ds

    #def __new__(cls, ds):
    #    return BlobSet(ds)

    def __call__(self, **kwargs):
        return BlobSet(self._ds, **kwargs)

    def __getitem__(self, var):
        da = self._ds[var]
        return BlobArray(da)


@register_dataarray_accessor('blobs')
class BlobsDataArrayAccessor:
    """
    Allows you to create a BlobArray instance from a xarray.DataArray by
    `da.blobs()`
    """

    def __init__(self, da, threshold=DEFAULT_THRESHOLD):
        self._da = da

        # TODO make this a property?
        self.threshold = threshold

    #def __new__(cls, da):
    #    return BlobArray(da)

    def __call__(self, *args, **kwargs):
        return BlobArray(self._da, *args, **kwargs)


class BlobSet:
    """
    All blobs in a dataset, across all variables.

    Created with `ds.blobs()`
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

    def __init__(self, da, threshold=DEFAULT_THRESHOLD):
        if not isinstance(da, DataArray):
            raise TypeError
        else:
            self.da = da

        self._threshold = threshold
        self._blob_list = self.find_blobs(threshold=self._threshold)

    def find_blobs(self, threshold=DEFAULT_THRESHOLD):
        self._blob_list = find_blobs(self.da, threshold=threshold)
        return self._blob_list

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value
        self.find_blobs(threshold=self._threshold)

    def __iter__(self):
        yield from self._blob_list

    def __len__(self):
        return len(self._blob_list)

    def __str__(self):
        text = "<xblobs.BlobArray>\n"
        text += f"Contains {len(self)} blobs above a threshold of {self.threshold}"
        text += f"found in {str(self.da)}"
        return text


class Blob:
    """
    A single blob.

    Accessed by `for blob in BlobArray`
    """

    def __init__(self, variable, id):
        self.variable = variable
        self.id = id

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

    def size(self):
        raise NotImplementedError
