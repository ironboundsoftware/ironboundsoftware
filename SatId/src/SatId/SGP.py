'''
Created on May 14, 2009

@author: nick.loadholtes
'''
import formats.TLE as TLE
import SatId
#from SatId import *
import math

def SGP4(tle, tsince):
	"""
		An implementation of the SGP4 algorithm, from Space Track Report#3
		
	"""
	if None == tle:
		return (None, None, None)
	
	ck2 = SatId.ck2
	twothirds = SatId.twothird

#	* SGP4 3 NOV 80
#SUBROUTINE SGP4(IFLAG,TSINCE)
#
# input parameters
#
#COMMON/E1/XMO,XNODEO,OMEGAO,EO,XINCL,XNO,XNDT2O,
#1 XNDD6O,BSTAR,X,Y,Z,XDOT,YDOT,ZDOT,EPOCH,DS50

# These are constants defined in the __init__ file
#
#COMMON/C1/CK2,CK4,E6A,QOMS2T,S,TOTHRD,
#1 XJ3,XKE,XKMPER,XMNPDA,AE

#DOUBLE PRECISION EPOCH, DS50
#
# Prep the observation code (conversion to radians, etc.)
#XNDD6O=XNDD6O*(10.**IEXP) 
#XNODEO=XNODEO*DE2RA 
#OMEGAO=OMEGAO*DE2RA 
#XMO=XMO*DE2RA 
	#Mean motion already handled
	tle.ra *= SatId.radians_per_degree
	tle.perigee *= SatId.radians_per_degree
	tle.anomaly *= SatId.radians_per_degree

#XINCL=XINCL*DE2RA 
#TEMP=TWOPI/XMNPDA/XMNPDA 
#XNO=XNO*TEMP*XMNPDA 
#XNDT2O=XNDT2O*TEMP 
#XNDD6O=XNDD6O*TEMP/XMNPDA 
	tle.inclination *= SatId.radians_per_degree
	inittemp = SatId.twopi/SatId.minutes_per_day/SatId.minutes_per_day
	tle.meanMotion *= inittemp * SatId.minutes_per_day
	tle.firstDeriv *= inittemp
	tle.secondDeriv *= inittemp/SatId.minutes_per_day

#* INPUT CHECK FOR PERIOD VS EPHEMERIS SELECTED 
#* PERIOD GE 225 MINUTES IS DEEP SPACE 
#A1=(XKE/XNO)**TOTHRD 
#TEMP=1.5*CK2*(3.*COS(XINCL)**2-1.)/(1.-EO*EO)**1.5 
#DEL1=TEMP/(A1*A1) 
#AO=A1*(1.-DEL1*(.5*TOTHRD+DEL1*(1.+134./81.*DEL1))) 
#DELO=TEMP/(AO*AO) 
#XNODP=XNO/(1.+DELO) 
	a1 = (SatId.xke/tle.meanMotion) ** SatId.twothird
	inittemp = 1.5 * SatId.ck2 * (3.0 *math.cos(tle.inclination) ** 2 - 1.0)/ \
		(1.0 - tle.eccentricity * tle.eccentricity)**1.5
	initdel1 = inittemp/(a1*a1)
	a0 = a1 *(1.0 - initdel1*(0.5 * SatId.twothird + initdel1 * (1.0 +134.0/81.0 * initdel1)))
	initdel0 = inittemp/(a0*a0)
	xnodp = tle.meanMotion/(1.0 + initdel0)
	
# Next lines determine if it is deep space or not.
#IF((TWOPI/XNODP/XMNPDA) .GE. .15625) IDEEP=1 
#BSTAR=BSTAR*(10.**IBEXP)/AE 
#TSINCE=TS 
#IFLAG=1 

#IF (IFLAG .EQ. 0) GO TO 100

#
#* RECOVER ORIGINAL MEAN MOTION (XNODP) AND SEMIMAJOR AXIS (AODP)
#* FROM INPUT ELEMENTS
#

#A1=(XKE/XNO)**TOTHRD
	a1 = (SatId.xke / tle.meanMotion)** twothirds 
	
#COSIO=COS(XINCL)
#THETA2=COSIO*COSIO
#X3THM1=3.*THETA2-1.
	cosio = math.cos(tle.inclination)
	theta2 = cosio*cosio
	x3thm1 = 3 *(theta2 - 1)
	
#EOSQ=EO*EO
#BETAO2=1.-EOSQ
#BETAO=SQRT(BETAO2)
	eosquared = tle.eccentricity * tle.eccentricity
	beta_o2 = 1.0 - eosquared
	beta_o = math.sqrt(beta_o2)
	
#DEL1=1.5*CK2*X3THM1/(A1*A1*BETAO*BETAO2)
#AO=A1*(1.-DEL1*(.5*TOTHRD+DEL1*(1.+134./81.*DEL1)))
#DELO=1.5*CK2*X3THM1/(AO*AO*BETAO*BETAO2)
#XNODP=XNO/(1.+DELO)
#AODP=AO/(1.-DELO)
	del1 = 1.5* ck2 *x3thm1/(a1*a1*beta_o*beta_o2)
	ao = a1*(1.0 - del1 * (0.5 * twothirds + del1 * (1.0 + 134.0/81.0 * del1)))
	delo = 1.5 * ck2 * x3thm1/(ao*ao * beta_o * beta_o2)
	xnodp = tle.meanMotion/(1.0 + delo)
	aodp = ao/(1.0-delo)

#
#* INITIALIZATION
#* FOR PERIGEE LESS THAN 220 KILOMETERS, THE ISIMP FLAG IS SET AND
#* THE EQUATIONS ARE TRUNCATED TO LINEAR VARIATION IN SQRT A AND
#* QUADRATIC VARIATION IN MEAN ANOMALY. ALSO, THE C3 TERM, THE
#* DELTA OMEGA TERM, AND THE DELTA M TERM ARE DROPPED.
#

#ISIMP=0
#IF((AODP*(1.-EO)/AE) .LT. (220./XKMPER+AE)) ISIMP=1
	isimp = 0
	if aodp*(1.0-tle.eccentricity)/SatId.ae < (220.0/SatId.xkmper + SatId.ae):
		isimp = 1

#
#* FOR PERIGEE BELOW 156 KM, THE VALUES OF
#* S AND QOMS2T ARE ALTERED
#

#S4=S
#QOMS24=QOMS2T
#PERIGE=(AODP*(1.-EO)-AE)*XKMPER
	s4 = SatId.S
	qoms24 = SatId.qoms2t
	perige = (aodp*(1.0-tle.eccentricity)-SatId.ae) * SatId.xkmper

#IF(PERIGE .GE. 156.) GO TO 10
	if perige < 156.0:
		print "goto 10"
	
	#S4=PERIGE-78.
		s4 = perige-78.0
	
	#
	# NOTE: Need to double check this section
	#	
	#IF(PERIGE .GT. 98.) GO TO 9
		if perige > 98.0:
			print "goto 9"
	#9 QOMS24=((120.-S4)*AE/XKMPER)**4
			qosm24 = ((120.0 - s4) * SatId.xkmper) ** 4
		else:
	#S4=20.
			s4 = 20.0
	
	#S4=S4/XKMPER+AE
		s4 = s4/SatId.xkmper+SatId.ae
		
#10 PINVSQ=1./(AODP*AODP*BETAO2*BETAO2)
#TSI=1./(AODP-S4)
#ETA=AODP*EO*TSI
#ETASQ=ETA*ETA
#EETA=EO*ETA
	pinvsq = 1.0/(aodp * aodp * beta_o2 * beta_o2)
	tsi = 1.0/(aodp - s4)
	eta = aodp * tle.eccentricity * tsi
	etasq = eta * eta
	eeta = tle.eccentricity * eta

#PSISQ=ABS(1.-ETASQ)
#COEF=QOMS24*TSI**4
#COEF1=COEF/PSISQ**3.5
#C2=COEF1*XNODP*(AODP*(1.+1.5*ETASQ+EETA*(4.+ETASQ))+.75*
#1 CK2*TSI/PSISQ*X3THM1*(8.+3.*ETASQ*(8.+ETASQ)))
#C1=BSTAR*C2
	psisq = abs(1.0-etasq)
	coef = qoms24 * tsi**4
	coef1 = coef/psisq**3.5
	c2 = coef1 * xnodp * (aodp *(1.0 + 1.5*etasq + eeta * (4.0 + etasq)) + 0.75
						* ck2 * tsi/psisq *x3thm1 * (8.0 + 3.0 * etasq * (8.0 + etasq)))
	c1 = tle.bStarDrag * c2
	
#SINIO=SIN(XINCL)
#A3OVK2=-XJ3/CK2*AE**3
#C3=COEF*TSI*A3OVK2*XNODP*AE*SINIO/EO
#X1MTH2=1.-THETA2
	sinio = math.sin(tle.inclination)
	a3ovk2 = -SatId.xj3/ck2 * SatId.ae**3
	c3 = coef * tsi * a3ovk2 * xnodp * SatId.ae * sinio/tle.eccentricity
	x1mth2 = 1.0 - theta2
	
	
#C4=2.*XNODP*COEF1*AODP*BETAO2*(ETA*
#1 (2.+.5*ETASQ)+EO*(.5+2.*ETASQ)-2.*CK2*TSI/
#2 (AODP*PSISQ)*(-3.*X3THM1*(1.-2.*EETA+ETASQ*
#3 (1.5-.5*EETA))+.75*X1MTH2*(2.*ETASQ-EETA*
#4 (1.+ETASQ))*COS(2.*OMEGAO)))
	c4 = 2.0 * xnodp * coef1 * aodp * beta_o2 * (eta *
					(2.0 + 0.5*etasq) + tle.eccentricity * (0.5 + 2.0 * etasq) -	2.0 * ck2 * tsi/ 
					(aodp * psisq) * (-3.0 * x3thm1 * (1.0 - 2.0 * eeta + etasq *
					(1.5 -.5 * eeta)) + 0.75 * x1mth2 * (2.0 * etasq - eeta *
					(1.0 + etasq)) * math.cos(2.0 * tle.perigee)))

#C5=2.*COEF1*AODP*BETAO2*(1.+2.75*(ETASQ+EETA)+EETA*ETASQ)
#THETA4=THETA2*THETA2
#TEMP1=3.*CK2*PINVSQ*XNODP
#TEMP2=TEMP1*CK2*PINVSQ
#TEMP3=1.25*CK4*PINVSQ*PINVSQ*XNODP
	c5 = 2.0 * coef1 * aodp * beta_o2 * (1.0 + 2.75 *(etasq + eeta) + eeta * etasq)
	theta4 = theta2 * theta2
	temp1 = 3.0 * ck2 * pinvsq * xnodp
	temp2 = temp1 * ck2 * pinvsq
	temp3 = 1.25 * SatId.ck4 * pinvsq * pinvsq * xnodp
	
#XMDOT=XNODP+.5*TEMP1*BETAO*X3THM1+.0625*TEMP2*BETAO*
#1 (13.-78.*THETA2+137.*THETA4)
	xmdot = xnodp + 0.5 * temp1 * beta_o * x3thm1 + 0.0625 * temp2 * beta_o	 * (13.0 - 78.0 * theta2 + 137.0 * theta4)

#X1M5TH=1.-5.*THETA2
#OMGDOT=-.5*TEMP1*X1M5TH+.0625*TEMP2*(7.-114.*THETA2+
#1 395.*THETA4)+TEMP3*(3.-36.*THETA2+49.*THETA4)
	x1m5th = 1.0 - 5.0 * theta2					
	omgdot = -0.5 * temp1 * x1m5th + 0.0625 * temp2 * (7.0 - 114.0 * theta2 + 
							395.0 * theta4) + temp3 * (3.0 - 36.0 * theta2 + 49.0 * theta4)

#XHDOT1=-TEMP1*COSIO
#XNODOT=XHDOT1+(.5*TEMP2*(4.-19.*THETA2)+2.*TEMP3*(3.-
#1 7.*THETA2))*COSIO
	xhdot1 = -temp1 * cosio
	xnodot = xhdot1 + (0.5 * temp2 * (4.0 - 19.0 * theta2) + 2.0 * temp3 * (3.0 -
							7.0 * theta2)) * cosio
							
#OMGCOF=BSTAR*C3*COS(OMEGAO)
#XMCOF=-TOTHRD*COEF*BSTAR*AE/EETA
#XNODCF=3.5*BETAO2*XHDOT1*C1
#T2COF=1.5*C1
#XLCOF=.125*A3OVK2*SINIO*(3.+5.*COSIO)/(1.+COSIO)
#AYCOF=.25*A3OVK2*SINIO
#DELMO=(1.+ETA*COS(XMO))**3
#SINMO=SIN(XMO)
#X7THM1=7.*THETA2-1.
	omgcof = tle.bStarDrag * c3 * math.cos(tle.perigee)
	xmcof = -twothirds * coef * tle.bStarDrag * SatId.ae/eeta
	xnodcf = 3.5 * beta_o2 * xhdot1 * c1
	t2cof = 1.5 * c1
	xlcof = 0.125 * a3ovk2 * sinio * (3.0 * 5.0 * cosio) / (1.0 + cosio)
	aycof = 0.25 * a3ovk2 * sinio
	delmo = (1.0 + eta * math.cos(tle.anomaly))
	sinmo = math.sin(tle.anomaly)
	x7thm1 = 7.0 * theta2 - 1.0
	
#IF(ISIMP .EQ. 1) GO TO 90
	if isimp != 1:
		#C1SQ=C1*C1
		#D2=4.*AODP*TSI*C1SQ
		#TEMP=D2*TSI*C1/3.
		#D3=(17.*AODP+S4)*TEMP
		#D4=.5*TEMP*AODP*TSI*(221.*AODP+31.*S4)*C1
		c1sq = c1 * c1
		d2 = 4.0 * aodp * tsi * c1sq
		temp = d2 * tsi * c1/3.0
		d3 = (17.0 * aodp + s4) * temp
		d4 = 0.5 * temp * aodp * tsi * (221.0 * aodp + 31.0 * s4) * c1
	
		#T3COF=D2+2.*C1SQ
		#T4COF=.25*(3.*D3+C1*(12.*D2+10.*C1SQ))
		#T5COF=.2*(3.*D4+12.*C1*D3+6.*D2*D2+15.*C1SQ*(
		#1 2.*D2+C1SQ))
		t3cof = d2 + 2.0 * c1sq
		t4cof = 0.25 * (3.0 * d3 + c1 * (12.0 * d2 + 10.0 * c1sq))
		t5cof = 0.2 * (3.0 * d4 + 12.0 * c1 * d3 + 6.0 * d2 * d2 + 15.0 * c1sq * (
							2.0 * d2 + c1sq))

#90 IFLAG=0
	iflag = 0

#
#* UPDATE FOR SECULAR GRAVITY AND ATMOSPHERIC DRAG
#

#100 XMDF=XMO+XMDOT*TSINCE
#OMGADF=OMEGAO+OMGDOT*TSINCE
#XNODDF=XNODEO+XNODOT*TSINCE
#OMEGA=OMGADF
#XMP=XMDF
#TSQ=TSINCE*TSINCE
#XNODE=XNODDF+XNODCF*TSQ
	xmdf = tle.anomaly + xmdot * tsince
	omgadf = tle.perigee + omgdot * tsince
	xnoddf = tle.ra + xnodot * tsince
	omega = omgadf
	xmp = xmdf
	tsq = tsince * tsince
	xnode = xnoddf + xnodcf * tsq
	
#TEMPA=1.-C1*TSINCE
#XNODE=XNODDF+XNODCF*TSQ
#TEMPL=T2COF*TSQ
	tempa = 1.0 - c1 * tsince
	tempe = tle.bStarDrag * c4 * tsince
	templ = t2cof * tsq
	
#IF(ISIMP .EQ. 1) GO TO 110
	if isimp != 1:
		#DELOMG=OMGCOF*TSINCE
		#TEMPL=T2COF*TSQ
		#TEMP=DELOMG+DELM
		#XMP=XMDF+TEMP
		#OMEGA=OMGADF-TEMP
		#TCUBE=TSQ*TSINCE
		#TFOUR=TSINCE*TCUBE
		#TEMPA=TEMPA-D2*TSQ-D3*TCUBE-D4*TFOUR
		#TEMPE=TEMPE+BSTAR*C5*(SIN(XMP)-SINMO)
		#TEMPL=TEMPL+T3COF*TCUBE+
		#1 TFOUR*(T4COF+TSINCE*T5COF)
		delomg = omgcof * tsince
		delm = xmcof * ((1.0 + eta * math.cos(xmdf)) **3 - delmo)
		temp = delomg + delm
		xmp = xmdf + temp
		omega = omgadf - temp
		tcube = tsq * tsince
		tfour = tsince * tcube
		tempa = tempa - d2 * tsq - d3 * tcube - d4 * tfour
		tempe = tempe + tle.bStarDrag * c5 * (math.sin(xmp) - sinmo)
		templ = templ + t3cof * tcube + tfour * (t4cof + tsince * t5cof)

#110 A=AODP*TEMPA**2
#E=EO-TEMPE
#XL=XMP+OMEGA+XNODE+XNODP*TEMPL
#BETA=SQRT(1.-E*E)
#XN=XKE/A**1.5
	a = aodp * tempa ** 2
	e = tle.eccentricity - tempe
	xl = xmp + omega + xnode + xnodp * templ
	beta = math.sqrt(1.0 - e * e)
	xn = SatId.xke / a ** 1.5
	

#* LONG PERIOD PERIODICS

#AXN=E*COS(OMEGA)
#TEMP=1./(A*BETA*BETA)
#XLL=TEMP*XLCOF*AXN
#AYNL=TEMP*AYCOF
#XLT=XL+XLL
#AYN=E*SIN(OMEGA)+AYNL
	axn = e * math.cos(omega)
	temp = 1.0/(a * beta * beta)
	xll = temp * xlcof * axn
	aynl = temp * aycof
	xlt = xl + xll
	ayn = e * math.sin(omega) + aynl

#
#* SOLVE KEPLERS EQUATION
#

#CAPU=FMOD2P(XLT-XNODE)
#TEMP2=CAPU
	capu = (xlt - xnode)%(SatId.twopi) #fmod2p(xlt - xnode)%(SatId.twopi)
	temp2 = capu
#DO 130 I=1,10
	for loopcounter in range(1, 11):
		#SINEPW=SIN(TEMP2)
		#COSEPW=COS(TEMP2)
		sinepw = math.sin(temp2)
		cosepw = math.cos(temp2)
		#TEMP3=AXN*SINEPW
		#TEMP4=AYN*COSEPW
		#TEMP5=AXN*COSEPW
		#TEMP6=AYN*SINEPW
		temp3 = axn * sinepw
		temp4 = ayn * cosepw
		temp5 = axn * cosepw
		temp6 = ayn * sinepw
		#EPW=(CAPU-TEMP4+TEMP3-TEMP2)/(1.-TEMP5-TEMP6)+TEMP2
		epw = (capu - temp4 + temp3 - temp2) / (1.0 - temp5 - temp6) + temp2
		#IF(ABS(EPW-TEMP2) .LE. E6A) GO TO 140
		#130 TEMP2=EPW
		if abs(epw - temp2) <= SatId.e6a:
			break
		temp2 = epw

#
#* SHORT PERIOD PRELIMINARY QUANTITIES
#

#140 ECOSE=TEMP5+TEMP6
#ESINE=TEMP3-TEMP4
#ELSQ=AXN*AXN+AYN*AYN
#TEMP=1.-ELSQ
#PL=A*TEMP
#R=A*(1.-ECOSE)
#TEMP1=1./R
#RDOT=XKE*SQRT(A)*ESINE*TEMP1
#RFDOT=XKE*SQRT(PL)*TEMP1
	ecose = temp5 + temp6
	esine = temp3 - temp4
	elsq = axn * axn + ayn * ayn
	temp = 1.0 - elsq
	pl = a * temp
	r = a * (1.0 - ecose)
	temp1 = 1.0/r
	rdot = SatId.xke * math.sqrt(a) * esine * temp1
	rfdot = SatId.xke * math.sqrt(pl) * temp1
	
#TEMP2=A*TEMP1
#BETAL=SQRT(TEMP)
#TEMP3=1./(1.+BETAL)
#COSU=TEMP2*(COSEPW-AXN+AYN*ESINE*TEMP3)
#SINU=TEMP2*(SINEPW-AYN-AXN*ESINE*TEMP3)
#U=ACTAN(SINU,COSU)
#SIN2U=2.*SINU*COSU
#COS2U=2.*COSU*COSU-1.
#TEMP=1./PL
#TEMP1=CK2*TEMP
#TEMP2=TEMP1*TEMP
	temp2 = a * temp1
	betal = math.sqrt(temp)
	temp3 = 1.0 / (1.0 + betal)
	cosu = temp2 * (cosepw - axn + ayn * esine * temp3)
	sinu = temp2 * (sinepw - ayn - axn * esine * temp3)
	u = math.atan2(sinu, cosu)
	sin2u = 2.0 * sinu * cosu
	cos2u = 2.0 * cosu * cosu - 1.0
	temp = 1.0/pl
	temp1 = ck2 * temp
	temp2 = temp1 * temp
	
#
#* UPDATE FOR SHORT PERIODICS
#

#RK=R*(1.-1.5*TEMP2*BETAL*X3THM1)+.5*TEMP1*X1MTH2*COS2U
#UK=U-.25*TEMP2*X7THM1*SIN2U
#XNODEK=XNODE+1.5*TEMP2*COSIO*SIN2U
#XINCK=XINCL+1.5*TEMP2*COSIO*SINIO*COS2U
#RDOTK=RDOT-XN*TEMP1*X1MTH2*SIN2U
#RFDOTK=RFDOT+XN*TEMP1*(X1MTH2*COS2U+1.5*X3THM1)
	rk = r * (1.0 - 1.5 * temp2 * betal * x3thm1) + 0.5 *temp1 * x1mth2 * cos2u
	uk = u - 0.25 * temp2 * x7thm1 * sin2u
	xnodek = xnode + 1.5 * temp2 * cosio * sin2u
	xinck = tle.inclination + 1.5 * temp2 * cosio * sinio * cos2u
	rdotk = rdot - xn * temp1 * x1mth2 * sin2u
	rfdotk = rfdot + xn * temp1 * (x1mth2 * cos2u + 1.5 * x3thm1)
	
#
#* ORIENTATION VECTORS
#

#SINUK=SIN(UK)
#COSUK=COS(UK)
#SINIK=SIN(XINCK)
#COSIK=COS(XINCK)
#SINNOK=SIN(XNODEK)
#COSNOK=COS(XNODEK)
	sinuk = math.sin(uk)
	cosuk = math.cos(uk)
	sinik = math.sin(xinck)
	cosik = math.cos(xinck)
	sinnok = math.sin(xnodek)
	cosnok = math.cos(xnodek)

#XMX=-SINNOK*COSIK
#XMY=COSNOK*COSIK
#UX=XMX*SINUK+COSNOK*COSUK
#UY=XMY*SINUK+SINNOK*COSUK
#UZ=SINIK*SINUK
#VX=XMX*COSUK-COSNOK*SINUK
#VY=XMY*COSUK-SINNOK*SINUK
#VZ=SINIK*COSUK
	xmx = -sinnok * cosik
	xmy = cosnok * cosik
	ux = xmx * sinuk + cosnok * cosuk
	uy = xmy * sinuk + sinnok * cosuk
	uz = sinik * sinuk
	vx = xmx * cosuk - cosnok * sinuk
	vy = xmy * cosuk - sinnok * sinuk
	vz = sinik * cosuk

#
#* POSITION AND VELOCITY
#

#X=RK*UX
#Y=RK*UY
#Z=RK*UZ
#XDOT=RDOTK*UX+RFDOTK*VX
#YDOT=RDOTK*UY+RFDOTK*VY
#ZDOT=RDOTK*UZ+RFDOTK*VZ
	x = rk * ux
	y = rk * uy
	z = rk * uz
	xdot = rdotk * ux + rfdotk * vx
	ydot = rdotk * uy + rfdotk * vy
	zdot = rdotk * uz + rfdotk * vz
	
#
# Original code did this outside of the SGP functions.
#X=X*XKMPER/AE 
#Y=Y*XKMPER/AE 
#Z=Z*XKMPER/AE 
#XDOT=XDOT*XKMPER/AE*XMNPDA/86400. 
#YDOT=YDOT*XKMPER/AE*XMNPDA/86400. 
#ZDOT=ZDOT*XKMPER/AE*XMNPDA/86400. 
	x *= SatId.xkmper/SatId.ae
	y *= SatId.xkmper/SatId.ae
	z *= SatId.xkmper/SatId.ae
	xdot *= SatId.xkmper/SatId.ae * SatId.minutes_per_day /86400.0
	ydot *= SatId.xkmper/SatId.ae * SatId.minutes_per_day /86400.0
	zdot *= SatId.xkmper/SatId.ae * SatId.minutes_per_day /86400.0
	
	return (x, y, z)	
#RETURN
#END

def actan(s,c):
	"""From the Space Track pdf: The function subroutine ACTAN is passed the values of sine and cosine in that order and 
it returns the angle in radians within the range of 0 to 2pi."""
	output = 0
	if c < 0:
		temp = s/c
		output = output + math.atan(temp)
		return output
	
	return output

#FUNCTION ACTAN(SINX,COSX) 
#COMMON/C2/DE2RA,PI,PIO2,TWOPI,X3PIO2 
#ACTAN=0. 
#IF (COSX.EQ.0. ) GO TO 5 
#IF (COSX.GT.0. ) GO TO 1 
#ACTAN=PI 
#GO TO 7 
#1 IF (SINX.EQ.0. ) GO TO 8 
#IF (SINX.GT.0. ) GO TO 7 
#ACTAN=TWOPI 
#GO TO 7 
#5 IF (SINX.EQ.0. ) GO TO 8 
#IF (SINX.GT.0. ) GO TO 6 
#ACTAN=X3PIO2 
#GO TO 8 
#6 ACTAN=PIO2 
#GO TO 8 
#7 TEMP=SINX/COSX 
#ACTAN=ACTAN+ATAN(TEMP) 
#8 RETURN 

def fmod2p(x):
	""" This is a function to take in an angle in radians and return
	the angle in the range of 0 to 2*pi """
	if x <= SatId.twopi:
		return x
	output = x%(SatId.twopi)
#	if output < 0.09: # If the angle is really small?
#		output = SatId.twopi - output
	return output

