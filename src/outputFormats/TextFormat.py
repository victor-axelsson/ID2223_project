class TextFormat:

	def __init__(self, folder, name):
		self.folder = folder
		self.name = name

	def isOfType(self, value, type):
		return value == type or ((value & 0xF0) >> 4) == type

	def valToChar(self, val):
		return chr(val)

	def createTrack(self, notes, width):

		cursor = 0
		trackString = ""
		stack = {}
		stackText = ""

		for note in notes:

			increment = int(note['x']) - cursor

			stackText = ""
			for n in stack:
				stackText += self.valToChar(n)

			for i in range(0, increment):
					trackString += " " + stackText

			if self.isOfType(note['type'], 0x9):
				#Note on
				stack[note['y']] = note
			elif self.isOfType(note['type'], 0x8):
				#Note off
				if note['y'] in stack:
					stack.pop(note['y'])

			#move the cursor
			cursor += increment

		filename = self.folder + self.name + '_track[' + str(note['track']) + '].txt'
		with open(filename, 'w+') as f:
			f.write(trackString)

		return filename

	def mergeTracks(self, files):

		
		longestTrack = 0
		tracks = []
		for file in files:
			with open(file, 'r') as f:
				track = f.read()
				longestTrack = max(longestTrack, len(track) + 1)
				tracks.append(track)
				
		allTracks = [""] * longestTrack

		for track in tracks:
			pts = track.split(" ")

			for i in range(0, len(pts)):
				allTracks[i] += pts[i]


		allTracks = " ".join(allTracks)

		filename =  self.folder + self.name + "_track_all" + '.txt'

		with open(filename, 'w+') as f:
			f.write(allTracks)

		return filename