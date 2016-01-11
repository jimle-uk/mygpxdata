# -*- coding: utf-8 -*-
from .xmlquery import XMLQuery

class Parser(object):
	def __init__(self):
		self._data = {}
		pass

	def load(self, filename):
		pass

	def run(self):
		pass

	def parse(self, filename):
		self.load(filename)
		self.run()

class XMLParser(Parser):
	def __init__(self):
		super(XMLParser, self).__init__()
		self._xmlQuery = XMLQuery()

	def load(self, filename):
		self._xmlQuery.open(filename)

	def run(self):
		self._data = self._xmlQuery.toDict()

	def getTrackSegments(self):
		return self._data['trk']['trkseg']