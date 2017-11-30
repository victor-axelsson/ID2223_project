class TrackChunk:
	chunkId = None
	chunkSize = None
	trackEventData = None

	def __init__(self, chunkId, chunkSize, trackEventData):
		self.chunkId = chunkId
		self.chunkSize = chunkSize
		self.trackEventData = trackEventData

	def printIt(self):
		print("chunkId =>" + str(self.chunkId))
		print("chunkSize =>" + str(self.chunkSize))
		print("trackEventData =>" + str(self.trackEventData))