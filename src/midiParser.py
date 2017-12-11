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
	rsBuf = None    # Running status buffer, handles skipped status bytes in Channel Voice events

	def __init__(self, filepath, format=True):
		self.filepath = filepath
		if format:
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

	# TODO move out to helpers, class-independent
	def getBit(self, byte, idx):
		return ((byte & (1 << idx)) >> idx)

	def readBytes(self, n, byteArray, offset=0):
		newOffset = offset + n
		if newOffset > len(byteArray):
			raise Exception("Requested bytes ({})exceed byteArray length {}".format(newOffset, len(byteArray)))
		return int.from_bytes(byteArray[offset : newOffset], byteorder='big'), newOffset

	def parseVaq(self, byteArray, offset=0):
		dtbyte, offset = self.readBytes(1, byteArray, offset)
		vaq = 0x00
		while self.getBit(dtbyte, 7) == 1:
			vaq = (vaq << 7) + (dtbyte & 0x7F)
			dtbyte, offset = self.readBytes(1, byteArray, offset)
		# Parse remaining
		vaq = (vaq << 7) + (dtbyte & 0x7F)
		deltaTime = int(vaq)
		return (deltaTime, offset)

	def _parseTrack(self, binary_file):
		ofs = 0
		# Parse the track data
		chunkId = binary_file.read(4)
		if not chunkId == b'MTrk':
			print("WARN: Expected track chunk type to equal 'MTrk, got {}. Skipping...".format(chunkId))
			# TODO parse through rest of record until next MTrk? Check dependencies in caller
			return
		chunkSize = self.toInt(binary_file.read(4))

		eventDataBytes = bytearray(binary_file.read(chunkSize))
		events = []

		while (ofs < len(eventDataBytes)):
			# Parse variable-length quantity for delta time
			dt, ofs = self.parseVaq(eventDataBytes, ofs)
			statusByte, ofs = self.readBytes(1, eventDataBytes, ofs)

			if 0xF0 <= statusByte and statusByte <= 0xF7:
				# Clear the running status buffer; non-voice event received
				self.rsBuf = None

			if statusByte == 0xF0 or statusByte == 0xF7:
				dataLength, ofs = self.parseVaq(eventDataBytes, ofs)
				data, ofs = self.readBytes(dataLength, eventDataBytes, ofs)

				print("SysEx event: length {}, data {}".format(dataLength, data))
				ev = SystemExclusiveEvent(statusByte, dataLength, data, dt)
				events.append(ev)

			elif statusByte == 0xFF:
				metaType, ofs = self.readBytes(1, eventDataBytes, ofs)
				dataLength, ofs = self.parseVaq(eventDataBytes, ofs)
				data, ofs = self.readBytes(dataLength, eventDataBytes, ofs)

				print("Meta event: type {} with length {} and data {}".format(metaType, dataLength, data))
				if metaType == 0x2f: # end of track
					events.append(EndOfTrack())
					break
				ev = MetaEvent(metaType, dataLength, data, dt)
				events.append(ev)
			else:
				print("Channel event with data={}".format(hex(statusByte)))
				statusNibble = (statusByte >> 4)
				channel = (statusByte & 0xFF) #TODO Currently unused

				if 0x80 <= statusByte <= 0xEF:
					# Buffer stores the statusByte when a Voice Category Status (ie, 0x80 to 0xEF) is received.
					self.rsBuf = statusByte
				else:
					print("Running statusByte detected on {} (with running status={})".format(statusByte, hex(self.rsBuf)))
					# Reverse read so that byte can be used as param1
					# self.rsBuf points to our correct status
					ofs -= 1

				param1, ofs = self.readBytes(1, eventDataBytes, ofs)
				param2 = 0x00
				if statusNibble == 0xC or statusNibble == 0xD:
					dataLength = 1
				else:
					length = 2
					dataLength, ofs = self.readBytes(1, eventDataBytes, ofs)

				if self.rsBuf is not None:
					# Ignore any events without a status, running or otherwise
					print("Read data {}, {}".format(hex(param1), hex(param2)))
					ev = MidiChannelEvent(self.rsBuf, dataLength, dt, param1, param2)
					events.append(ev)

		return TrackChunk(chunkId, chunkSize, events)


	def _format(self):
		with open(self.filepath, "rb") as binary_file:

			# Seek position and read N bytes
			binary_file.seek(0)  # Go to beginning

			#Grab the header of the file
			header = self._formatHeader(binary_file)

			self.tracks = []

			#Grab all the tracks
			for i in range(header.numberOfTracks):
				track = self._parseTrack(binary_file)
				self.tracks.append(track)
				print("Track " + str(i + 1) + "/" + str(header.numberOfTracks))




