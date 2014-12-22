#!/usr/bin/env python
from csv import DictReader
import os
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta
from datetime_truncate import truncate
from collections import defaultdict
from operator import itemgetter
from numpy import array, zeros


dates = defaultdict(int)
years = set()

for fn in os.listdir('data'):
    for d in DictReader(open('data/'+fn, 'r'), delimiter=','):
        if d['CATEGORY'] != 'LARCENY THEFT':
            continue

        d = truncate(parse_date(d['INCIDENT_DATE']), 'day')
        if d.year < 2009 or d.year > 2013:
            continue
        
        dates[d] += 1
        years.add(d.year)


print '\t'.join(['date'] + map(str, list(sorted(years))))

d = datetime(2013, 1, 1)
while d <= datetime(2014, 1, 1):
    week_begin = d
    stats = zeros(len(years))
    for _ in range(7):
        stats += array([
            dates[datetime(y, d.month, d.day)] for y in sorted(years)
        ])
        d += timedelta(days=1)

    print '\t'.join(
        [week_begin.strftime('%m-%d')] + [str(int(s)) for s in stats]
    )
    
