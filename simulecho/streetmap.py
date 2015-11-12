import urllib
import io
import Image

def street_map(ll_lon, ll_lat, ur_lon, ur_lat, res):
    URL='http://ows.terrestris.de/osm/service/?LAYERS=OSM-WMS&SERVICE=WMS&VERSION=1.1'\
    +'.1&REQUEST=GetMap&STYLES=&FORMAT=image/jpeg&SRS=EPSG:4326&BBOX='+str(ll_lon)+','\
    +str(ll_lat)+','+str(ur_lon)+','+str(ur_lat)+'&WIDTH='+str(res[0])\
    +'&HEIGHT='+str(res[1])
    image_str = urllib.urlopen(URL).read()
    image_buffer = io.BytesIO(image_str)
    image = Image.open(image_buffer).convert("RGB")
    return image