class TrackWithError:
	def __init__(self, name, path):
		self.name = name
		self.path = path
		self.count = 1

	def addCount(self):
		self.count += 1

	def __eq__(self, other):
		return isinstance(other, TrackWithError) and self.name == other.name

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.name)