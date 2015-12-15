# -*- coding:utf8 -*-

#Input: latitude, longitude, raio de cobertura
#       altura da torre, altura até a posição do alimentador
#       elevação da antena em graus
#       posição angular dos lóbulos em graus (lóbulo principal = 0°)
#       ângulo de abertura dos lóbulos em graus

import numpy as np
import matplotlib.pyplot as plt
import wradlib
from netCDF4 import Dataset
from streetmap import street_map
from zoompan import ZoomPan

class Rad_sim():
    def __init__(self):
        self.units = {'distance': 'm', 'angles': 'dg', 'raio_area': 'Km'}
        data = Dataset("data/etopo1_bedrock.nc")
        self.topo_data = data.variables['Band1'][:]
        #self.topo_data[np.where(self.topo_data < -30)] = -1000
        self.lon_data = data.variables['lon'][:]
        self.lat_data = data.variables['lat'][:]
        self.ux, self.uy = self.topo_data.shape
        self.base_map = street_map(self.lon_data[0], self.lat_data[0],
                                self.lon_data[self.uy-1], self.lat_data[self.ux-1],
                                (self.uy+2800,self.ux+2520))
        self.fig = plt.figure(figsize=[10,8])
    
    def find_area(self):
        #ll = lower left and ur = upper right
        lon_lat_dist = self.radius/111.276
        ll_lon = self.lon - lon_lat_dist
        ll_lat = self.lat - lon_lat_dist
        ur_lon = self.lon + lon_lat_dist
        ur_lat = self.lat + lon_lat_dist
        return ll_lon, ll_lat, ur_lon, ur_lat


    def get_area(self,topography):
        lon_lat_dist = self.radius/111.276
        ll_lon = self.lon - lon_lat_dist
        ll_lat = self.lat - lon_lat_dist
        ur_lon = self.lon + lon_lat_dist
        ur_lat = self.lat + lon_lat_dist
        lat1, lon1 = self.lat_data[0], self.lon_data[0]
        dx = abs(lat1 - self.lat)
        dy = abs(lon1 - self.lon)
        #resolution -> one minute
        dx = int(np.round(dx*60))
        dy = int(np.round(dy*60))
        lon_lat_dist = int(lon_lat_dist*60)
        lon_lat_dist = min(lon_lat_dist,dx,dy,self.ux-dx,self.uy-dy)
        ll_x = dx - lon_lat_dist
        ll_y = dy - lon_lat_dist
        ur_x = dx + lon_lat_dist
        ur_y = dy + lon_lat_dist
        if topography==0:
            dx = abs(lat1 - self.lat)
            dy = abs(lon1 - self.lon)
            dx = int(np.round(dx*95.013))
            dy = int(np.round(dy*95.013))
        return self.topo_data[ll_x:ur_x,ll_y:ur_y], (dx,dy)


    def height(self, T, M, azi, n, lim):
        T1 = np.zeros(lim)
        k = 0
        ang = np.deg2rad(90-azi)
        tg = np.tan(ang)
        if azi <= 90:
            a = -1
            b = 1
        elif azi < 180:
            a = 1
            b = 1
        elif azi <= 270:
            a = 1
            b = -1
        elif azi < 360:
            a = -1
            b = -1
        for i in xrange(lim):
            j = abs(int(np.round(tg*i)))
            if j < lim:
                k += 1
                if T[a*j-n,b*i+n] > 0:
                    T1[i] = T[a*j-n,b*i+n]
            else:
                break
        x = 111.276/60*1000*np.linspace(0, lim, k, endpoint=True)
        LP = self.elev + self.pos_LP
        #LP1 = LP + self.ang_LP/2.
        LP2 = LP - self.ang_LP/2.
        #LS1 = self.elev + self.pos_1LS
        #LS11 = LS1 + self.ang_1LS/2.
        #LS12 = LS1 - self.ang_1LS/2.
        #LS2 = self.elev + self.pos_2LS
        #LS21 = LS2 + self.ang_2LS/2.
        #LS22 = LS2 - self.ang_2LS/2.
        #LS3 = self.elev + self.pos_3LS
        #LS31 = LS3 + self.ang_3LS/2.
        #LS32 = LS3 - self.ang_3LS/2.
        ones = np.ones(len(x))
        #elev = np.array([LP1*ones,LP2*ones,LS11*ones,LS12*ones,LS21*ones,LS22*ones,LS31*ones,LS32*ones])
        elev = LP2
        lon, lat, alt = wradlib.georef.polar2lonlatalt_n(x, azi, elev, (self.lon,self.lat,self.total_h))
        #T1[0]+self.tower_h+self.h
        for i in xrange(len(x)):
            if T1[i] >= alt[i]:
                j = abs(int(np.round(tg*i)))
                M[a*j-lim,b*i+lim] = 1
        return M
      
    def show_image(self, M, M_size, center, topography=0,cbar=1):
        ll_lon, ll_lat, ur_lon, ur_lat = self.find_area()
        #fig = plt.figure(figsize=[10,8])
        ax = self.fig.add_subplot(111)
        plt.title("lon = " + str(self.lon) + " e lat = " + str(self.lat) \
                + "\nelev = " + str(self.elev))
        if topography==1:
            plt.imshow(self.topo_data,cmap=plt.cm.gist_earth,vmin=-1600,vmax=2000,origin='lower',hold=False)
            if cbar==1:
                plt.colorbar()
        else:
            plt.imshow(self.base_map,origin='lower',hold=False)
        plt.plot(center[1],center[0],'kx',markersize=10)
        xyticks = 9
        ll_lon = self.lon_data[0]
        ll_lat = self.lat_data[0]
        ur_lon = self.lon_data[self.uy-1]
        ur_lat = self.lat_data[self.ux-1]
        if topography==1:
            xticks = self.uy
            yticks = self.ux
        else:
            xticks = self.uy + 2800
            yticks = self.ux + 2520
        length = 20
        x = np.linspace(ll_lon,ur_lon,length)
        y = np.linspace(ll_lat,ur_lat,length)
        for i in xrange(length):
            x[i] = "%.3f"%x[i]
        for i in xrange(length):
            y[i] = "%.3f"%y[i]
        plt.xlabel("Longitude")
        plt.xticks(np.linspace(0,xticks,length),x)
        plt.ylabel("Latitude")
        plt.yticks(np.linspace(0,yticks,length),y)
        for i in xrange(2*M_size):
            for j in xrange(2*M_size):
                if M[2*M_size-1-i,2*M_size-1-j] == 1:
                    plt.plot(center[1]+M_size-j,center[0]+M_size-i,'o',markersize=1,color='red')
        return ax

    def echo(self,lon=-50.36111,lat=-25.50528, radius=150, tower_h=25.,
                h=4.5, elev=0.3, pos_LP=0., pos_1LS=-2.7, pos_2LS=-1.9, pos_3LS=-1.3,
                ang_LP=1., ang_1LS=0.5, ang_2LS=0.25, ang_3LS=0.125, alt=None,topography=0,cbar=1):
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.tower_h = tower_h
        self.h = h
        self.elev = elev
        self.pos_LP = pos_LP
        self.pos_1LS = pos_1LS
        self.pos_2LS = pos_2LS
        self.pos_3LS = pos_3LS
        self.ang_LP = ang_LP
        self.ang_1LS = ang_1LS
        self.ang_2LS = ang_2LS
        self.ang_3LS = ang_3LS
        self.alt = alt
        T, center = self.get_area(topography)
        n = np.min(T.shape)
        n2 = n/2
        if self.alt==None:
            self.alt = T[n2,n2]
        self.total_h = self.alt + self.tower_h + self.h
        lim = int(self.radius/111.276*60)
        M = np.zeros((2*lim,2*lim))
        for azi in xrange(360):
            M = self.height(T,M,azi,n2,lim)
        #plot
        ax = self.show_image(M,lim,center,topography=topography,cbar=cbar)
        return ax
        
        
    def simulate(self,lon=-50.36111,lat=-25.50528, radius=150, tower_h=25.,
                h=4.5, elev=0.3, pos_LP=0., pos_1LS=-2.7, pos_2LS=-1.9, pos_3LS=-1.3,
                ang_LP=1., ang_1LS=0.5, ang_2LS=0.25, ang_3LS=0.125, alt=None,topography=0,cbar=1):
         ax = self.echo(lon,lat, radius, tower_h,
                h, elev, pos_LP, pos_1LS, pos_2LS, pos_3LS,
                ang_LP, ang_1LS, ang_2LS, ang_3LS, alt,topography=topography,cbar=1)
         ###
         zp = ZoomPan(ax,self.echo,self.lat_data[0],self.lon_data[0],
                      elev=self.elev,topography=topography)
         figZoom = zp.zoom_factory(ax, base_scale = 1.1)
         figPan = zp.pan_factory(ax)
         ###
         plt.show()
         return self.lon, self.lat