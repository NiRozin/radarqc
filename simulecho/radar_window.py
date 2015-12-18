# -*- coding:utf8 -*-
#lats/lons --> TXS, CAS, PARAGUAY


import gtk
import pygtk

class radar_selection():
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat
        self.lons = [-50.36133, -53.525356, -57.523335]
        self.lats = [-25.505314, -24.875566, -25.333055]
    
    
    def set_coord(self, widget, idx):
        self.lon = self.lons[idx]
        self.lat = self.lats[idx]
    
    
    def return_coord(self):
        return self.lon, self.lat
    
    
    def rad_window(self):
        window = gtk.Window()
        window.set_title("Radars")
        window.set_size_request(400,400)
        window.connect("destroy",lambda w: gtk.main_quit())
        #Teixeira Soares
        txs_box = gtk.HBox(False,0)
        txs_box.set_border_width(5)
        #
        button = gtk.Button("Teixeira Soares")
        button.connect("clicked", self.set_coord, 0)
        button.connect_object("clicked", gtk.Widget.destroy, window)
        #
        txs_box.pack_start(button)
        #Cascavel
        cas_box = gtk.HBox(False,0)
        cas_box.set_border_width(5)
        #
        button = gtk.Button("Cascavel")
        button.connect("clicked", self.set_coord, 1)
        button.connect_object("clicked", gtk.Widget.destroy, window)
        #
        cas_box.pack_start(button)
        #Paraguay
        par_box = gtk.HBox(False,0)
        par_box.set_border_width(5)
        #
        button = gtk.Button("Paraguay")
        button.connect("clicked", self.set_coord, 2)
        button.connect_object("clicked", gtk.Widget.destroy, window)
        #
        par_box.pack_start(button)
        #
        vbox = gtk.VBox(False,0)
        vbox.pack_start(txs_box,False)
        vbox.pack_start(cas_box,False)
        vbox.pack_start(par_box,False)
        #
        window.add(vbox)
        window.show_all()
        gtk.main()