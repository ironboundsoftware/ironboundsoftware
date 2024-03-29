"""
	__init__.py
	
	This is the main file for determining the potential ID of a satellite.
"""

import math 

__version__ = '1.0'

#
# Constants
PI = math.pi
twopi = 2*PI
radians_per_degree = (2*PI)/360
c = 299792458

#
# These are constants from the Spacetrack #3 fortran code.
ck2 = 5.413080e-4
ck4 = 0.62098875e-6
e6a = 1.0e-6
qoms2t = 1.88027916e-9
S = 1.01222928
twothird = 2/3.0 #TOTHRD 2/3 .66666667
xj3 = -0.253881e-5
xke = 0.743669161e-1
xkmper = 6378.135 #XKMPER kilometers/Earth radii 6378.135
minutes_per_day = 1440.0 #XMNPDA time units/day 1440.0
ae = 1.0 #AE distance units/Earth radii 1.0

#PIO2 pi/2 1.57079633

#X3PIO2 3pi/2 4.71238898
