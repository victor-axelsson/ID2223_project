class WTFIsThisEvent:

	dataBuffer = None
	stringLength = None
	
	def __init__(self, dataBuffer, length=-1):
		self.dataBuffer = dataBuffer
		if length == -1:
			self.stringLength = int.from_bytes(dataBuffer[1], byteorder='big')
		else:
			self.stringLength = length

	def getOffset(self):
		return self.stringLength

	def getClassName(self):
		return "WTFIsThisEvent"