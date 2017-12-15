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
		stackText = ""
		noteText = ""

		for note in notes:
			increment = int(note['x']) - cursor

			#Print the stack
			if increment > 0:
				for i in range(0, increment):
					trackString += " " + stackText

			#Add note to stack
			if self.isOfType(note['type'], 0x9):
				# Note on
				stack.append(note)
				noteText = self.valToChar(note['y'])

			elif self.isOfType(note['type'], 0x8):
				#Note off
				for i in range(0, len(stack)):
					if stack[i]['y'] == note['y']:
						del stack[i]
						break

			#Build the new stack text
			stackText = ""
			for n in stack:
				stackText += self.valToChar(n['y'])

			#Add the note
			trackString += noteText

			#move the cursor
			cursor += increment



			'''
			if increment > 0:
				for i in range(0, increment):
					trackString += " "

					for n in stack:
						trackString += self.valToChar(n['y'])

				cursor += increment
			'''

		filename = self.folder + self.name + '_track[' + str(note['track']) + '].txt'
		with open(filename, 'w+') as f:
			f.write(trackString)

		return filename

	def mergeTracks(self, files):

		allTracks = ""
		for file in files:
			with open(file, 'r') as f:
				allTracks += f.read() + "\n"

		filename =  self.folder + self.name + "_track_all" + '.txt'

		with open(filename, 'w+') as f:
			f.write(allTracks)

		return filename