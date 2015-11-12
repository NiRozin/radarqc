# -*- coding:utf8 -*-

#RME: lat=-19.94528, lon=-44.43444
#TXS: lat=-25.50528, lon =-50.36111
#CAS: lat=-24.87000, lon=-53.40000

from simulecho import Rad_sim

radarTXS = Rad_sim() #It is set to Teixeira Soares, elevation 0.3°
radarTXS.echo()

radarCAS = Rad_sim() #If the altitude is not given, it uses the data
radarCAS.echo(lat=-24.87000, lon=-53.40000, elev=0.4)
radarCAS.echo(lat=-24.87000, lon=-53.40000, alt = 719.81,elev=0.4)

radarRME = Rad_sim()
radarRME.echo(lat=-19.94528, lon=-44.43444)
