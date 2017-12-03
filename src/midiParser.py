from src.headerChunk import HeaderChunk
from src.trackChunk import TrackChunk


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

			#trackEventData = binary_file.read(chunkSize)

			#Read the delta time
			read = True
			vaqString = ""
			deltaTime = 0
			while read or bytesRead >= chunkSize:
				byte = binary_file.read(1)
				bytesRead += 1

				asString = bin(int.from_bytes(byte, byteorder="big")).strip('0b')
				vaqString = asString + vaqString
				if len(asString) < 8 or asString[7] == '0':
					read = False

			if vaqString == "":
				deltaTime = 0
			else:
				deltaTime = int(vaqString, 2)
		


			byte = binary_file.read(1)
			for bit, i in self.bits(byte):
				print("Bit: " + str(bit) + " i: " + str(i))



			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b'))
			#print(print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b')))
			#print(print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b')))
			#print(print(bin(int.from_bytes(binary_file.read(1), byteorder="big")).strip('0b')))


			#trackChunk = TrackChunk(chunkID, chunkSize, trackEventData)
			#trackChunk.printIt()


