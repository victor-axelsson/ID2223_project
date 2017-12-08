class MetaEvent:
	type = None
	length = None
	data = None
	deltaTime = None

	def __init__(self, type, length, data, deltaTime):
		self.type = type
		self.length = length
		self.data = data
		self.deltaTime = deltaTime

	def __repr__(self):
		return "[MetaEvent, type: {}, length: {}, deltaTime: {}, data: {}]".format(self.type, self.length, self.deltaTime, self.data)

	def printDataAsAscii(self):
		n = int(self.data, 2)
		stringRep = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
		print(stringRep)

