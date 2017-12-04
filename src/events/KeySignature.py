class KeySignature:

	dataBuffer = None
	def __init__(self, dataBuffer):
		self.dataBuffer = dataBuffer

	def getOffset(self):
		return 2

	def getClassName(self):
		return "KeySignature"