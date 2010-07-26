import os
from django.contrib.gis.utils import LayerMapping
from models import Town

town_mapping = {
    'town_id' : 'town_id',
    'town_name' : 'town_name',
    'type' : 'type',
    'geometry' : 'MULTIPOLYGON',
}

town_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/towns.shp'))

def run(verbose=True):
    lm = LayerMapping(Town, town_shp, town_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)