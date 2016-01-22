#-*- coding: utf-8 -*-

import pyart
import os
from glob import glob

"""
Get together odim format files from cemadem radar.

input:
    infile: str
        input filename
    outfile: str
        output filename
output:
    grid: file
        file in uf format with all fildes avaliable
"""
      
try:
    infile  = sys.argv[1] 
    outfile  = sys.argv[2] 
except:
    print "Use:  python odim_together.py <input filename> <output filename>"
    sys.exit()
    
#filename = 'JGI-250--2015-07-30--00-05-07'
#dir_in = '/simepar/radar/cemaden/jgi/n2/hdf5odim/2015/07/30/'

#search all files with the same data
dir_in = infile[:50]
lista = os.listdir(dir_in)
filename = infile[50:79]
#search all files with the same data
arqs = [arq for arq in lista if arq.startswith(filename)]
lista = []

#complete filenames
for arq in arqs:
    lista = lista + glob(dir_in + arq)
    
#radar reading
radars = [pyart.aux_io.read_odim_h5(arq, file_field_names=False) for arq in lista]

#adding radar fields
radar = radars[0]
for r in radars:
    field = r.fields.keys()[0]
    dic = r.fields[field]
    radar.add_field(field, dic, replace_existing=True)

#write the radar in uf format
pyart.io.write_uf(outfile, radar)
#pyart.io.write_uf('/discolocal/tulipa/JGI-250--2015-07-30--00-05-07.uf', radar)