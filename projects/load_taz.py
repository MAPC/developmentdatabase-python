import os
from django.contrib.gis.utils import LayerMapping
from models import Taz, Town

taz_mapping = {
    'taz_id' : 'taz_id',
    'town_id' : 'town_id',
    'town_name' : 'town_name',
    'x' : 'x',
    'y' : 'y',
    'geometry' : 'MULTIPOLYGON',
}

taz_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/taz.shp'))

def run(verbose=True):
    lm = LayerMapping(Taz, taz_shp, taz_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)