#!/usr/bin/env python
from csv import DictReader
from dateutil.parser import parse as parse_date
from datetime_truncate import truncate
from numpy import array, zeros
from BeautifulSoup import BeautifulStoneSoup as bss
import shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class ZipCode(object):
    def __init__(self, code):
        self.code = code
        self.polygon = self.get_polygon()

        
    def get_polygon(self):
        sf = shapefile.Reader('data/cb_2013_us_zcta510_500k.dbf')
        index = [
            i for (i, r) in enumerate(sf.records()) if r[0] == str(self.code)
        ][0]
        
        shape = sf.shape(index)
        return Polygon([(lat, lon) for (lon, lat) in shape.points])

    
    def contains(self, lat, lon):
        return self.polygon.contains(Point(float(lat), float(lon)))


eagle_rock = ZipCode(90041)


def emit_normalized_file(relpath, max_year):
    cat_whitelist = ('LARCENY THEFT', 'GRAND THEFT AUTO', 'BURGLARY', 'ROBBERY',)

    for d in DictReader(open(relpath, 'r'), delimiter=','):
        if d['CATEGORY'] not in cat_whitelist:
            continue

        day = truncate(parse_date(d['INCIDENT_DATE'], 'day'))
        if d.year > max_year:
            continue

        if d['ZIP'] != '90041':
            continue

        
        

def emit_geo_file(relpath):
    pass


def emit_property_crime():
    # years 2005-2013 all have fairly normalized data, from here:
    # http://shq.lasdnews.net/CrimeStats/CAASS/desc.html
    for _ in range(2005, 2014):
        emit_normalized_file('data/%s.csv', 2013)

    # for 2014 the only source as of this writing is from the newer
    # data.lacity.org.
    # here we have to sort out what's in eagle rock using the geo
    # coordinates in the file.
    emit_geo_file('data/2014.csv')

    # there's a last 30 days file, which coincidentally as of this
    # writing covers January, 2015.
    emit_normalized_file('data/last30.csv')


def main():
    pass

    
if __name__ == '__main__':
    main()
