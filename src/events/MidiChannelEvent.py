class MidiChannelEvent:

	type = None
	length = None
	deltaTime = None 
	param1 = None
	param2 = None

	def __init__(self, type, length, deltaTime, param1, param2):
		self.type = type
		self.length = length
		self.deltaTime = deltaTime
		self.param1 = param1
		self.param2 = param2

	def __repr__(self):
		return "[MidiChannelEvent, type: {}, length: {}, deltaTime: {}, param1: {}, param2: {}]".format(self.type, self.length, self.deltaTime, self.param1, self.param2)