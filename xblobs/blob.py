
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
