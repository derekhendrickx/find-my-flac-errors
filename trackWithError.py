import unicodedata

class TrackWithError:
	def __init__(self, name, path):
		self.normalizedName = TrackWithError.normalizeName(name)
		self.name = name
		self.path = path
		self.count = 1

	def addCount(self):
		self.count += 1

	def __eq__(self, other):
		print('test')
		return isinstance(other, TrackWithError) and self.normalizedName == other.normalizedName

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.normalizedName)
	
	@staticmethod
	def normalizeName(name):
		return unicodedata.normalize('NFKD', name).encode('ascii','ignore').decode('utf-8')