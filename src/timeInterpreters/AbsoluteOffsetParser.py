from src.events.MidiChannelEvent import MidiChannelEvent
import inspect

class AbsoluteOffsetParser:

	trackFilter = None
	drawer = None

	def __init__(self, trackFilter, drawer):
		self.trackFilter = trackFilter
		self.drawer = drawer
		self.parseToAbsoluteOffset()

	def parseToAbsoluteOffset(self):
		if self.trackFilter.isTypeOne:
			self.parseTypeOne()
		else:
			#raise Exception("The type two time format is not yet implemented")
			print("The type two time format is not yet implemented [SKIPPING]")

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
				file = self.drawer.createTrack(notes, maxCursor)
				if file != None:
					files.append(file)

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


				cursor = cursor + round((event.deltaTime / self.trackFilter.ticksPerBeat) * 16)

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
