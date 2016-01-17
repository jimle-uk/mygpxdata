# -*- coding: utf-8 -*-
import os.path
import re
import xml.etree.ElementTree as etree

class XMLNode:
	"""
	Wraps around a XML node and gives it super powers.
	"""
	def __init__(self, node=None):
		self._node = node
		self._xmlns, self._nodeName = self.getNodeTag()

	def getNodeTag(self):
		node_tag = re.search(r"\{(.+)\}(.+)", self._node.tag)
		return node_tag.group(1), node_tag.group(2)

	def xmlns(self, name):
		return "{%s}%s" % (self._xmlns, name)

	def querySelector(self, name):
		node = self._node.find(self.xmlns(name)) if self._node != None else None
		return XMLNode(node)

	def querySelectorAll(self, name):
		nodes = self._node.findall(self.xmlns(name)) if self._node != None else None
		return [XMLNode(node) for node in nodes] if nodes else []

	def children(self):
		return [XMLNode(child) for child in self._node._children] if self._node != None else []

	def attr(self, name=None, default=None):
		if self._node != None:
			return self._node.attrib.get(name, default) if name != None else self._node.attrib
		else:
			return default

	def text(self):
		return self._node.text if self._node != None else ""

	def toDict(self):
		"""
		recursive function that converts xml tree to dict
		"""
		retVal = {}
		if self._node != None:

			text = self.text()
			attrs = self.attr()
			childNodes = self.children()
			
			childValues = {}

			for child in childNodes:
				child_dict = child.toDict()
				if len(child_dict.values()) == 1:
					child_dict = child_dict.values()[0]
				if not child._nodeName in childValues:
					childValues[child._nodeName] = []
				childValues[child._nodeName].append(child_dict)

			# if childValue[x] is a single element array, then just return
			# the childValue[0]
			for k, v in childValues.iteritems():
				if len(v) == 1:
					retVal[k] = v[0]
				else:
					retVal[k] = v

			if text != None and text.strip():
				retVal["text"] = text.strip()

			retVal.update(attrs)

		return retVal

	def __repr__(self):
		return repr(self._node)

	def __len__(self):
		return len(self._node)


class XMLQuery(XMLNode):
	"""
	like XMLNode but with ability to open xml files from disk
	"""
	def __init__(self, tree=None, **kwargs):
		if "filename" in kwargs:
			self.filename = kwargs.get("filename")

		self.setup(tree)

	def open(self, filename):
		"""
		load external XML file and parse using xml.etree.ElementTree.parse
		"""
		if not filename:
			if hasattr(self, "filename"):
				filename = self.filename
			else:
				raise ValueError("No filename given.")

		if not os.path.isfile(filename):
			raise IOError("file not found. Tried \"%s\"" % filename)

		try:
			tree = etree.parse(filename)
			self.setup(tree)
			return True
		except Exception as e:
			raise e

	def setup(self, tree):
		"""
		initialising variables for XMLNode functionality
		"""
		if tree:
			self._tree = tree
			self._node = self._tree.getroot()
			self._xmlns, self._nodeName = self.getNodeTag()
		return self