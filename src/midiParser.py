from src.headerChunk import HeaderChunk
from src.trackChunk import TrackChunk
from src.events.TimeSignature import TimeSignature

class MidiParser:

	filepath = None
	headerChunk = None

	def __init__(self, filepath):
		self.filepath = filepath
		self._format()

	def toInt(self, byte):
		return int.from_bytes(byte, byteorder='big')

	def _formatHeader(self, binary_file):
		#Read the Header for the file		    
	    chunkID = binary_file.read(4)
	    chunkSize = self.toInt(binary_file.read(4))
	    formatType = self.toInt(binary_file.read(2))
	    numberOfTracks = self.toInt(binary_file.read(2))
	    timeDivision = self.toInt(binary_file.read(2))

	    self.headerChunk = HeaderChunk(chunkID, chunkSize, formatType, numberOfTracks, timeDivision)
	    self.headerChunk.printIt()
   
	def bits(self, bytes):
		for b in bytes:
			for i in range(8):
				yield ((b >> i) & 1, i)

	def getMetadataType(self, type):
		mapper = {
			b'\x00': 'SequenceNumber',
			b'\x01': 'TextEvent',
			b'\x02': 'CopyrightNotice',
			b'\x03': 'Sequence/TrackName',	
			b'\x04': 'InstrumentName',	
			b'\x05': 'Lyrics',
			b'\x06': 'Marker',
			b'\x07': 'CuePoint',
			b'\x20': 'MIDIChannelPrefix',
			b'\x2F': 'EndOfTrack',
			b'\x51': 'SetTempo',
			b'\x54': 'SMPTEOffset',
			b'\x58': 'TimeSignature',
			b'\x59': 'KeySignature',
			b'\x7F': 'SequencerSpecific'
		}

		return mapper[type]

	def getMidiChannelType(self, type):
		print(type)
		mapper = {
			b'\x08': 'NoteOff',
			b'\x09': 'NoteOn',
			b'\x0A': 'NoteAftertouch',
			b'\x0B': 'Controller',
			b'\x0C': 'ProgramChange',
			b'\x0D': 'ChannelAftertouch',
			b'\x0E': 'PitchBend'
		}

		return mapper[type]

	def buildMetadataEvent(self, eventType, bufferData):
		if eventType == 'SequenceNumber':
			raise Exception("Not implemented")
		elif eventType == 'TextEvent':
			raise Exception("Not implemented")
		elif eventType == 'CopyrightNotice':
			raise Exception("Not implemented")
		elif eventType == 'Sequence/TrackName':
			raise Exception("Not implemented")
		elif eventType == 'InstrumentName':
			raise Exception("Not implemented")
		elif eventType == 'Lyrics':
			raise Exception("Not implemented")
		elif eventType == 'Marker':
			raise Exception("Not implemented")
		elif eventType == 'CuePoint':
			raise Exception("Not implemented")
		elif eventType == 'MIDIChannelPrefix':
			raise Exception("Not implemented")
		elif eventType == 'EndOfTrack':
			raise Exception("Not implemented")
		elif eventType == 'SetTempo':
			raise Exception("Not implemented")
		elif eventType == 'SMPTEOffset':
			raise Exception("Not implemented")
		elif eventType == 'TimeSignature':
			return TimeSignature(bufferData)
		elif eventType == 'KeySignature':
			raise Exception("Not implemented")
		elif eventType == 'SequencerSpecific':
			raise Exception("Not implemented")
		else:
			raise Exception("There is no such metadata event")

	def buildMidiChannelEvent(self, eventType, bufferData):
		if eventType == 'NoteOff':
			raise Exception("Not implemented")
		elif eventType == 'NoteOn':
			raise Exception("Not implemented")
		elif eventType == 'NoteAftertouch':
			raise Exception("Not implemented")
		elif eventType == 'Controller':
			raise Exception("Not implemented")
		elif eventType == 'ProgramChange':
			raise Exception("Not implemented")
		elif eventType == 'ChannelAftertouch':
			raise Exception("Not implemented")
		elif eventType == 'PitchBend':
			raise Exception("Not implemented")
		else:
			raise Exception("There is no such midi channel event")

	def printByte(self, byte):
		for bit, i in self.bits(byte):
				print("Bit: " + str(bit) + " i: " + str(i))

	def _format(self):	
		with open(self.filepath, "rb") as binary_file:
			# Read the whole file at once
			data = binary_file.read()
			#print(data)

			# Seek position and read N bytes
			binary_file.seek(0)  # Go to beginning

			self._formatHeader(binary_file)

			#Parse the track data
			chunkID = binary_file.read(4)
			chunkSize = self.toInt(binary_file.read(4))
			trackChunk = TrackChunk(chunkID, chunkSize)
			events = []

			trackEventData = binary_file.read(chunkSize)
			L = [trackEventData[i:i+1] for i in range(len(trackEventData))]

			while len(L) > 0:
				print(L)
				#Read the delta time
				vaqString = ""
				cursor = 0
				deltaTime = 0
				for i in range(0, len(L)):
					byte = L[i]
					asString = bin(int.from_bytes(byte, byteorder="big")).strip('0b')
					vaqString = asString[1:] + vaqString

					if int.from_bytes(byte, byteorder="big") & 0b10000000 != 0b10000000:
						cursor += 1
						break

					cursor +=1

				if vaqString == "":
					deltaTime = 0
				else:
					deltaTime = int(vaqString, 2)


				#Read the event type
				if L[cursor] == b'\xFF':
					cursor += 1
					print("Metadata events")
					type = self.getMetadataType(L[cursor])
					#We use +2 to skip the event type and length fields
					cursor += 2
					event = self.buildMetadataEvent(type, L[cursor:])
					cursor = cursor + event.getOffset()
					events.append(event)
					L = L[cursor:]
					print(L)

				elif L[cursor] == b'\xF0':
					cursor += 1
					print("System Exclusive Events")
				else:
					cursor += 1
					print("MIDI channel events")
					event = self.buildMidiChannelEvent(self.getMidiChannelType(L[cursor]), L[cursor +1:])
					cursor = 1 + event.getOffset()
					events.append(event)
					L = L[cursor:]

				print(cursor)

			'''
			byte = binary_file.read(1)
			for bit, i in self.bits(byte):
				print("Bit: " + str(bit) + " i: " + str(i))
			'''


			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b')))
			#print(print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b')))
			#print(print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b')))


			#trackChunk = TrackChunk(chunkID, chunkSize, trackEventData)
			#trackChunk.printIt()


