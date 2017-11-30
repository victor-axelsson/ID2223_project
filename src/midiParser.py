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
    
	def _format(self):	
		with open(self.filepath, "rb") as binary_file:
		    # Read the whole file at once
		    data = binary_file.read()
		    #print(data)

		    # Seek position and read N bytes
		    binary_file.seek(0)  # Go to beginning

		    self._formatHeader(binary_file)


		    chunkID = binary_file.read(4)
		    chunkSize = self.toInt(binary_file.read(4))
		    trackEventData = binary_file.read(chunkSize)

		    trackChunk = TrackChunk(chunkID, chunkSize, trackEventData)
		    trackChunk.printIt()


