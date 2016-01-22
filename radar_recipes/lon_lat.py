import pyart
import wradlib
import numpy as np

radar = pyart.io.read("/simepar/radar/simepar/txs/n2/sigmet/2015/06/15/TXS150615233725.RAWAB6Z.gz")
r = radar.range['data']

elev = [0.5, 1., 1.5, 2., 3., 4., 6., 8.]
sitecoords = (-25.505314, -50.36133, 1016.08)
for i in xrange(14):
    for j in xrange(360):
        lon,lat,alt = wradlib.georef.polar2lonlatalt_n(r, j*np.ones(960), elev[i]*np.ones(960), sitecoords)
        M = np.array([lon,lat])
        np.savetxt("lon_lat_TXS_" + str(i) + ".txt",M)