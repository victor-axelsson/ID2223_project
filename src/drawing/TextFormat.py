class TextFormat:

	def __init__(self, folder, name):
		self.folder = folder
		self.name = name

	def isOfType(self, value, type):
		return value == type or ((value & 0xF0) >> 4) == type

	def valToChar(self, val):
		return chr(val)

	def drawTrack(self, notes, width):

		cursor = 0
		trackString = ""
		stack = []

		for note in notes:
			increment = int(note['x']) - cursor
			cursor += increment



			if self.isOfType(note['type'], 0x9):
				# Note on
				stack.append(note)
			elif self.isOfType(note['type'], 0x8):
				#Note of
				for i in range(0, len(stack)):
					if stack[i]['y'] == note['y']:
						del stack[i]
						break

			for i in range(0, increment):
				trackString += " "

				for n in stack:
					trackString += self.valToChar(n['y'])

		filename = self.folder + self.name + '_track[' + str(note['track']) + '].txt'
		with open(filename, 'w') as f:
			f.write(trackString)

		return filename

	def mergeTracks(self, files):

		allTracks = ""
		for file in files:
			with open(file, 'r') as f:
				allTracks += f.read() + "\n"

		filename =  self.folder + self.name + "_track_all" + '.txt'

		with open(filename, 'w') as f:
			f.write(allTracks)

		return filename