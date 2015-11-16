# -*- coding:utf8 -*-

#RME: lat=-19.94528, lon=-44.43444
#TXS: lat=-25.50528, lon =-50.36111
#CAS: lat=-24.87000, lon=-53.40000

from simulecho import Rad_sim

radarTXS = Rad_sim() #It is set to Teixeira Soares, elevation 0.3°
radarTXS.simulate() #If the altitude is not given, it uses the data