#-*- coding: utf-8 -*-

import pyart
import sys
import numpy as np
#import matplotlib.pyplot as plt

"""
Creat a grid with one choosen elevation and use the HMC field with nearest bin  interpolation

input:
    infile: str
        input filename
    sweep: int
        desired sweep 
    outfile: str
        output filename
    resolution: tuple
        (z, y, x)
output:
    grid: file
        file in netcdf4 format
"""


class RadarFunctions:
    
    def __init__(self):
        self.Re = 8500000. # effective earth radius
        self.R = 6375000.  # earth radius
        
    def cart2radial(self, x, y, elev):
        s = np.sqrt(x**2 + y**2)
        r = self.ground2slant(s, elev)
        azim = np.arctan2(x, y)
        azim = np.rad2deg(azim)
        azim = np.where(x<0, azim+360, azim)
        return r, azim
    
    def slant2ground(self, r, elev):
        fi = np.deg2rad(elev)
        s = self.Re * np.arctan2(r*np.cos(elev), self.Re + r*np.sin(elev))
        return s
    
    def ground2slant(self, s, elev):
        fi = np.deg2rad(elev)
        r = self.Re / (np.cos(elev)/np.tan(s/self.Re) - np.sin(elev))
        return r
    
    def radial2latlon(self, r, azim, elev, radar_lat, radar_lon):
        latC = np.deg2rad(radar_lat)
        lonC = np.deg2rad(radar_lon)
        s = self.slant2ground(r, elev)
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
    
    def cartesian(self, radar, data, elev):
        '''
        #########data é uma matriz em polar já feito o extract_sweeps
        Na hora de montar a matriz cartesiana, considera o (0,0) em baixo do lado esquerdo
        '''
        res = 97
        m_cart = np.tile(-999., (res, res))
        raio = radar.range['data'][-1] #last radar range
        first_gate = radar.range['data'][0]
        bin_spacing = radar.range['data'][1] - radar.range['data'][0]
        nbins = radar.ngates
        #Encontra o centro de cada quadrado da grade cartesiana, centrada no radar
        x = np.arange(-raio + raio/res, raio, raio*2./res)
        y = np.arange(-raio + raio/res, raio, raio*2./res)
        #y = y[::-1] #para considerar o (0,0) em cima do lado esquerdo
        x,y = np.meshgrid(x,y)
        #Encontra o bin e ray correspondente a cada centro
        r, rays = self.cart2radial(x, y, elev)
        rays = rays - radar.azimuth['data'][0]
        rays = np.round(rays, 0).astype(int)
        rays = np.where(rays<0, rays + 360, rays)
        rays = np.where(rays==360, 0, rays)
        bins = np.round((r - first_gate)/bin_spacing, 0).astype(int)
        bins = np.where(bins>=nbins, -1, bins)
    
        m_cart = data[rays, bins]
        m_cart = np.where(bins<0, -999., m_cart)
        
        return m_cart
    
    def radar_limits(self, radar, elev):
        raio = radar.range['data'][-1]
        #Encontra os limites em lat/lon do alcance do radar
        radar_lat = radar.latitude['data'][0]
        radar_lon = radar.longitude['data'][0]
        latmin = self.radial2latlon(raio, 180, elev, radar_lat, radar_lon)[0]
        latmax = self.radial2latlon(raio,   0, elev, radar_lat, radar_lon)[0]
        lonmin = self.radial2latlon(raio, 270, elev, radar_lat, radar_lon)[1]
        lonmax = self.radial2latlon(raio,  90, elev, radar_lat, radar_lon)[1]
        return latmin, latmax, lonmin, lonmax

    def lat_lon_grid(self, grid, grid_shape, min_lat, max_lat, min_lon, max_lon ):
        d_lat = (max_lat - min_lat)/float(96)
        d_lon = (max_lon - min_lon)/float(96)
        lat = [min_lat]
        lon = [min_lon]
        for i in xrange(1,97):
            lat.append(lat[-1] + d_lat)
            lon.append(lon[-1] + d_lon)
        grid.axes['y_disp']['data'] = np.array(lat)
        grid.axes['x_disp']['data'] = np.array(lon)
        
try:
    infile  = sys.argv[1]
    sweep   = sys.argv[2]
    outfile = sys.argv[3]
    #try resolution = 
except:
    print "Use:  python ppi_HMC.py <input filename>  <sweep>  <output filename> (z, y, x) "
    sys.exit()

radar = pyart.io.read(infile, file_field_names=True)
#exclude unused fields
for field in radar.fields.keys():
    if field not in ['DBZH', 'DBZ', 'HMC']:
        del radar.fields[field]
        
try:
    radar = radar.extract_sweeps([int(sweep)])
    elev  = radar.fixed_angle['data'][int(sweep)]
except:
    print "Sweep not found"
    sys.exit()
    
#creating the grid    
grid_shape  = (1, 97, 97) #meters between gates: 500
grid_limits = ((0,0), (-240000, 240000), (-240000, 240000) )
grid = pyart.map.grid_from_radars((radar,), grid_shape, grid_limits)

try:
    del grid.fields['ROI']
except:
    pass

radf = RadarFunctions()
#interpolation
for field in radar.fields.keys():
    m_cart = radf.cartesian(radar, radar.fields[field]['data'].data , elev)
    m_cart = m_cart[np.newaxis]
    grid.fields[field]['data'] = np.ma.masked_less_equal(m_cart, 0)
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.imshow(np.ma.masked_less_equal(m_cart, 0),origin='lower')
    #ax.imshow(grid.fields[field]['data'][0],origin='lower')
    #plt.show()
    
min_lat, max_lat, min_lon, max_lon = radf.radar_limits(radar, elev)
radf.lat_lon_grid(grid, grid_shape, min_lat, max_lat, min_lon, max_lon )

pyart.io.write_grid(outfile, grid)


