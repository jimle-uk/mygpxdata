import unittest
import math

class TestUtils(unittest.TestCase):

	def setUp(self):
		self.lonlat = [
			( "-0.137579000", "51.419945000" ),
			( "-0.137578000", "51.419945000" ),
			( "-0.137979000", "51.420126000" ),
			( "-0.138086000", "51.420218000" ),
			( "-0.138302000", "51.420234000" ),
			( "-0.138433000", "51.420290000" ),
			( "-0.138589000", "51.420313000" ),
			( "-0.138712000", "51.420373000" ),
			( "-0.138751000", "51.420468000" )]

		self.trkseg = [[{ "lon": "-0.137579000", "lat": "51.419945000" }]]

	def test_pi(self):
		self.assertEqual(utils.pi, math.pi)

	def test_glOffset(self):
		self.assertEqual(utils.glOffset, math.pow(2, 28))

	def test_glRadius(self):
		self.assertEqual(utils.glRadius, math.pow(2, 28) / math.pi)

	def test_lonToX(self):
		x = [utils.lonToX(float(x[0])) for x in self.lonlat]
		expected_results = [231504374.0, 231504643.0, 231397000.0, 231368278.0, 231310296.0, 231275131.0, 231233255.0, 231200237.0, 231189768.0]
		self.assertEqual(x, expected_results)

	def test_latToY(self):
		y = [utils.lonToX(float(x[1])) for x in self.lonlat]
		expected_results = [14071371840.0, 14071371840.0, 14071420426.0, 14071445122.0, 14071449417.0, 14071464450.0, 14071470624.0, 14071486730.0, 14071512231.0]
		self.assertEqual(y, expected_results)

	def test_calculateBounds(self):
		expected_results = ('-0.137578000', '-0.138751000', '51.419945000', '51.420468000')
		self.assertEqual(utils.calculateBounds(self.lonlat), expected_results)

	def test_calculateScale(self):
		test_a = {"w":100, "h":100, "min_x":1, "max_x":10, "min_y":1, "max_y":10}
		expected_a = (11.11111111111111, 11.11111111111111)
		test_b = {"w":200, "h":100, "min_x":1, "max_x":10, "min_y":1, "max_y":10}
		expected_b = (22.22222222222222, 11.11111111111111)
		test_c = {"w":100, "h":200, "min_x":1, "max_x":10, "min_y":1, "max_y":10}
		expected_c = (11.11111111111111, 22.22222222222222)
		test_d = {"w":-100, "h":-100, "min_x":-1, "max_x":-10, "min_y":-1, "max_y":-10}

		self.assertEqual(utils.calculateScale(**test_a), expected_a)
		self.assertEqual(utils.calculateScale(**test_b), expected_b)
		self.assertEqual(utils.calculateScale(**test_c), expected_c)
		self.assertEqual(utils.calculateScale(**test_d), expected_a)

	def test_calculateOffset(self):
		test_a = {"w":100, "h":100, "min_x":1, "max_x":10, "min_y":1, "max_y":10}
		expected_a = (46, -54)
		test_b = {"w":200, "h":100, "min_x":1, "max_x":10, "min_y":1, "max_y":10}
		expected_b = (96, -54)
		test_c = {"w":100, "h":200, "min_x":1, "max_x":10, "min_y":1, "max_y":10}
		expected_c = (46, -104)
		test_d = {"w":-100, "h":-100, "min_x":-1, "max_x":-10, "min_y":-1, "max_y":-10}
		expected_d = (-45, 55)
		
		self.assertEqual(utils.calculateOffset(**test_a), expected_a)
		self.assertEqual(utils.calculateOffset(**test_b), expected_b)
		self.assertEqual(utils.calculateOffset(**test_c), expected_c)
		self.assertEqual(utils.calculateOffset(**test_d), expected_d)

	def test_calculateAngle(self):
		self.assertEquals(utils.calculateAngle((0,0), (1,1)), 45.0) # north east
		self.assertEquals(utils.calculateAngle((0,0), (0,1)), 90) # north
		self.assertEquals(utils.calculateAngle((0,0), (-1,1)), 135.0) # north west
		self.assertEquals(utils.calculateAngle((0,0), (-1,0)), 180.0) # west
		self.assertEquals(utils.calculateAngle((0,0), (-1,-1)), -135) # south west
		self.assertEquals(utils.calculateAngle((0,0), (0,-1)), -90.0) # south
		self.assertEquals(utils.calculateAngle((0,0), (1,-1)), -45) # south east 
		self.assertEquals(utils.calculateAngle((0,0), (0,0)), 0) # east 

	def test_concatCoordinateGroups(self):
		test_a = [[1,2,3]]
		expected_a = [1,2,3]
		test_b = [[1,2,3], [4,5,6]]
		expected_b = [1,2,3,4,5,6]
		test_c = [[1,2,3],[4,5,6],[7],[8,9]]
		expected_c = [1,2,3,4,5,6,7,8,9]

		self.assertEquals(utils.concatCoordinateGroups(test_a), expected_a)
		self.assertEquals(utils.concatCoordinateGroups(test_b), expected_b)
		self.assertEquals(utils.concatCoordinateGroups(test_c), expected_c)

	def test_trackSegmentsToCoordinates(self):
		self.assertEquals(utils.trackSegmentsToCoordinates(self.trkseg), [[(231504374.0, 445151444.0)]])

	def test_transformCoordinates(self):
		coordinates = utils.trackSegmentsToCoordinates(self.trkseg)
		test_a = {"coordinates": coordinates, "min_x": coordinates[0][0][0], "min_y": coordinates[0][0][1], "scale_x": 1, "scale_y": 1}
		expected_a = [[(0.0, 0.0)]]
		test_b = {"coordinates": coordinates, "min_x": 0, "min_y": 0, "scale_x": 200, "scale_y": 200}
		expected_b = [[(46300874800.0, 89030288800.0)]]

		self.assertEquals(utils.transformCoordinates(**test_a), expected_a)
		self.assertEquals(utils.transformCoordinates(**test_b), expected_b)

	def test_filterCoordinatesByAngle(self):
		coordinates = [
			(0,0), # 0
			(1,1), # 45.0
			(1,1.4), # 45.0
			(-1,-1), # -219.8
			(-1.2,-1), # 309.8
			(-1,-1) # -180
		]

		self.assertEquals(len(utils.filterCoordinatesByAngle(coordinates, degrees=45)), 5)
		self.assertEquals(len(utils.filterCoordinatesByAngle(coordinates, degrees=180)), 3)
		self.assertEquals(len(utils.filterCoordinatesByAngle(coordinates, degrees=200)), 2)
		self.assertEquals(len(utils.filterCoordinatesByAngle(coordinates, degrees=300)), 1)


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		import utils
	unittest.main()
