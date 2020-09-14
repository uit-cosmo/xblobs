import numpy as np

class Blob():
    """
    A single blob.
    """

    def __init__(self, variable, id, n_var = 'n', t_dim = 'time', rad_dim = 'radial',pol_dim = 'binormal'):
        """
        variable : xbout Dataset containing blob_labels

        id : integer between 0 and number of detected blobs 
            0: refers to the background
            1-n: detected blobs  

        Choose other parameters equivalent to find_blobs() function.
        """
        self.variable = variable
        self.id = id
        self.n_var = n_var
        self.t_dim = t_dim
        self.rad_dim = rad_dim
        self.pol_dim = pol_dim

        self.label_field = self.variable['blob_labels'].where(self.variable['blob_labels'] == self.id, drop=True)
        self.n_field = self.variable[self.n_var].where(self.variable['blob_labels'] == self.id, drop=True)
        com_radial_field = self.n_field[self.rad_dim]*self.n_field
        com_binormal_field = self.n_field[self.pol_dim]*self.n_field
        total_mass_unnormalized = self.n_field.sum(dim=(self.pol_dim,self.rad_dim))

        self.com_radial = com_radial_field.sum(dim=(self.pol_dim,self.rad_dim)).values/total_mass_unnormalized.values
        self.com_binormal = com_binormal_field.sum(dim=(self.pol_dim,self.rad_dim)).values/total_mass_unnormalized.values

    def t_init(self):
        """
        Returns
        -------
        time when blob is detected : np.scalar
        """
        return self.label_field[self.t_dim].values[0]

    def lifetime(self):
        """
        Returns
        -------
        lifetime : np.scalar
        """
        return self.label_field[self.t_dim].values[-1] - self.label_field[self.t_dim].values[0]

    def com(self):
        """
        Returns
        -------
        centre of mass for each time step : 2d np.array

        """
        try:
            return np.vstack((np.concatenate(self.com_radial), np.concatenate(self.com_binormal)))
        except:
            return np.vstack(((self.com_radial), (self.com_binormal)))


    def velocity(self):
        """
        Returns
        -------
        absolute velocity for each time step : np.array

        """
        if(self.com_radial.size == 1):
            #print('blob only detected in one frame')
            return 0
        else:
            try:
                return ((np.diff(np.concatenate(self.com_radial))/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0]))**2 + \
                        (np.diff(np.concatenate(self.com_binormal))/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0]))**2)**0.5
            except:
                return ((np.diff(self.com_radial)/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0]))**2 + \
                        (np.diff(self.com_binormal)/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0]))**2)**0.5

    def velocity_x(self):
        """
        Returns
        -------
        radial velocity for each time step : np.array

        """
        if(self.com_radial.size == 1):
            #print('blob only detected in one frame')
            return 0
        else:
            try:
                return np.diff(np.concatenate(self.com_radial))/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0])
            except:
                return np.diff((self.com_radial))/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0])


    def velocity_y(self):
        """
        Returns
        -------
        poloidal velocity for each time step : np.array

        """        
        if(self.com_binormal.size == 1):
            #print('blob only detected in one frame')
            return 0
        else:
            try:
                return np.diff(np.concatenate(self.com_binormal))/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0])
            except:
                return np.diff(self.com_binormal)/(self.label_field[self.t_dim].values[1] - self.label_field[self.t_dim].values[0])

    def amplitude(self):
        """
        Returns
        -------
        array of amplitudes of blob for each timestep : np.array
        """
        try:
            return np.concatenate(self.n_field.max(dim=(self.rad_dim,self.pol_dim)).values)
        except:
            return self.n_field.max(dim=(self.rad_dim,self.pol_dim)).values


    def max_amplitude(self):
        """
        Returns
        -------
        maximum amplitude in blob's lifetime : np.scalar
        """
        return self.n_field.max(dim=(self.t_dim,self.rad_dim,self.pol_dim)).values

    def mass(self):
        """
        Returns
        -------
        array of mass of blob for each timestep : np.array
        """
        try:
            return np.concatenate(self.n_field.sum(dim=(self.rad_dim,self.pol_dim)).values*self.variable[self.rad_dim].values[1]*self.variable[self.pol_dim].values[1])
        except:
            return self.n_field.sum(dim=(self.rad_dim,self.pol_dim)).values*self.variable[self.rad_dim].values[1]*self.variable[self.pol_dim].values[1]

    def average_mass(self):
        """
        Returns
        -------
        time averaged mass of blob  : np.scalar
        """
        return self.n_field.sum(dim=(self.t_dim,self.rad_dim,self.pol_dim)).values*self.variable[self.rad_dim].values[1]*self.variable[self.pol_dim].values[1] \
            / self.n_field.sum(dim=(self.rad_dim,self.pol_dim)).values.size

    def size(self):
        """
        Returns
        -------
        array of size of blob for each timestep : np.array
        """
        try:
            return np.concatenate(self.label_field.sum(dim=(self.rad_dim,self.pol_dim)).values*self.variable[self.rad_dim].values[1]*self.variable[self.pol_dim].values[1] / self.id)
        except:
            return self.label_field.sum(dim=(self.rad_dim,self.pol_dim)).values*self.variable[self.rad_dim].values[1]*self.variable[self.pol_dim].values[1] / self.id

        
