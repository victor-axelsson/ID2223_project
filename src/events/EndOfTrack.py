class EndOfTrack:

	dataBuffer = None
	def __init__(self, dataBuffer):
		self.dataBuffer = dataBuffer

	def getOffset(self):
		return 0

	def getClassName(self):
		return "EndOfTrack"