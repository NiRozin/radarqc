#-*- coding: utf-8 -*-

import os
import h5py
import copy

"""
Some brazilian hdf5 radar structure has the pulse_width_mks attribute. This attribute
leads to KeyError: "can't open attribute (Attribute: Can't open object)"

This script add the pulse_width_us attribute in h5_file[scan]['how'].attrs field.
Not exclude the pulse_width_mks field and solve the KeyError from pulse_width_mks.

input:
    infile: str
        input filename of file in hdf5 format
output:
    h5: file
        file in hdf5 format
  
"""
try:
    infile  = sys.argv[1] 
except:
    print "Usage:  python mks_correct.py  <input filename>"
    sys.exit()

#add write permission
os.system('chmod 644 ' + infile)
#print  os.system('ls -l ' + filename)
h5 = h5py.File(infile, 'r+')
scans = [scan for scan in h5.keys() if scan.startswith('scan')]
for scan in scans:
    h5[scan]['how'].attrs['pulse_width_us'] =  h5[scan]['how'].attrs['pulse_width_mks']

h5.close()
#take out write permission (only read)
os.system('chmod 444 ' + infile)
