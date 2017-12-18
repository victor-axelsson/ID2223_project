from src.events.MidiChannelEvent import MidiChannelEvent

class TextInput:

	template = None
	fileInput = None
	events = None

	def __init__(self, midiTemplate, fileInput):
		self.template = midiTemplate
		self.fileInput = fileInput
		self._parse()

	def grabFileContents(self, filePath):
		content = ""
		with open(filePath, 'r') as f:
			content = f.read()

		return content

	def asciiToHex(self, asciiChar):
		return ord(asciiChar)

	def addNoteOnValue(self, time, note):
		deltaTime = time * self.template.headerChunk.timeDivision / 16
		#type, length, deltaTime, param1, param2
		event = MidiChannelEvent(0x90, 0, deltaTime, self.asciiToHex(note),  0x50)
		self.events.append(event)

	def addNoteOffValue(self, time, note):
		deltaTime = time * self.template.headerChunk.timeDivision / 16
		#type, length, deltaTime, param1, param2
		event = MidiChannelEvent(0x80, 0, deltaTime, self.asciiToHex(note),  0x50)
		self.events.append(event)

	def _generateEvents(self, pts):
		self.events = []

		stack = set()
		timeCursor = 0
		for pt in pts:

			#Take a shallow copy of the mem-stack
			stackCopy = stack.copy()

			for note in pt:
				if note not in stack:
					stack.add(note)
					self.addNoteOnValue(max(0, timeCursor -1), note)
					timeCursor = 0
				else:
					if note in stackCopy:
						stackCopy.remove(note)

			# Everything that is left in the stack copy was no longer being printed. Therefore, we create a note off
			for note in stackCopy:
				self.addNoteOffValue(max(0, timeCursor -1), note)
				stack.remove(note)
				timeCursor = 0

			timeCursor += 1

	def _parse(self):
		content = self.grabFileContents(self.fileInput)
		pts = content.split(" ")
		self._generateEvents(pts)

		#This is very tied to template file and won't work if you change the template
		#Grab the template events and replace all note events with the new ones
		templateTrack = self.template.tracks[0]
		prefix = templateTrack.events[0:6]
		suffix = templateTrack.events[8:]
		newEvents = prefix + self.events + suffix
		templateTrack.events = newEvents
		self.template.tracks = []
		self.template.tracks.append(templateTrack)
		

	def saveToFile(self, filePath):
		self.template.parseToString(filePath)


