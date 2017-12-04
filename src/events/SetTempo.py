class SetTempo:

	dataBuffer = None
	def __init__(self, dataBuffer):
		self.dataBuffer = dataBuffer

	def getOffset(self):
		return 3

	def getClassName(self):
		return "SetTemp"