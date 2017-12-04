from src.headerChunk import HeaderChunk
from src.trackChunk import TrackChunk
from src.events.EndOfTrack import EndOfTrack
from src.events.MetaEvent import MetaEvent
from src.events.SystemExclusiveEvent import SystemExclusiveEvent
from src.events.MidiChannelEvent import MidiChannelEvent
import binascii

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

	def printByte(self, byte):
		for bit, i in self.bits(byte):
				print("Bit: " + str(bit) + " i: " + str(i))

	def readVaq(self, stream):
		d, stream = self.readBytes(1, stream)
		vaq = ""
		deltaTime = 0
		while d[0] == '1':
			vaq = vaq + d[1:]
			d, stream = self.readBytes(1, stream)

		vaq = vaq + d[1:]
		deltaTime = int(vaq, 2)
		return (deltaTime, stream)

	def printBinaryAsAscii(self, data):
		n = int('0b' + data, 2)
		print(binascii.unhexlify('%x' % n))

	def _formatTrack(self, binary_file):
		#Parse the track data
		chunkId = binary_file.read(4)
		chunkSize = self.toInt(binary_file.read(4))

		events = []

		trackEventData = binary_file.read(chunkSize)
		trackEventDataBinaryString = bin(int.from_bytes(trackEventData, byteorder="big")).strip('0b')
		
		d, trackEventDataBinaryString = self.readBits(4, trackEventDataBinaryString)
		deltaTime = 0
		first = True

		while len(trackEventDataBinaryString) > 0:

			if not first:
				deltaTime, trackEventDataBinaryString = self.readVaq(trackEventDataBinaryString)

			#Check first 4 bits
			if d == '1111':
				d, trackEventDataBinaryString = self.readBits(4, trackEventDataBinaryString)

				#Metadata events
				if d == '1111':
					type, trackEventDataBinaryString = self.readBytes(1, trackEventDataBinaryString)

					#If you get a end of track, just exit
					if type == '00101111':
						events.append(EndOfTrack())
						break;

					length, trackEventDataBinaryString = self.readVaq(trackEventDataBinaryString)
					data, trackEventDataBinaryString = self.readBytes(length, trackEventDataBinaryString)

					events.append(MetaEvent(type, length, data, deltaTime))

				else:
					print(d)
					type = d
					length, trackEventDataBinaryString = self.readVaq(trackEventDataBinaryString)
					data, trackEventDataBinaryString = self.readBytes(length, trackEventDataBinaryString)
					
					events.append(SystemExclusiveEvent(type, length, data, deltaTime))

			else:
				type = d
				channel, trackEventDataBinaryString = self.readBits(4, trackEventDataBinaryString)

				#Midi channel events C and D have length 1. The other have length 2
				length = 2
				param1, trackEventDataBinaryString = self.readBytes(1, trackEventDataBinaryString)
				param2 = None
				if type == '1100' or type == '1101':
					length = 1
				else:
					param2, trackEventDataBinaryString = self.readBytes(1, trackEventDataBinaryString)

				events.append(MidiChannelEvent(type, length, deltaTime, param1, param2))

			first = False

		return TrackChunk(chunkId, chunkSize, events)
		
	def readBits(self, nrOfBits, stream):
		bits = stream[0:nrOfBits]
		return (bits, stream[nrOfBits:])

	def readBytes(self, nrOfBytes, stream):
		nrOfBits = nrOfBytes * 8
		bits = stream[0:nrOfBits]
		return (bits, stream[nrOfBits:])

	def _format(self):	
		with open(self.filepath, "rb") as binary_file:
			# Read the whole file at once
			#data = binary_file.read()
			#stream = bin(int.from_bytes(data, byteorder="big")).strip('0b')
			#stream = int.from_bytes(data, byteorder="big")

			#print(self.readBits(4, stream))

			# Seek position and read N bytes
			binary_file.seek(0)  # Go to beginning

			header = self._formatHeader(binary_file)
			
			
			for i in range(0, header.numberOfTracks):
				track = self._formatTrack(binary_file)
				print("Track " + str(i) + "/" + str(header.numberOfTracks))
			
			
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


