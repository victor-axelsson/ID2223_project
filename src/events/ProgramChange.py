class ProgramChange:
	dataBuffer = None
	def __init__(self, dataBuffer):
		self.dataBuffer = dataBuffer

	def getOffset(self):
		return 1

	def getClassName(self):
		return "ProgramChange"