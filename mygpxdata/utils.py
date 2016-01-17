# -*- coding: utf-8 -*-
import math
# ==============================================================================
# math
# ==============================================================================

pi = math.pi
glOffset = math.pow(2, 28)
glRadius = glOffset / pi

def lonToX(lon):
	return round(glOffset + glRadius * lon * pi);

def latToY(lat):
	return round(glOffset - glRadius * math.log((1 + math.sin(lat * pi)) / (1 - math.sin(lat * pi))) / 2);

def calculateBounds(coordinates):
	"""
	caculates the upper and lower bounds of the coordinate set
	"""
	x_values = [coordinate[0] for coordinate in coordinates]
	y_values = [coordinate[1] for coordinate in coordinates]
	max_x, min_x = max(x_values), min(x_values)
	max_y, min_y = max(y_values), min(y_values)
	
	return min_x, max_x, min_y, max_y

def calculateScale(w, h, min_x, max_x, min_y, max_y):
	"""
	returns scale factor between route bounds (dx,dy) and the canvas
	"""
	dx = max_x - min_x
	dy = max_y - min_y

	scale = dy if dx < dy else dx

	scale_x = float(w)/scale
	scale_y = float(h)/scale
	
	return scale_x, scale_y

def calculateOffset(w, h, min_x, max_x, min_y, max_y):
	"""
	calculates offset of the svg path to position it center within the regions
	of canvas.
	"""
	offset_x = (w/2) - ((max_x - min_x)/2)
	offset_y = 0 - (h/2) - ((max_y - min_y)/2)
	
	return (offset_x, offset_y)

def calculateAngle(p1, p2):
	"""
	calculates angle between p1 and p2. Returns angle in degrees.
	"""
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]
	rads = math.atan2(dy, dx)
	degs = math.degrees(rads)
	return degs

# ==============================================================================
# track
# ==============================================================================
def flatten(l):
	return [i for n in l for i in n]

def trackSegmentsToCoordinates(segments):
	coordinates = []
	for seg in segments:
		coordinates.append([(lonToX(float(trkpt.get('lon'))), latToY(float(trkpt.get('lat')))) for trkpt in seg])
	return coordinates

def transformCoordinates(coordinates, min_x, min_y, scale_x, scale_y):
	"""
	Manipulates coordinates to ensure they display within
	the bounds of canvas
	"""
	transformed_coordinates = []
	for seg in coordinates:
		transformed_coordinates.append([((trkpt[0]-min_x)*scale_x,(trkpt[1]-min_y)*scale_y) for trkpt in seg])
	return transformed_coordinates

def filterCoordinatesByAngle(coordinates, degrees=0):
	"""
	filters out coordinates based on difference in angle between coordinate (C)
	and previous coordinate (B) and previous coordinate (B) and previous-previous
	coordinate (A).
	eg:
	[
		(1,1), # coordinate (A)
		(2,2), # coordinate (B)
		(3,3), # coordinate (C)
	]
	primary use case is to exclude coordinates which do not diverge much from
	previous coordinate if terms of direction. We assume if they're not 
	diverging much, then it is safe to assume direction is a relatively straight line.
	We can then omit the coordinate and reduce the number of coordinates to
	render giving us a much smoother route.
	ie. if -degrees < CB - BA > +degrees then include else omit

	"""
	retVal = []
	A = None
	B = None
	for coordinate in coordinates:
		C = coordinate
		angle_1 = calculateAngle(A, B) if A and B else 0
		angle_2 = calculateAngle(B, C) if B else 0

		A,B = (B,C) if B else (A,C)

		if abs(angle_2 - angle_1) >= degrees:
			retVal.append(coordinate)

	return retVal