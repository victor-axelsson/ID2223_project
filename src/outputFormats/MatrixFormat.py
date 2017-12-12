from src.drawing.TrackDrawer import TrackDrawer

class MatrixFormat:

	trackFilter = None
	drawer = None

	def __init__(self, trackFilter):
		self.trackFilter = trackFilter
		self.drawer = TrackDrawer()
		self.parseToMatrix()

	def parseToMatrix(self):
		if self.trackFilter.isTypeOne:
			self.parseTypeOne()
		else:
			raise Exception("The type two time format is not yet implemented")

	def parseTypeOne(self):
		trackCounter = 0
		maxCursor = 0; 
		files = []
		for track in self.trackFilter.tracks:	
			#print(track)
			notes, cursor = self.parseTrack(track, trackCounter)
			maxCursor = max(cursor, maxCursor)
			trackCounter += 1
			if len(notes) > 0:
				files.append(self.drawer.drawTrack(notes, maxCursor))

		self.drawer.mergeTracks(files)


	def isOfType(self, value, typeVal):
		return value == typeVal or ((value & (typeVal << 4)) >> 4) == typeVal

	def parseTrack(self, track, trackCounter):
		cursor = 0
		notes = []

		for event in track:
			#print(event.type)


			cursor = cursor + ((event.deltaTime / self.trackFilter.ticksPerBeat) * 16)

			if self.isOfType(event.type, 0x9) or self.isOfType(event.type, 0x8):
				notes.append({
					'x': cursor,
					'y': event.param1,
					'type': event.type,
					'track': trackCounter
				})

		return notes, cursor
