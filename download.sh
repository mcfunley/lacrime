#!/bin/bash

download() {
  wget --no-clobber --output-document=data/$1.csv "http://shq.lasdnews.net/CrimeStats/CAASS/$1-PART_I_AND_II_CRIMES.csv" 
}

mkdir -p data
download "2004"
download "2005"
download "2006"
download "2007"
download "2008"
download "2009"
download "2010"
download "2011"
download "2012"
download "2013"
download "2014"

