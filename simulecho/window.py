# -*- coding:utf8 -*-

import gtk
import pygtk
from simul_echo import Rad_sim
    
    
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.set_title("Simulecho")
window.set_size_request(400,400)
window.connect("destroy",gtk.main_quit)

def simulate(widget,entry,entry2):
    radar = Rad_sim()
    radar.simulate(elev=float(entry.get_text()), topography=float(entry2.get_text())) 
    

def set_basemap(widget,entry,topography):
    if topography==1:
        entry.set_text("1")
    else:
        entry.set_text("0")

#
vbox = gtk.VBox(False,0)
vbox.set_border_width(5)
#
elev_box = gtk.HBox(False,0)
elev_box.set_border_width(5)
#
vbox.pack_start(elev_box,False)
#
check_box = gtk.HBox(False,0)
check_box.set_border_width(5)
#
vbox.pack_start(check_box,False)
#
entry2 = gtk.Entry()
entry2.set_editable(True)
entry2.set_text("0.3")
#
check_map = gtk.RadioButton(None, "Map")
check_map.connect("toggled",set_basemap,entry2,0)
check_box.pack_start(check_map)
#
check_topography = gtk.RadioButton(check_map, "Topography")
check_topography.connect("toggled",set_basemap,entry2,1)
check_box.pack_start(check_topography)
#
hbox = gtk.HBox(False,0)
hbox.set_border_width(5)
#
entry1 = gtk.Entry()
entry1.set_editable(True)
entry1.set_text("0.3")
label = gtk.Label("Elevation:")
elev_box.pack_start(label)
elev_box.pack_start(entry1)
label = gtk.Label("degrees")
elev_box.pack_start(label)
#
vbox.pack_start(hbox,False)
#
button = gtk.Button("Start")
button.connect("clicked",simulate,entry1,entry2)
hbox.pack_start(button)
button = gtk.Button("Close")
button.connect("clicked",lambda w: gtk.main_quit())
hbox.pack_start(button)
#
window.add(vbox)
window.show_all()
gtk.main()