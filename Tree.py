import bisect
from Page import Page

class BTree(object):

	def __init__(self, order):
		self.order = order
		self._root = self._bottom = Page(self)

	def _path_to(self, item):
		"""

	    """
		current = self._root
		ancestry = []

		while getattr(current, "children", None):
			index = bisect.bisect_left(current.keys, item)
			ancestry.append((current, index))
			if index < len(current.keys) \
				and current.keys[index] == item:
				return ancestry
			current = current.children[index]

		index = bisect.bisect_left(current.keys, item)
		ancestry.append((current, index))
		present = index < len(current.keys)
		present = present and current.keys[index] == item
		return ancestry

	def present(self, item, ancestors):
		last, index = ancestors[-1]
		return index < len(last.keys) and last.keys[index] == item

	def insert(self, item):
		current = self._root
		ancestors = self._path_to(item)
		node, index = ancestors[-1]
		while getattr(node, "children", None):
			node = node.children[index]
			index = bisect.bisect_left(node.keys, item)
			ancestors.append((node, index))
		node, index = ancestors.pop()
		node.insert(index, item, ancestors)

	def remove(self, item):
		current = self._root
		ancestors = self._path_to(item)

		if self.present(item, ancestors):
			node, index = ancestors.pop()
			node.remove(index, ancestors)
		else:
			raise ValueError("%r not in %s" % (item, self.__class__.__name__))

	def contains(self, item):
		return self.present(item, self._path_to(item))

	def __iter__(self):
		def _recurse(node):
			if node.children:
				for child, item in zip(node.children, node.keys):
					for child_item in _recurse(child):
						yield child_item
					yield item
				for child_item in _recurse(node.children[-1]):
					yield child_item
			else:
				for item in node.keys:
					yield item

		for item in _recurse(self._root):
			yield item

	def __repr__(self):
		def recurse(node, accum, depth):
			accum.append(("  " * depth) + repr(node))
			for node in getattr(node, "children", []):
				recurse(node, accum, depth + 1)

		accum = []
		recurse(self._root, accum, 0)
		return "\n".join(accum)