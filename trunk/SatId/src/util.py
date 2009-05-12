'''
util.py
	Utility functions for SatId
	
Created on May 5, 2009

@author: nick.loadholtes

This is what to duplicate (from observe.cpp):


void DLL_FUNC get_satellite_ra_dec_delta( const double *observer_loc,
                                 const double *satellite_loc, double *ra,
                                 double *dec, double *delta)
{
   double vect[3], dist2 = 0.;
   int i;

   for( i = 0; i < 3; i++)
      {
      vect[i] = satellite_loc[i] - observer_loc[i];
      dist2 += vect[i] * vect[i];
      }
   *delta = sqrt( dist2);
   *ra = atan2( vect[1], vect[0]);
   if( *ra < 0.)
      *ra += PI + PI;
   *dec = asin( vect[2] / *delta);
}

void DLL_FUNC epoch_of_date_to_j2000( const double jd, double *ra, double *dec)
{
   const double t_centuries = (jd - 2451545.) / 36525.;
   const double m = (3.07496 + .00186 * t_centuries / 2.) * (PI / 180.) / 240.;
   const double n = (1.33621 - .00057 * t_centuries / 2.) * (PI / 180.) / 240.;
   const double ra_rate  = m + n * sin( *ra) * tan( *dec);
   const double dec_rate = n * cos( *ra);

   *ra -= t_centuries * ra_rate * 100.;
   *dec -= t_centuries * dec_rate * 100.;
}

'''

import math

#
# Constants
PI = math.pi
radians_per_degree = (2*PI)/360
c = 299792458


