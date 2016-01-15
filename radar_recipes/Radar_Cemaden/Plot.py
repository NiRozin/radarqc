# -*- coding: utf-8 -*-

import os
#import Image
import numpy as np
#from glob import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
#from matplotlib.patches import Polygon
#from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap, cm

from Heymsfield import Heymsfield
heym = Heymsfield()
from ColorMap import ColorMap
cm = ColorMap()
#from RadarFunctions import RadarFunctions


#radf = RadarFunctions()

class Plot:

    def __init__(self):
        self.dirname = 'images/'
        try:
            os.makedirs(self.dirname)
        except:
            pass

    #def image_mask(self, figname, mask):
        #file_mask = '../%s.png' % mask
        #file_contour = '%s.png' % figname
        #img_contour = Image.open(file_contour).convert("RGBA")
        #img_mask = Image.open(file_mask).convert("RGBA")
        #img = Image.composite(img_mask, img_contour, img_mask)
        #img.save(file_contour)

    #def image_trim(self, figname):
        #file_contour = '%s.png' % figname
        #os.system('convert -trim %s %s' % (file_contour, file_contour))
        #os.renames(file_contour, file_contour.split('.')[0]+'.png')

    def draw_circle(self, rs, m, elev):
        angles = np.arange(0,360)
        lat, lon = heym.radial2latlon(rs.radar_range, angles, elev, rs.radar_lat, rs.radar_lon)
        x, y = m(lon, lat)
        m.plot(x, y, color='black', linewidth=1.5)


    #def make_natgrid(self, lat, lon, values, x, y):
        #import Ngl
        #grid = Ngl.natgrid(lon, lat, values, x[0,:], y[:,0]).T
        #return grid
        
    def PPI(self, rs, data, elev, moment, figname):
        figname = self.dirname+figname
        data = rs.cartesian(data[:,:,elev], elev)

        fig = plt.figure(figsize=(8,6))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        
        latmin, latmax, lonmin, lonmax = rs.radar_limits(elev)

        m = Basemap(projection='cyl', lon_0=rs.radar_lon, lat_0=rs.radar_lat,
                    llcrnrlat=latmin, urcrnrlat=latmax,
                    llcrnrlon=lonmin, urcrnrlon=lonmax,
                    resolution='h', suppress_ticks=True)
                    
        #m.drawcoastlines(color='0', linewidth=1)
        #m.drawstates(color='0', linewidth=1)
        #m.drawcountries(color='0', linewidth=1)
        #m.drawrivers(color='blue')
        #m.fillcontinents(color='#cc9955', lake_color='aqua', zorder = 0) #cor do continente
        #m.drawmapboundary(fill_color='aqua')                             #cor do mar

        parallels = np.arange(-90,0,1.)
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10,  linewidth=0.0)
        meridians = np.arange(180.,360.,1.)
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10,  linewidth=0.0)

        numcols, numrows = data.shape
        lons, lats = m.makegrid(numcols, numrows) # get lat/lons of ny by nx evenly space grid.
        x, y = m(lons, lats)                      # compute map proj coordinates.

        cmap, clevs, unit, title = cm.get_info(moment)
        norm = mpl.colors.BoundaryNorm(clevs, cmap.N)
        contour = m.contourf(x, y, data, clevs, cmap=cmap, norm=norm)

        cbar = m.colorbar(contour, cmap=cmap, norm=norm, spacing='uniform', location='right', pad='2%', size='5%')
        cbar.set_label(unit, rotation='horizontal')

        plt.title(title+u' (%.1f°)\n%s' % (rs.fixed_angle[elev], rs.date))

        self.draw_circle(rs, m, elev) #desenha o círculo do raio do radar
        plt.savefig(figname)
        #self.image_mask(figname, 'mask')
        #self.image_trim(figname) #recorta a imagem


    
