# -*- coding: utf-8 -*-

import numpy as np
from datetime import datetime

from Heymsfield import Heymsfield
heym = Heymsfield()

class ReadRadarStructure:

    def __init__(self, radar):
        '''
        radar: radar structure from pyart
        '''
        self.sweep_start = radar.sweep_start_ray_index['data']
        self.sweep_end = radar.sweep_end_ray_index['data']
        self.ranges = radar.range['data']
        self.bin_spacing = radar.range['meters_between_gates']
        self.first_gate = radar.range['meters_to_center_of_first_gate']
        self.azimuth = radar.azimuth['data']
        self.radar_alt = radar.altitude['data'][0]
        self.radar_lat = radar.latitude['data'][0]
        self.radar_lon = radar.longitude['data'][0]
        self.radar_range = self.ranges[-1]
        self.fixed_angle = radar.fixed_angle['data']
        self.nbins = self.ranges.shape[0]
        self.num_sweeps = len(self.fixed_angle)
        self.date = datetime.strptime(radar.time['units'], 'seconds since %Y-%m-%dT%H:%M:%SZ')

    def mount_volume(self, radar, var):
        '''
        Mounts a volume data
        Interpolate data to make 360 rays.

        radar: radar structure from pyart
        var: variable to be read
        '''
        data = np.ma.getdata(radar.fields[var]['data'])
        mask = np.ma.getmask(radar.fields[var]['data'])
        data = np.where(mask, -999., data)
        volume = np.tile(-999., (360, self.nbins, self.num_sweeps)).astype(float)
        for e in xrange(self.num_sweeps):
            ini_sweep = self.sweep_start[e]
            end_sweep = self.sweep_end[e]
            azim_sweep = self.azimuth[ini_sweep:end_sweep+1]
            for r in xrange(360):
                idx_ray = np.argmin(np.abs(azim_sweep-r))
                aux = data[idx_ray]
                volume[r,:len(aux),e] = aux
        return volume

    def cartesian(self, data, elev):
        '''
        Na hora de montar a matriz cartesiana, considera o (0,0) em baixo do lado esquerdo
        '''
        res = 400
        m_cart = np.tile(-999., (res, res))

        #Encontra o centro de cada quadrado da grade cartesiana, centrada no radar
        x = np.arange(-self.radar_range+self.radar_range/float(res), self.radar_range, self.radar_range*2./float(res))
        y = np.arange(-self.radar_range+self.radar_range/float(res), self.radar_range, self.radar_range*2./float(res))
        #y = y[::-1] #para considerar o (0,0) em cima do lado esquerdo
        x,y = np.meshgrid(x,y)

        #Encontra o bin e ray correspondente a cada centro
        r, rays = heym.cart2radial(x, y, elev)
        rays = np.round(rays,0).astype(int)
        rays = np.where(rays==360,0,rays)
        bins = np.round((r-self.first_gate)/self.bin_spacing,0).astype(int)
        bins = np.where(bins>=self.nbins, -1, bins)

        m_cart = data[rays, bins]
        m_cart = np.where(bins<0, -999., m_cart)
        return m_cart

    def radar_limits(self, elev):
        '''
        Encontra os limites em lat/lon do alcance do radar
        '''
        latmin = heym.radial2latlon(self.radar_range, 180, elev, self.radar_lat, self.radar_lon)[0]
        latmax = heym.radial2latlon(self.radar_range,   0, elev, self.radar_lat, self.radar_lon)[0]
        lonmin = heym.radial2latlon(self.radar_range, 270, elev, self.radar_lat, self.radar_lon)[1]
        lonmax = heym.radial2latlon(self.radar_range,  90, elev, self.radar_lat, self.radar_lon)[1]
        return latmin, latmax, lonmin, lonmax

