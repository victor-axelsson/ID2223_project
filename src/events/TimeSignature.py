class TimeSignature:

	dataBuffer = None
	def __init__(self, dataBuffer):
		print("Here")
		self.dataBuffer = dataBuffer

	def getOffset(self):
		return 4

	def getClassName(self):
		return "TimeSignature"