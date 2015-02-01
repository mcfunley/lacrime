#!/bin/bash

download() {
  wget --no-clobber --output-document=data/$1.csv "http://shq.lasdnews.net/CrimeStats/CAASS/$1-PART_I_AND_II_CRIMES.csv" 
}

mkdir -p data
download "2005"
download "2006"
download "2007"
download "2008"
download "2009"
download "2010"
download "2011"
download "2012"
download "2013"
wget --no-clobber --output-document=data/2014.csv "https://data.lacity.org/api/views/eta5-h8qx/rows.csv?accessType=DOWNLOAD"
wget --no-clobber --output-document=data/la_city.kml "https://s3-us-west-2.amazonaws.com/mappingla.com/downloads/neighborhoods/la_city.kml"
wget --no-clobber --output-document=data/last30.csv "http://shq.lasdnews.net/CrimeStats/CAASS/PART_I_AND_II_CRIMES.csv"

wget --no-clobber --output-document=data/cb_2013_us_zcta510_500k.zip "http://www2.census.gov/geo/tiger/GENZ2013/cb_2013_us_zcta510_500k.zip"
pushd data
unzip cb_2013_us_zcta510_500k.zip
popd
