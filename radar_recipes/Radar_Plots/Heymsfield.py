# -*- coding: utf-8 -*-

import numpy as np

class Heymsfield:
    '''
        An Interactive System for Compositing Digital Radar and Satellite Data. (Heymsfield, G. M. et al)

        radial   : (r, teta, phi)
        polar    : (s, teta)
        cartesian: (x, y)
        lat-lon  : (sigma, alpha)

        r   : slant range
        s   : ground range
        phi : elevation angle
        azim: azimuth (teta)
        lat : latitude (sigma)
        lon : longitude (alpha)
        latC: latitude do radar
        lonC: longitude do radar
    '''

    def __init__(self):
        self.Re = 8500000. # effective earth radius
        self.R = 6375000.  # earth radius

    def slant2ground(self, r, fi):
        fi = np.deg2rad(fi)
        s = self.Re * np.arctan2(r*np.cos(fi), self.Re + r*np.sin(fi))
        return s

    def ground2slant(self, s, fi):
        fi = np.deg2rad(fi)
        r = self.Re / (np.cos(fi)/np.tan(s/self.Re) - np.sin(fi))
        return r

    def radial2cart(self, r, azim, fi):
        s = self.slant2ground(r, fi)
        fi = np.deg2rad(fi)
        azim = np.deg2rad(azim)
        x = s*np.sin(azim)
        y = s*np.cos(azim)
        return x, y

    def cart2radial(self, x, y, fi):
        s = np.sqrt(x**2 + y**2)
        r = self.ground2slant(s, fi)
        azim = np.arctan2(x, y)
        azim = np.rad2deg(azim)
        azim = np.where(x<0, azim+360, azim)
        return r, azim

    def radial2latlon(self, r, azim, fi, radar_lat, radar_lon):
        latC = np.deg2rad(radar_lat)
        lonC = np.deg2rad(radar_lon)
        #para quando for duas matrizes, mais tem que testar ainda
        #try:
            #azim = azim.reshape(azim.shape[0], 1)
        #except:
            #pass
        s = self.slant2ground(r, fi)
        lamb = s / self.R
        azim = np.deg2rad(azim)
        
        lat = np.arcsin(np.cos(lamb)*np.sin(latC) + np.sin(lamb)*np.cos(latC)*np.cos(azim))
        
        aux = (np.cos(lamb) - np.sin(latC)*np.sin(lat)) / (np.cos(latC)*np.cos(lat))
        aux = np.where(aux>1., 1., aux)
        aux = np.where(aux<-1., -1., aux)
        aux = np.arccos(aux)
        lon = np.where(azim<=np.pi, lonC + aux, lonC - aux)
        lat = np.rad2deg(lat)
        lon = np.rad2deg(lon)
        return lat, lon

    def latlon2radial(self, lat, lon, fi, radar_lat, radar_lon):
        latC = np.deg2rad(radar_lat)
        lonC = np.deg2rad(radar_lon)
        lat = np.deg2rad(lat)
        lon = np.deg2rad(lon)

        lamb = np.arccos(np.sin(lat)*np.sin(latC) + np.cos(lat)*np.cos(latC)*np.cos(lon-lonC))
        s = self.R * lamb
        r = self.ground2slant(s, fi)

        aux = (np.sin(lat) - np.cos(lamb)*np.sin(latC))/ float(np.sin(lamb)*np.cos(latC))
        aux = np.where(aux>1., 1., aux)
        aux = np.where(aux<-1., -1., aux)
        azim = np.arccos(aux)
        azim = np.rad2deg(azim)
        azim = np.where(lon<lonC, 360-azim, azim)
        return r, azim

    def cart2latlon(self, x, y, fi, radar_lat, radar_lon):
        r, azim  = self.cart2radial(x, y, fi)
        lat, lon = self.radial2latlon(r, azim, fi, radar_lat, radar_lon)
        return lat, lon

    def latlon2cart(self, lat, lon, fi, radar_lat, radar_lon):
        r, azim = self.latlon2radial(lat, lon, fi, radar_lat, radar_lon)
        x, y    = self.radial2cart(r, azim, fi)
        return x, y

