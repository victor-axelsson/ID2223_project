class NoteTrackFilter:

	parser = None
	timeDivision = None
	isTypeOne = None
	ticksPerBeat = None
	nrOfSMPTEFrames = None
	clockTicksPerFrame = None

	#This is the events that this filter will keep
	keepEvents = {
		0x9, 	# note on
		0x8, 	# note off
		0x03, 	# Sequence/Track Name
		0x04,	# Instrument Name 
		0x51,	# Set Tempo 
		0x54,	# SMPTE Offset 
		0x58, 	# Time Signature 
		0x59 	# Key Signature 
	}

	tracks = None

	def __init__(self, parser):
		self.parser = parser
		self.timeDivision = parser.headerChunk.timeDivision
		self.setTimeDivision()
		self.filterTracks()

	def isOfType(self, value, typeVal):
		return value == typeVal or ((value & (typeVal << 4)) >> 4) == typeVal

	def setTimeDivision(self):
		if self.timeDivision & 0x8000 == 0x8000:
			self.isTypeOne = False
			self.nrOfSMPTEFrames = (self.timeDivision & 0x7F00) >> 4
			self.clockTicksPerFrame = self.timeDivision & 0x00FF
			#print("Frames per second [ATTENTION, NOT YET PROPERLY TESTED]")
			#raise Exception("Frames per second is not yet implemented")
		else:
			self.isTypeOne = True
			self.ticksPerBeat = self.timeDivision & 0x7FFF

	def filterTracks(self):
		self.tracks = []
		for track in self.parser.tracks:
			self.tracks.append(self.filterTrack(track))

	def filterTrack(self, track):
		events = []
		deltaTime = 0
		for event in track.events:
			#print(event)
			if event.type in self.keepEvents or ((event.type & 0xF0) >> 4) in self.keepEvents:

				if self.isOfType(event.type, 0x9):
					if event.length > 0:
						event.deltaTime += deltaTime
						events.append(event)
						deltaTime = 0
					else:
						#Flip it to a note off value
						event.type = event.type ^ 0b00010000
						event.deltaTime += deltaTime
						events.append(event)
						deltaTime = 0
				else:
					event.deltaTime += deltaTime
					events.append(event)
					deltaTime = 0
			else:
				#We need to keep track of missing delta times when we remove events
				deltaTime += event.deltaTime

		return events
