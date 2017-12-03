class TrackChunk:
	chunkId = None
	chunkSize = None

	def __init__(self, chunkId, chunkSize):
		self.chunkId = chunkId
		self.chunkSize = chunkSize
		self._format()

	def _format(self):
		print("F")

	def printIt(self):
		print("chunkId =>" + str(self.chunkId))
		print("chunkSize =>" + str(self.chunkSize))
		#print(bin(int.from_bytes(self.trackEventData, byteorder="big")).strip('0b'))
		#print(bin(int.from_bytes(self.trackEventData, 	byteorder="little")).strip('0b'))
		#print("trackEventData =>" + str(self.trackEventData))
