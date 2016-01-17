# -*- coding: utf-8 -*-
from .parser import XMLParser
from .renderer import SVGRenderer
from .utils import trackSegmentsToCoordinates

class myGPXData:
	def __init__(self):
		self._parser = XMLParser()
		self._renderer = SVGRenderer()
		
	def open(self, filename):
		self._data = self._parser.parse(filename)

	def update(self, **kwargs):
		coordinates = utils.trackSegmentsToCoordinates(self.getTrackSegments())
		
		if "size" in kwargs:
			self._renderer.setSize(kwargs.get("size"))
		
		if "resolution" in kwargs:
			self._renderer.setPathResolution(kwargs.get("resolution"))

		self._renderer.setCoordinates(coordinates)

	def renderToString(self, **kwargs):
		self.update(**kwargs)
		return self._renderer.renderToString()

	def renderToFile(self, filename, **kwargs):
		self.update(**kwargs)
		return self._renderer.renderToFile(filename)