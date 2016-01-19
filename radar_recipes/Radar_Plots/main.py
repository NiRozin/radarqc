#coding: utf-8

import pyart
import numpy as np
import sys

from ReadRadarStructure import ReadRadarStructure
from Plot import Plot
plot = Plot()


"""
Creat a jpg with the lower elevation from the radar structure.

input:
    infile: str
        input filename

    outfile: str
        output filename

output:
    jpg that will be in images folder
    
Obs.:
        Use:  python main.py <input filename> <output filename>
"""

try:
    filename  = sys.argv[1]
    figname = sys.argv[2]
except:
    print "Use:  python main.py <input filename> <output filename>"
    print 'Exemplo: python main.py /discolocal/teste.hdf5 test_DBZH'
    sys.exit()


field = 'DBZH'

try:
    radar = pyart.aux_io.read_odim_h5(filename)
except:
    try:
        radar = pyart.aux_io.read_gamic(filename)
    except:
        try:
            radar = pyart.io.read(filename)
        except:
            print "Unknown file format"
            sys.exit()

#try:
#    radar.fields[field]['total_power'].mask[np.where(radar.fields[field]['total_power'].data<=15)]
#except:
#    radar.fields[field]['DBZH'].mask[np.where(radar.fields[field]['DBZH'].data<=15)]

rs = ReadRadarStructure(radar)
try:
    field = 'DBZH'
    values = rs.mount_volume(radar, field)
except:
    field = 'total_power'
    values = rs.mount_volume(radar, field)

#find lower elevation
e = np.argmin(rs.fixed_angle)

moment = 'DBZH'

plot.PPI(rs, values, e, moment, figname)

