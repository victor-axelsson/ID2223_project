import binascii

class MetaEvent:
	Start = '1111'
	EndOfTrack = '00101111'

	type = None
	length = None
	data = None
	deltaTime = None

	def __init__(self, type, length, data, deltaTime):
		self.type = type
		self.length = length
		self.data = data
		self.deltaTime = deltaTime

	def printDataAsAscii(self):
		n = int('0b' + self.data, 2)
		print(binascii.unhexlify('%x' % n))

