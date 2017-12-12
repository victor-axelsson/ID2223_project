from src.drawing.TrackDrawer import TrackDrawer
from src.events.MidiChannelEvent import MidiChannelEvent
import inspect

class MatrixFormat:

	trackFilter = None
	drawer = None

	def __init__(self, trackFilter, drawer):
		self.trackFilter = trackFilter
		self.drawer = drawer
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

		if len(files) > 0:
			self.drawer.mergeTracks(files)


	def isOfType(self, value, typeVal):
		return value == typeVal or ((value & (typeVal << 4)) >> 4) == typeVal

	def parseTrack(self, track, trackCounter):
		cursor = 0
		notes = []

		if self.trackFilter.ticksPerBeat > 0:
			for event in track:
				#print(event.type)


				cursor = cursor + ((event.deltaTime / self.trackFilter.ticksPerBeat) * 16)

				if self.isOfType(event.type, 0x9) or self.isOfType(event.type, 0x8):
					if isinstance(event, MidiChannelEvent):
						notes.append({
							'x': cursor,
							'y': event.param1,
							'type': event.type,
							'track': trackCounter
						})
					else:
						print("There is some bug here. This class should not have this type")

		return notes, cursor
