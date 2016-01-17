myGpxData
=========
```myGPXData``` was the result of a weekend exercise extracting running data 
(as in exercise/fitness) from my fitness tracking app and learning how it works.

The goal of this package is to take a gpx file and:

1. draw/trace its track points to a graphic; saving to disk or returning as a string.
2. extract popular stats (for running); distance, duration, splits, pace and climb.

#### Current project status
As of 2016-01-17, extracting stats have been added.

~~As of 2016-01-01, myGPXData is alpha version and only renders gpx to svg. Does not current
extract stats.~~

Note: This package does not render the gpx route on top of a map (ie. openstreetmaps, google maps).
Only the route is rendered.

#### Installation requirements and dependencies

- python 2.7
- svgwrite 1.1.6

#### License

BSD. See ```LICENSE```

#### How to use

```python
from myGPXData import myGPXData

gpx = myGPXData()
gpx.open("/path/to/file.gpx")

# output width and height is required
width = 320
height = 240

output = gpx.renderToString(size=(width, height))
# output = "<?xml version="1.0" encoding="utf-8" ?>..." etc

gpx.renderToFile("/path/to/file.svg", size=(width, height))


print "total distance: ", gpxdata.getTotalDistance() 
# returns total is in meters eg. "4489.14574646"

print "total duration: ", divmod(gpxdata.getTotalDuration(), 60)
# returns total in seconds. Divmod for minutes eg. "(47, 3)" means 47mins 30secs

print "total climb: ", gpxdata.getTotalClimb()
# returns total climb in meters eg. "50.3" 

print "splits", gpxdata.getSplits()
# returns array of tuples of (distance(mtrs), duration(secs), climb(mtrs), pace(secs)) per ~1km (default) of total distance. eg. [(1004.1364255006434, 483, 7.299999999999994, 481.0103365777068), ... ]

print "average pace", divmod(gpxdata.getAveragePace(), 60)
# returns average pace per km in seconds. Divmod for minutes. eg. "(9.0, 17)" means 9mins 17secs
```

#### Todo

1. ~~Finish adding gpx stats; distance, duration, splits, pace and climb~~
2. Try out different renderers ie. data-url, canvas
3. Documentation, tests etc
