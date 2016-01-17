# -*- coding: utf-8 -*-
from .utils import flatten, convertTimestamp
import math


# ==============================================================================
# time
# ==============================================================================
def calculateDuration(dt):
	"""returns number of seconds between two datetime objects"""
	duration = dt[-1] - dt[0]
	return duration.seconds

def getTimestamps(trackSegments):
	"""returns array of all timestamps as datetime objects from trackSegments"""
	timestamps = []
	for seg in trackSegments:
		timestamps.append([convertTimestamp(item.get("time")) for item in seg])
	return timestamps

def calculateTotalDuration(trackSegments):
	"""returns seconds of total duration from trackSegments"""
	timestamps = getTimestamps(trackSegments)
	return sum([calculateDuration(leg) for leg in timestamps])

# ==============================================================================
# distance
# ==============================================================================
def calculateDistance(p1, p2):
	"""
	returns metres between two cooridates (lon,lat), (lon,lat) using 
	havesine formula returns distance in metres
	credit: http://www.movable-type.co.uk/scripts/latlong.html
	"""
	R = 6371000 # metres
	latitude_1 = math.radians(p1[1])
	latitude_2 = math.radians(p2[1])
	delta_latitude = math.radians(p2[1]-p1[1])
	delta_longtitude = math.radians(p2[0]-p1[0])

	a = math.sin(delta_latitude/2) * math.sin(delta_latitude/2) + \
		math.cos(latitude_1) * math.cos(latitude_2) * math.sin(delta_longtitude/2) * \
		math.sin(delta_longtitude/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = R * c
	return d

def getDistances(trackSegments):
	"""returns array of distances between trkpts in metres"""
	distances = []

	for seg in trackSegments:
		total = []
		prev_item = None
		for item in seg:
			lat, lon = float(item.get('lat')), float(item.get('lon'))
			if prev_item:
				total.append(calculateDistance(prev_item, (lon, lat)))
			prev_item = (lon, lat)
		distances.append(total)
	return distances

def calculateTotalDistance(trackSegments):
	"""returns sum of total distance in metres from trackSegments"""
	return sum(flatten(getDistances(trackSegments)))


# ==============================================================================
# climb
# ==============================================================================
def getElevations(trackSegments):
	"""returns array of elevations in metres from trackSegments"""
	elevations = []
	for seg in trackSegments:
		elevations.append([float(item.get("ele")) for item in seg])
	return elevations

def calculateClimb(elevations):
	"""returns climb between elevations"""
	total = []
	previous_elevation = None
	for elevation in elevations:
		total.append(elevation - previous_elevation if previous_elevation and elevation - previous_elevation > 0 else 0)
		previous_elevation = elevation
	return total

def getClimbs(trackSegments):
	"""returns climb in meters"""
	return [calculateClimb(elevations) for elevations in getElevations(trackSegments)]

def calculateTotalClimb(trackSegments):
	"""returns total climb in meters from elevations from trackSegments"""
	return sum(flatten(getClimbs(trackSegments)))


# ==============================================================================
# splits
# ==============================================================================
def calculateSplits(trackSegments, split_distance=1000):
	"""returns array of tuples of (distance, duration, climb, pace) per split_distance chunk of trackSegments"""
	d = flatten(getDistances(trackSegments))
	t = flatten(getTimestamps(trackSegments))
	c = flatten(getClimbs(trackSegments))
	
	indexes = []
	d_total = 0
	for i in xrange(0, len(d)):
		if d_total >= split_distance:
			indexes.append(i)
			d_total = 0
		d_total += d[i]

	if indexes[-1] < len(d):
		indexes.append(len(d))

	chunks = [[x[slice(indexes[i-1] if i-1 > -1 else 0, indexes[i])] for i in xrange(0, len(indexes))] for x in [d, t, c]]
	splits = zip(*[[(sum(x) if i!=1 else calculateDuration(x)) for x in chunks[i]] for i in xrange(0, len(chunks))])

	pace = [calculatePace(split, split_distance) for split in splits]
	splits = [splits[i] + (pace[i],) for i in xrange(0, len(splits))]

	return splits

# ==============================================================================
# pace
# ==============================================================================
def calculatePace(split, units=1000):
	"""returns pace per kilometers"""
	distance, duration, climb = split
	return duration/(distance/units)

def calculateAveragePace(trackSegments):
	"""returns average pace per kilometers in seconds"""
	splits = calculateSplits(trackSegments)
	return sum([pace for distance, duration, climb, pace in splits])/len(splits)
