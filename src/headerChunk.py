class HeaderChunk:

	chunkID = None
	chunkSize = None
	formatType = None
	numberOfTracks = None
	timeDivision = None

	def __init__(self, chunkID, chunkSize, formatType, numberOfTracks, timeDivision):
		self.chunkID = chunkID
		self.chunkSize = chunkSize
		self.formatType = formatType
		self.numberOfTracks = numberOfTracks
		self.timeDivision = timeDivision

	def printIt(self):
		print("chunkID =>" + str(self.chunkID))
		print("chunkSize =>" + str(self.chunkSize))
		print("formatType =>" + str(self.formatType))
		print("numberOfTracks =>" + str(self.numberOfTracks))
		print("timeDivision =>" + str(self.timeDivision))

	def parseToString(self):
		content = ""
		