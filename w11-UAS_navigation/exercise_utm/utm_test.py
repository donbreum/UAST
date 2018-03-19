#!/usr/bin/env python
#*****************************************************************************
# UTM projection conversion test
# Copyright (c) 2013-2016, Kjeld Jensen <kjeld@frobomind.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#*****************************************************************************
"""
This file contains a simple Python script to test the UTM conversion class.

Revision
2013-04-05 KJ First version
2015-03-09 KJ Minor update of the license text.
2016-01-16 KJ Corrected a minor problem with the library location reference.
"""
# import utmconv class
from utm import utmconv
from math import pi, cos, acos, sin
# define test position
#test_lat =  55.47
#test_lon = 010.33

test_lat =  42.160771
test_lon = 024.747739

print ('Test position [deg]:')
print ('  latitude:  %.10f'  % (test_lat))
print ('  longitude: %.10f'  % (test_lon))
#N55.47 E010.33
# instantiate utmconv class
#uc = utm.from_latlon(lat, lon)
uc = utmconv()

# convert from geodetic to UTM
(hemisphere, zone, letter, easting, northing) = uc.geodetic_to_utm (test_lat,test_lon)
print ('\nConverted from geodetic to UTM [m]')
print ('  %d %c %.5fe %.5fn' % (zone, letter, easting, northing))


# convert back from UTM to geodetic
(lat, lon) = uc.utm_to_geodetic (hemisphere, zone, easting, northing)
print ('\nConverted back from UTM to geodetic [deg]:')
print (' Original latitude:  %.10f'  % (lat))
print (' Original longitude: %.10f'  % (lon))
lat11=lat
lon11=lon
lat=lat*(pi/(180))
lon=lon*(pi/(180))

###########################################################################
easting1 = easting + 1000
print ('  %d %c %.5fe %.5fn' % (zone, letter, easting1, northing))

# convert back from UTM to geodetic
(lat1, lon1) = uc.utm_to_geodetic (hemisphere, zone, easting1, northing)
print ('\nConverted back from UTM to geodetic [deg]:')
print (' Easting latitude:  %.10f'  % (lat1))
print (' Easting longitude: %.10f'  % (lon1))

lat1=lat1*(pi/(180))
lon1=lon1*(pi/(180))

dist_east=acos(sin(lat1)*sin(lat)+cos(lat1)*cos(lat)*cos(lon1-lon)) #Distance between points
print ('  Easting distance: %.10f'  % (dist_east))

distance_east=1852*((180*60)/pi)*dist_east
print ('  Easting distance in meters: %.10f'  % (distance_east))


########################################################################


northing2 = northing + 1000
print ('  %d %c %.5fe %.5fn' % (zone, letter, easting, northing2))

## convert back from UTM to geodetic
#(lat, lon) = uc.utm_to_geodetic (hemisphere, zone, easting, northing)
#print ('\nConverted back from UTM to geodetic [deg]:')
#print (' Original latitude:  %.10f'  % (lat))
#print (' Original longitude: %.10f'  % (lon))

# convert back from UTM to geodetic
(lat2, lon2) = uc.utm_to_geodetic (hemisphere, zone, easting, northing2)
print ('\nConverted back from UTM to geodetic [deg]:')
print (' Northing latitude:  %.10f'  % (lat2))
print (' Northing longitude: %.10f'  % (lon2))


lat2=lat2*(pi/(180))
lon2=lon2*(pi/(180))
#ftp://ftp.bartol.udel.edu/anita/amir/My_thesis/Figures4Thesis/CRC_plots/Aviation%20Formulary%20V1.46.pdf
dist_north = acos(sin(lat2)*sin(lat)+cos(lat2)*cos(lat)*cos(lon2-lon))
print ('  Northing distance: %.10f'  % (dist_north))
distance_north=1852*((180*60)/pi)*dist_north
print ('  North distance in meters: %.10f'  % (distance_north))


#XTD =asin(sin(dist_AD)*sin(distance_east-distance_north))


# detrmine conversion position error [m]
lat_err = abs(lat11-test_lat)
lon_err = abs(lon11-test_lon)
earth_radius = 6378137.0 # [m]
lat_pos_err = lat_err/360.0 * 2*pi*earth_radius
lon_pos_err = lon_err/360.0 * 2*pi*(cos(lat)*earth_radius)
print ('\nPositional error from the two conversions [m]:')
print ('  latitude:  %.10f'  % (lat_pos_err))
print ('  longitude: %.10f'  % (lon_pos_err))


# detrmine conversion position error [m]
lat_err = abs(lat1-lat2)
lon_err = abs(lon1-lon2)
earth_radius = 6378137.0 # [m]
lat_pos_err = lat_err/360.0 * 2*pi*earth_radius
lon_pos_err = lon_err/360.0 * 2*pi*(cos(lat)*earth_radius)
print ('\nPositional error from the two conversions [m]:')
print (' Error latitude:  %.10f'  % (lat_pos_err))
print (' Error longitude: %.10f'  % (lon_pos_err))
