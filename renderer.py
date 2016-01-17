import svgwrite
from .utils import ( concatCoordinateGroups, calculateBounds, calculateScale, 
	transformCoordinates ,calculateOffset , filterCoordinatesByAngle )

class Renderer(object):
	canvas_width = 0
	canvas_height = 0
	margin_left, margin_right, margin_top, margin_bottom = 10, 10, 10, 10

	def __init__(self, **kwargs):
		if "coordinates" in kwargs.keys():
			self._coordinates = kwargs.get("coordinates")
			self.computeValues()

	def render(self):
		pass

	def setSize(self, size):
		self.canvas_width, self.canvas_height = size

	def computeValues(self):
		all_coordinates = flatten(self._coordinates)

		self.min_x, self.max_x, self.min_y, self.max_y = calculateBounds(all_coordinates)
		self.scale_x, self.scale_y = calculateScale(self.canvas_width, self.canvas_height, self.min_x, self.max_x, self.min_y, self.max_y)
		
		self._transformed_cordinates = transformCoordinates(self._coordinates, self.min_x, self.min_y, self.scale_x, self.scale_y)
		self.t_min_x, self.t_max_x, self.t_min_y, self.t_max_y = calculateBounds(flatten(self._transformed_cordinates))

		self.offset_width = self.canvas_width + self.margin_left + self.margin_right
		self.offset_height = self.canvas_height + self.margin_top + self.margin_bottom
		self.offset = calculateOffset(self.offset_width, self.offset_height, self.t_min_x, self.t_max_x, self.t_min_y, self.t_max_y)

	def setCoordinates(self, coordinates):
		self._coordinates = coordinates
		self.computeValues()


class SVGRenderer(Renderer):

	path_attributes = {
		"stroke" : "#cccccc",
		"fill" : "none",
		"stroke_width" : 5,
		"stroke_opacity" : 0.5,
		"stroke_linejoin" : "round",
		"stroke_linecap" : "round"
	}
	path_resolution = 0.2

	def __init__(self, **kwargs):
		super(SVGRenderer, self).__init__(**kwargs)

	def render(self, **kwargs):
		dwg = svgwrite.Drawing(size=(self.offset_width, self.offset_height), **kwargs)
		for segment in self._transformed_cordinates:
			path = dwg.path(**self.path_attributes)
			path.push(self.generateSVGPathCommands(segment))
			# FIXME: not sure about hardcoding this flip...
			group = dwg.g(transform="scale(1,-1) translate(%s,%s)" % self.offset)
			group.add(path)
			dwg.add(group)
		return dwg

	def renderToString(self, **kwargs):
		dwg = self.render(**kwargs)
		return dwg.tostring()

	def renderToFile(self, filename, **kwargs):
		dwg = self.render(**kwargs)
		try:
			dwg.saveas(filename)
		except Exception as e:
			raise "Could not save file. %s %s" % (filename, e)

	def setPathAttributes(self, attributes):
		self.path_attributes.update(attributes)

	def setPathResolution(self, value):
		max_angle = 90.0
		self.path_resolution = float(max_angle/100) * (float((1-value)*100))

	def generateSVGPathCommands(self, coordinates):
		points = filterCoordinatesByAngle(coordinates, degrees=self.path_resolution)
		return ["M%s,%s" % points[0]] + ["L%s,%s" % pt for pt in points]
