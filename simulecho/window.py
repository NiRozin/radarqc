# -*- coding:utf8 -*-

import gtk
import pygtk
from simul_echo import Rad_sim
from radar_window import radar_selection

#Callback functions
def simulate(widget,entry,entry2, entry_lon, entry_lat,radar):
    lon, lat = radar.simulate(elev=float(entry.get_text()),
                              lon=float(entry_lon.get_text()),
                              lat=float(entry_lat.get_text()),
                              topography=float(entry2.get_text()))
    entry_lon.set_text(str(lon))
    entry_lat.set_text(str(lat))
    
    
def set_basemap(widget,entry,topography):
    if topography==1:
        entry.set_text("1")
    else:
        entry.set_text("0")


def known_radars(widget,entry_lon,entry_lat):
    known = radar_selection()
    known.rad_window()
    lon, lat = known.return_coord()
    entry_lon.set_text(str(lon))
    entry_lat.set_text(str(lat))
    
        
#Sets the window    
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_title("Simulecho")
window.set_size_request(400,400)
window.connect("destroy",gtk.main_quit)
#Box that packs everything
vbox = gtk.VBox(False,0)
vbox.set_border_width(5)
#Elevation box
elev_box = gtk.HBox(False,0)
elev_box.set_border_width(5)
#Longitude box
lon_box = gtk.HBox(False,0)
lon_box.set_border_width(5)
#Latitude box
lat_box = gtk.HBox(False,0)
lat_box.set_border_width(5)
#Check box for Map or Topography
check_box = gtk.HBox(False,0)
check_box.set_border_width(5)
#Known radars box
known_box = gtk.HBox(False,0)
known_box.set_border_width(5)
#Packing the boxes
vbox.pack_start(elev_box,False)
vbox.pack_start(lon_box,False)
vbox.pack_start(lat_box,False)
vbox.pack_start(check_box,False)
vbox.pack_start(known_box,False)
#Topography 0 or 1
entry2 = gtk.Entry()
entry2.set_editable(True)
entry2.set_text("0")
#Check button for the Map
check_map = gtk.RadioButton(None, "Map")
check_map.connect("toggled",set_basemap,entry2,0)
check_box.pack_start(check_map)
#Check button for the Topography
check_topography = gtk.RadioButton(check_map, "Topography")
check_topography.connect("toggled",set_basemap,entry2,1)
check_box.pack_start(check_topography)
#Entry for the Elevation
entry1 = gtk.Entry()
entry1.set_editable(True)
entry1.set_text("0.3")
label = gtk.Label("Elevation:     ")
elev_box.pack_start(label)
elev_box.pack_start(entry1)
label = gtk.Label("degrees")
elev_box.pack_start(label)
#Entry for the Longitude
entry_lon = gtk.Entry()
entry_lon.set_editable(True)
entry_lon.set_text(str(-50.36111))
label = gtk.Label("Longitude:    ")
lon_box.pack_start(label)
lon_box.pack_start(entry_lon)
label = gtk.Label("degrees")
lon_box.pack_start(label)
#Entry for the Latitude
entry_lat = gtk.Entry()
entry_lat.set_editable(True)
entry_lat.set_text(str(-25.50528))
label = gtk.Label("Latitude:       ")
lat_box.pack_start(label)
lat_box.pack_start(entry_lat)
label = gtk.Label("degrees")
lat_box.pack_start(label)
#Known radars button
button = gtk.Button("Radars")
button.connect("clicked",known_radars,entry_lon,entry_lat)
known_box.pack_start(button)
#Rad_sim object that contains the topography data and the street map
radar = Rad_sim()
#A box to pack the Start and Close buttons
hbox = gtk.HBox(False,0)
hbox.set_border_width(5)
#Start an Close buttons
button = gtk.Button("Start")
button.connect("clicked",simulate,entry1,entry2,entry_lon,entry_lat,radar)
hbox.pack_start(button)
button = gtk.Button("Close")
button.connect("clicked",lambda w: gtk.main_quit())
hbox.pack_start(button)
#Packs hbox to vbox
vbox.pack_start(hbox,False)
#Adds vbox to the window, shows all and calls the loop
window.add(vbox)
window.show_all()
gtk.main()