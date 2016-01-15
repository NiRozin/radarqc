#coding: utf-8

import pyart
import numpy as np

from ReadRadarStructure import ReadRadarStructure
from Plot import Plot
plot = Plot()

#colocar strutura de argv

filename = 'MC1-250--2016-01-11--00-00-03dBuZ.hdf5'
field = 'DBZH'
#ler radar

#colocar try except para plotar todos os tipos...ou quase
radar = pyart.aux_io.read_odim_h5(filename)

#verificar a questão do sweep a ser plotado...
radar.fields[field]['data'].mask[np.where(radar.fields[field]['data'].data<=)]

rs = ReadRadarStructure(radar)
values = rs.mount_volume(radar, field)

#find lower elevation
e = np.argmin(rs.fixed_angle)

moment = 'DBZH'
figname = 'imagem_DBZH'
plot.PPI(rs, values, e, moment, figname)

