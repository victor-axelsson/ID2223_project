class TrackChunk:
	chunkId = None
	chunkSize = None
	events = None

	def __init__(self, chunkId, chunkSize, events):
		self.chunkId = chunkId
		self.chunkSize = chunkSize
		self.events = events

	def printIt(self):
		print("chunkId =>" + str(self.chunkId))
		print("chunkSize =>" + str(self.chunkSize))
		print("events => " + str(self.events))

