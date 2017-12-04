from src.headerChunk import HeaderChunk
from src.trackChunk import TrackChunk
from src.events.TimeSignature import TimeSignature
from src.events.KeySignature import KeySignature
from src.events.SetTempo import SetTempo
from src.events.EndOfTrack import EndOfTrack
from src.events.WTFIsThisEvent import WTFIsThisEvent
from src.events.SequenceTrackName import SequenceTrackName
from src.events.CopyrightNotice import CopyrightNotice
from src.events.TextEvent import TextEvent
from src.events.Controller import Controller
from src.events.ProgramChange import ProgramChange
from src.events.NoteOn import NoteOn

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

	    return HeaderChunk(chunkID, chunkSize, formatType, numberOfTracks, timeDivision)
   
	def bits(self, bytes):
		for b in bytes:
			for i in range(8):
				yield ((b >> i) & 1, i)

	def getMetadataType(self, type):
		mapper = {
			b'\x00': 'SequenceNumber',
			b'\x01': 'TextEvent',
			b'\x02': 'CopyrightNotice',
			b'\x03': 'SequenceTrackName',	
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
			b'\x7F': 'SequencerSpecific',
			b'!': "WTFIsThisEvent"
		}

		return mapper[type]

	def getMidiChannelType(self, type):
		#We only care about the first 4 bits
		type = int.from_bytes(type, byteorder="big")
		if type <= 15:
			type = type << 4
		else:
			type = type & 0b11110000
		
		print("Type => " + str(type))
		#8
		if type == 0b10000000:
			return 'NoteOff'
		#9
		elif type == 0b10010000:
			return 'NoteOn'
		#A
		elif type == 0b10100000:
			return 'NoteAftertouch'
		#B
		elif type == 0b10110000:
			return 'Controller'
		#C
		elif type == 0b11000000:
			return 'ProgramChange'
		#D
		elif type == 0b11010000:
			return 'ChannelAftertouch'
		#E
		elif type == 0b11100000:
			return 'PitchBend'
		elif type == 0b00100000 :
			return 'WTFIsThisEvent'
		else:
			raise Exception("No such channel type: " + str(type))

	def buildMetadataEvent(self, eventType, bufferData):
		if eventType == 'SequenceNumber':
			raise Exception("Not implemented")
		elif eventType == 'TextEvent':
			return TextEvent(bufferData)
		elif eventType == 'CopyrightNotice':
			return CopyrightNotice(bufferData)
		elif eventType == 'SequenceTrackName':
			return SequenceTrackName(bufferData)
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
			return EndOfTrack(bufferData)
		elif eventType == 'SetTempo':
			return SetTempo(bufferData)
		elif eventType == 'SMPTEOffset':
			raise Exception("Not implemented")
		elif eventType == 'TimeSignature':
			return TimeSignature(bufferData)
		elif eventType == 'KeySignature':
			return KeySignature(bufferData)
		elif eventType == 'SequencerSpecific':
			raise Exception("Not implemented")
		elif eventType == 'WTFIsThisEvent':
			return WTFIsThisEvent(bufferData)
		else:
			raise Exception("There is no such metadata event")

	def buildMidiChannelEvent(self, eventType, bufferData):
		print(eventType)

		if eventType == 'NoteOff':
			raise Exception("Not implemented")
		elif eventType == 'NoteOn':
			return NoteOn(bufferData)
		elif eventType == 'NoteAftertouch':
			raise Exception("Not implemented")
		elif eventType == 'Controller':
			return Controller(bufferData)
		elif eventType == 'ProgramChange':
			return ProgramChange(bufferData)
		elif eventType == 'ChannelAftertouch':
			raise Exception("Not implemented")
		elif eventType == 'PitchBend':
			raise Exception("Not implemented")
		elif eventType == 'WTFIsThisEvent':
			return WTFIsThisEvent(bufferData, 1)
		else:
			raise Exception("There is no such midi channel event")

	def printByte(self, byte):
		for bit, i in self.bits(byte):
				print("Bit: " + str(bit) + " i: " + str(i))

	def readVaqFromBuffer(self, dataBuffer):
		vaqString = ""
		cursor = 0
		deltaTime = 0
		for i in range(0, len(dataBuffer)):
			byte = dataBuffer[i]
			asString = bin(int.from_bytes(byte, byteorder="big")).strip('0b')
			vaqString = asString[1:] + vaqString

			if int.from_bytes(byte, byteorder="big") & 0b10000000 != 0b10000000:
				cursor += 1
				break

			cursor += 1

		if vaqString != "":
			deltaTime = int(vaqString, 2)

		return (deltaTime, cursor)

	def _formatTrack(self, binary_file):
		#Parse the track data
		chunkID = binary_file.read(4)
		chunkSize = self.toInt(binary_file.read(4))
		
		events = []

		trackEventData = binary_file.read(chunkSize)
		L = [trackEventData[i:i+1] for i in range(len(trackEventData))]
		
		while len(L) > 0:
			deltaTime, cursor = self.readVaqFromBuffer(L)

			#Read the event type
			if L[cursor] == b'\xFF':
				cursor += 1
				print("Metadata events")
				type = self.getMetadataType(L[cursor])

				#We use +2 to skip the event type and length fields
				event = self.buildMetadataEvent(type, L[cursor:])
				cursor = cursor + event.getOffset() + 2
				events.append(event)
				L = L[cursor:]

			elif L[cursor] == b'\xF0':
				cursor += 1
				print("System Exclusive Events")
			else:
				print("MIDI channel events")
				print(L[cursor])
				print(L)
				#print(trackEventData)
				type = self.getMidiChannelType(L[cursor])
				midiChannel = int.from_bytes(L[cursor], byteorder="big") & 0b00001111
				
				#We use +2 to skip the event type and length fields
				event = self.buildMidiChannelEvent(type, L[cursor:])
				

				cursor = cursor + event.getOffset() +1
				events.append(event)
				L = L[cursor:]
				#raise Exception("halt")
		
		return TrackChunk(chunkID, chunkSize, events)
		
	def _format(self):	
		with open(self.filepath, "rb") as binary_file:
			# Read the whole file at once
			data = binary_file.read()
			#print(data)

			# Seek position and read N bytes
			binary_file.seek(0)  # Go to beginning

			header = self._formatHeader(binary_file)
			track = self._formatTrack(binary_file)

			track2 = self._formatTrack(binary_file)

			
			
			#print(hex(int(L[2], 2)))

			#track2 = self._formatTrack(binary_file)

			
			#for i in range(0, header.numberOfTracks):




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


