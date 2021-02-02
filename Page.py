class Page(object):
	__slots__ = ["tree", "keys", "children"]

	def __init__(self, tree, keys=None, children=None): # Construtor
		self.tree = tree
		self.keys = keys or []
		self.children = children or []

	def __repr__(self): # Formatar String para o Print
		return "[%s]" % (", ".join(map(str, self.keys)))

	def lateral(self, parent, parent_index, dest, dest_index): # Chaves na mesma Página
		if parent_index > dest_index:
			dest.keys.append(parent.keys[dest_index])
			parent.keys[dest_index] = self.keys.pop(0)
			if self.children:
				dest.children.append(self.children.pop(0))
		else:
			dest.keys.insert(0, parent.keys[parent_index])
			parent.keys[parent_index] = self.keys.pop()
			if self.children:
				dest.children.insert(0, self.children.pop())

	def shrink(self, ancestors): # Diminuir Árvore
		parent = None

		if ancestors:
			parent, parent_index = ancestors.pop()
			if parent_index:
				left_sib = parent.children[parent_index - 1]
				if len(left_sib.keys) < self.tree.order:
					self.lateral(
						parent, parent_index, left_sib, parent_index - 1)
					return

			if parent_index + 1 < len(parent.children):
				right_sib = parent.children[parent_index + 1]
				if len(right_sib.keys) < self.tree.order:
					self.lateral(
						parent, parent_index, right_sib, parent_index + 1)
					return

		center = len(self.keys) // 2
		sibling, push = self.split()

		if not parent:
			parent, parent_index = Page(
				self.tree, children=[self]), 0
			self.tree._root = parent

		parent.keys.insert(parent_index, push)
		parent.children.insert(parent_index + 1, sibling)
		if len(parent.keys) > parent.tree.order:
			parent.shrink(ancestors)

	def grow(self, ancestors): # Aumentar Árvore
		parent, parent_index = ancestors.pop()

		minimum = self.tree.order // 2
		left_sib = right_sib = None

		if parent_index + 1 < len(parent.children):
			right_sib = parent.children[parent_index + 1]
			if len(right_sib.keys) > minimum:
				right_sib.lateral(parent, parent_index + 1, self, parent_index)
				return

		if parent_index:
			left_sib = parent.children[parent_index - 1]
			if len(left_sib.keys) > minimum:
				left_sib.lateral(parent, parent_index - 1, self, parent_index)
				return

		if left_sib:
			left_sib.keys.append(parent.keys[parent_index - 1])
			left_sib.keys.extend(self.keys)
			if self.children:
				left_sib.children.extend(self.children)
			parent.keys.pop(parent_index - 1)
			parent.children.pop(parent_index)
		else:
			self.keys.append(parent.keys[parent_index])
			self.keys.extend(right_sib.keys)
			if self.children:
				self.children.extend(right_sib.children)
			parent.keys.pop(parent_index)
			parent.children.pop(parent_index + 1)

		if len(parent.keys) < minimum:
			if ancestors:
				parent.grow(ancestors)
			elif not parent.keys:
				self.tree._root = left_sib or self

	def split(self): # Dividir Página
		center = len(self.keys) // 2
		median = self.keys[center]
		sibling = type(self)(
			self.tree,
			self.keys[center + 1:],
			self.children[center + 1:])
		self.keys = self.keys[:center]
		self.children = self.children[:center + 1]
		return sibling, median

	def insert(self, index, item, ancestors): # Inserir Chaves na Página
		self.keys.insert(index, item)
		if len(self.keys) > self.tree.order:
			self.shrink(ancestors)

	def remove(self, index, ancestors): # Remover Chaves da Página
		minimum = self.tree.order // 2

		if self.children:
			additional_ancestors = [(self, index + 1)]
			descendent = self.children[index + 1]
			while descendent.children:
				additional_ancestors.append((descendent, 0))
				descendent = descendent.children[0]
			if len(descendent.keys) > minimum:
				ancestors.extend(additional_ancestors)
				self.keys[index] = descendent.keys[0]
				descendent.remove(0, ancestors)
				return

			additional_ancestors = [(self, index)]
			descendent = self.children[index]
			while descendent.children:
				additional_ancestors.append(
					(descendent, len(descendent.children) - 1))
				descendent = descendent.children[-1]
			ancestors.extend(additional_ancestors)
			self.keys[index] = descendent.keys[-1]
			descendent.remove(len(descendent.children) - 1, ancestors)
		else:
			self.keys.pop(index)
			if len(self.keys) < minimum and ancestors:
				self.grow(ancestors)