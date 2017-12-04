class CopyrightNotice: 
	dataBuffer = None
	stringLength = None

	def __init__(self, dataBuffer):
		self.dataBuffer = dataBuffer
		self.stringLength = int.from_bytes(dataBuffer[1], byteorder='big')

	def getOffset(self):
		return self.stringLength

	def getClassName(self):
		return "CopyrightNotice"