from src.events.types import Events
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
	tracks = None

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
		"""
		Parse a variable-length quantity value in MIDI chunks
		:param stream: the input data stream, aligned to the start of the variable-length quantity
		:return: tuple of parsed delta time and the remainder of the input data stream
		"""
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
		# Parse the track data
		chunkId = binary_file.read(4)
		if not chunkId == b'MTrk':
			print("WARN: Expected track chunk type to equal 'MTrk, got {}. Skipping...".format(chunkId))
			# TODO parse through rest of record until next MTrk? Check dependencies in caller
			return

		chunkSize = self.toInt(binary_file.read(4))

		events = []

		# Extract sequence of events from data
		trackEventData = binary_file.read(chunkSize)
		trackEventDataBinaryString = bin(int.from_bytes(trackEventData, byteorder="big")).strip('0b')

		d, trackEventDataBinaryString = self.readBits(4, trackEventDataBinaryString)
		deltaTime = 0
		first = True

		while len(trackEventDataBinaryString) > 0:

			if not first:
				# Parse # ticks since last event (can be 0)
				deltaTime, trackEventDataBinaryString = self.readVaq(trackEventDataBinaryString)

			#Check first 4 bits
			if d == Events.MetaOrSysex:
				d, trackEventDataBinaryString = self.readBits(4, trackEventDataBinaryString)

				#Metadata events
				if d == Events.Meta.Start:
					type, trackEventDataBinaryString = self.readBytes(1, trackEventDataBinaryString)

					#If you get a end of track, just exit
					if type == Events.Meta.EndOfTrack:
						events.append(EndOfTrack())
						break

					length, trackEventDataBinaryString = self.readVaq(trackEventDataBinaryString)
					data, trackEventDataBinaryString = self.readBytes(length, trackEventDataBinaryString)

					ev =  MetaEvent(type, length, data, deltaTime)
					events.append(ev)

				else:
					type = d
					length, trackEventDataBinaryString = self.readVaq(trackEventDataBinaryString)
					data, trackEventDataBinaryString = self.readBytes(length, trackEventDataBinaryString)

					events.append(SystemExclusiveEvent(type, length, data, deltaTime))

			else:
				# Parse channel message
				type = d
				channel, trackEventDataBinaryString = self.readBits(4, trackEventDataBinaryString)

				#Midi channel events C and D have length 1. The other have length 2
				length = 2
				param1, trackEventDataBinaryString = self.readBytes(1, trackEventDataBinaryString)
				param2 = None
				# TODO Could encode these lengths in event/message definitions
				if type == Events.Channel.ProgramChange or type == Events.Channel.ChannelAftertouch:
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

			# Seek position and read N bytes
			binary_file.seek(0)  # Go to beginning

			#Grab the header of the file
			header = self._formatHeader(binary_file)

			self.tracks = []

			#Grab all the tracks
			for i in range(header.numberOfTracks):
				track = self._formatTrack(binary_file)
				self.tracks.append(track)
				print("Track " + str(i + 1) + "/" + str(header.numberOfTracks))




