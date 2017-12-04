class SequenceTrackName:

	dataBuffer = None
	stringLength = None

	def __init__(self, dataBuffer):
		self.dataBuffer = dataBuffer
		self.stringLength = int.from_bytes(dataBuffer[1], byteorder='big')
		print(dataBuffer)
		#delta, cursor = self.readVaqFromBuffer(dataBuffer[1:])
		#self.stringLength = delta

	def readVaqFromBuffer(self, dataBuffer):
		vaqString = ""
		cursor = 0
		deltaTime = 0
		for i in range(0, len(dataBuffer)):
			byte = dataBuffer[i]
			asString = bin(int.from_bytes(byte, byteorder="big")).strip('0b')
			vaqString = asString[1:] + vaqString

			if int.from_bytes(byte, byteorder="big") & 0b10000000 != 0b10000000:
				cursor += 1
				break

			cursor +=1

		if vaqString != "":
			deltaTime = int(vaqString, 2)

		return (deltaTime, cursor)

	def getOffset(self):
		return self.stringLength

	def getClassName(self):
		return "SequenceTrackName"