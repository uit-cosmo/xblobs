import numpy as np

class Blob:
    """
    A single blob.

    Accessed by `for blob in BlobArray`
    """

    def __init__(self, variable, id):
        self.variable = variable
        self.id = id

        self.label_field = self.variable['blob_labels'].where(self.variable['blob_labels'] == self.id, drop=True)
        self.n_field = self.variable['n'].where(self.variable['blob_labels'] == self.id, drop=True)
        com_radial_field = self.n_field['radial']*self.n_field
        com_binormal_field = self.n_field['binormal']*self.n_field
        total_mass_unnormalized = self.n_field.sum(dim=('binormal','radial'))

        self.com_radial = com_radial_field.sum(dim=('binormal','radial')).values/total_mass_unnormalized.values
        self.com_binormal = com_binormal_field.sum(dim=('binormal','radial')).values/total_mass_unnormalized.values

    def t_init(self):
        """
        Returns
        -------
        time when blob is detected : np.scalar
        """
        return self.label_field['time'].values[0]

    def lifetime(self):
        """
        Returns
        -------
        lifetime : np.scalar
        """
        lifetime = self.label_field['time'].values[-1] - self.label_field['time'].values[0]
        return lifetime

    def com(self):
        """
        Returns
        -------
        centre of mass for each time step : np.array

        """
        return np.vstack((self.com_radial, self.com_binormal))

    def velocity(self):
        if(self.com_radial.size == 1):
            #print('blob only detected in one frame')
            return 0
        else:
            return ((np.diff(self.com_radial)/(self.label_field['time'].values[1] - self.label_field['time'].values[0]))**2 + \
                    (np.diff(self.com_binormal)/(self.label_field['time'].values[1] - self.label_field['time'].values[0]))**2)**0.5

    def velocity_x(self):
        if(self.com_radial.size == 1):
            #print('blob only detected in one frame')
            return 0
        else:
            return np.diff(self.com_radial)/(self.label_field['time'].values[1] - self.label_field['time'].values[0])

    def velocity_y(self):
        if(self.com_binormal.size == 1):
            #print('blob only detected in one frame')
            return 0
        else:
            return np.diff(self.com_binormal)/(self.label_field['time'].values[1] - self.label_field['time'].values[0])


    def amplitude(self):
        """
        Returns
        -------
        array of amplitudes of blob for each timestep : np.array
        """
        return self.n_field.max(dim=('radial','binormal')).values


    def max_amplitude(self):
        """
        Returns
        -------
        maximum amplitude in blob's lifetime : np.scalar
        """
        return self.n_field.max(dim=('time','radial','binormal')).values

    def mass(self):
        """
        Returns
        -------
        array of mass of blob for each timestep : np.array
        """
        return self.n_field.sum(dim=('radial','binormal')).values*self.variable['radial'].values[1]*self.variable['binormal'].values[1]

    def average_mass(self):
        """
        Returns
        -------
        time averaged mass of blob  : np.scalar
        """
        return self.n_field.sum(dim=('time','radial','binormal')).values*self.variable['radial'].values[1]*self.variable['binormal'].values[1] / self.n_field.sum(dim=('radial','binormal')).values.size

    def size(self):
        """
        Returns
        -------
        array of size of blob for each timestep : np.array
        """
        return self.label_field.sum(dim=('radial','binormal')).values*self.variable['radial'].values[1]*self.variable['binormal'].values[1] / self.id
        
