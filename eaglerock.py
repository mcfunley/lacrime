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


def emit_normalized_file(relpath, year):
    cat_whitelist = ('LARCENY THEFT', 'GRAND THEFT AUTO', 'BURGLARY', 'ROBBERY',)

    for d in DictReader(open(relpath, 'r'), delimiter=','):
        cat = d['CATEGORY']
        if cat not in cat_whitelist:
            continue

        day = truncate(parse_date(d['INCIDENT_DATE']), 'day')
        # allow for late reporting
        if day.year not in (year, year-1):
            continue

        if d['ZIP'] != '90041':
            continue

        if d['DELETED'] != 'N':
            continue

        emit_crime(day, cat)
        
        

def emit_geo_file(relpath, year):
    category_patterns = (
        'VEHICLE - STOLEN', 'THEFT FROM MOTOR VEHICLE - PETTY ($950.01 & OVER)',
        'ROBBERY', 'THEFT', 'BURGLARY', 'BIKE - STOLEN', 'THEFT-GRAND',
    )

    for d in DictReader(open(relpath, 'r'), delimiter=',', quotechar='"'):
        description = d['Crm Cd Desc']
        if not any([p in description for p in category_patterns]):
            continue

        if 'ATTEMPT' in description:
            continue

        day = truncate(parse_date(d['DATE OCC']), 'day')
        if day.year not in (year, year-1):
            continue

        latlon = d['Location 1'].strip('()').split(',')
        if len(latlon) != 2:
            continue
            
        if not eagle_rock.contains(*latlon):
            continue

        emit_crime(day, description)
                

def emit_property_crime():
    # years 2005-2013 all have fairly normalized data, from here:
    # http://shq.lasdnews.net/CrimeStats/CAASS/desc.html
    for y in range(2005, 2014):
        emit_normalized_file('data/%s.csv' % y, y)

    # for 2014 the only source as of this writing is from the newer
    # data.lacity.org.
    # here we have to sort out what's in eagle rock using the geo
    # coordinates in the file.
    emit_geo_file('data/2014.csv', 2014)

    # there's a last 30 days file, which coincidentally as of this
    # writing covers January, 2015.
    emit_normalized_file('data/last30.csv', 2015)


workfile = None
    
def emit_crime(day, description):
    global workfile
    print >>workfile, '%s\t%s' % (day, description)
    

def main():
    global workfile
    workfile = open('work/ercrimes.tsv', 'w')
    emit_property_crime()

    
if __name__ == '__main__':
    main()
