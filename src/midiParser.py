from src.headerChunk import HeaderChunk
import binascii

from src.events.EndOfTrack import EndOfTrack
from src.events.MetaEvent import MetaEvent
from src.events.MidiChannelEvent import MidiChannelEvent
from src.events.SystemExclusiveEvent import SystemExclusiveEvent
from src.headerChunk import HeaderChunk
from src.trackChunk import TrackChunk


class MidiParser:

	filepath = None
	headerChunk = None
	tracks = None
	rsBuf = None    # Running status buffer, handles skipped status bytes in Channel Voice events
	verbose = None

	def __init__(self, filepath, format=True, verbose=True):
		self.filepath = filepath
		self.verbose = verbose
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
			newOffset = len(byteArray)

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

	def vaqToString(self, intVal):
		intVal = int(intVal)
		strVal = "{0:b}".format(intVal)
		missingZeros = 0

		if len(strVal) % 8 > 0:
			missingZeros = 8 - (len(strVal) % 8)

		#Padd out missing zeros
		for i in range(0, missingZeros):
			strVal = "0" + strVal

		counter = len(strVal) -1
		vaq = ""
		while(counter >= 0):

			i = len(strVal) - counter -1

			if i % 7 == 0 and i > 0:
				if i <= 8:
					vaq =  strVal[counter] + "0" + vaq
				else:
					vaq =  strVal[counter] + "1" + vaq

				if counter == 0 and strVal[counter] == "1":
					vaq =  "1000000" + vaq

			else:
				vaq = strVal[counter] + vaq

			counter -= 1

		return vaq

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

				if self.verbose:
					print("SysEx event: length {}, data {}".format(dataLength, data))
				ev = SystemExclusiveEvent(statusByte, dataLength, data, dt)
				events.append(ev)

			elif statusByte == 0xFF:
				metaType, ofs = self.readBytes(1, eventDataBytes, ofs)
				dataLength, ofs = self.parseVaq(eventDataBytes, ofs)
				data, ofs = self.readBytes(dataLength, eventDataBytes, ofs)

				if self.verbose:
					print("Meta event: type {} with length {} and data {}".format(metaType, dataLength, data))
				if metaType == 0x2f: # end of track
					events.append(EndOfTrack())
					break
				ev = MetaEvent(metaType, dataLength, data, dt)
				events.append(ev)
			else:
				if self.verbose:
					print("Channel event with data={}".format(hex(statusByte)))
				statusNibble = (statusByte >> 4)
				channel = (statusByte & 0xFF) #TODO Currently unused

				if 0x80 <= statusByte <= 0xEF:
					# Buffer stores the statusByte when a Voice Category Status (ie, 0x80 to 0xEF) is received.
					self.rsBuf = statusByte
				else:
					if self.verbose:
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
					if self.verbose:
						print("Read data {}, {}".format(hex(param1), hex(param2)))
					ev = MidiChannelEvent(self.rsBuf, dataLength, dt, param1, param2)
					events.append(ev)

		return TrackChunk(chunkId, chunkSize, events)


	def _format(self):
		with open(self.filepath, "rb") as binary_file:

			# Seek position and read N bytes
			binary_file.seek(0)  # Go to beginning

			#Grab the header of the file
			self.headerChunk = self._formatHeader(binary_file)

			self.tracks = []

			#Grab all the tracks
			for i in range(self.headerChunk.numberOfTracks):
				track = self._parseTrack(binary_file)
				if track != None:
					self.tracks.append(track)
					if self.verbose:
						print("Track " + str(i + 1) + "/" + str(self.headerChunk.numberOfTracks))

	def padhexbytes(self, s, nrOfBytes):
		nrOfNibbles = nrOfBytes * 2
		return self.padhex(s, nrOfNibbles)

	def padhex(self, s, nrOfNibbles):
		hexStr = hex(s)[2:].zfill(nrOfNibbles)
		return bytearray.fromhex(hexStr)

	def bitstring_to_bytes(self, s):
		return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

	def int_to_bytes(self, x):
		return x.to_bytes((x.bit_length() + 7) // 8, 'big')

	def parseToString(self, file):
		with open(file, "wb") as f:
			bytes_written = 0

			#Print header file
			bytes_written += f.write(self.headerChunk.chunkID)
			bytes_written += f.write(self.padhex(self.headerChunk.chunkSize, 8))
			bytes_written += f.write(self.padhex(self.headerChunk.formatType, 4))
			bytes_written += f.write(self.padhex(self.headerChunk.numberOfTracks, 4))
			bytes_written += f.write(self.padhex(self.headerChunk.timeDivision, 4))

			track_size_pos = bytes_written
			#Print tracks
			for track in self.tracks:
				chunkIdBytes = f.write(track.chunkId)
				bytes_written += chunkIdBytes
				track_size_pos += chunkIdBytes


				# Write dummy track size; will be updated after we know all bytes
				bytes_written += f.write(self.padhex(0, 8))
				bytes_written = 0

				#Print events
				for event in track.events:
					event_bytes = 0
					vaq = self.vaqToString(event.deltaTime)
					vaqBytes = self.bitstring_to_bytes(vaq)
					event_bytes += f.write(vaqBytes)

					if isinstance(event, MidiChannelEvent):
						#The type contains both the type (4 bits) and the midi channel (4 bits)
						event_bytes += f.write(bytes((event.type,)))
						event_bytes += f.write(self.padhex(event.param1, 2))
						event_bytes += f.write(self.padhex(event.param2, 2))

					elif isinstance(event, MetaEvent):
						event_bytes += f.write(bytes((0xFF,)))
						event_bytes += f.write(bytes((event.type,)))
						event_bytes += f.write(bytes((event.length,)))
						event_bytes += f.write(self.int_to_bytes(event.data))

					elif isinstance(event, EndOfTrack):
						event_bytes += f.write(bytes((0xFF,)))
						event_bytes += f.write(bytes((0x2f,)))
						event_bytes += f.write(bytes((0x00,)))

					bytes_written += event_bytes
					if self.verbose:
						print("Wrote {}/{} bytes".format(event_bytes, bytes_written))
			f.seek(track_size_pos)
			f.write(self.padhex(bytes_written + 1, 8))
