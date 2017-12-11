import os
import sys
from src.filters.NoteTrackFilter import NoteTrackFilter

def parsePath(args):
	scriptDir = os.path.dirname(os.path.abspath(__file__))
	fileName = "01 Menuet.mid"
	filePath = "{}/{}".format(scriptDir, fileName)
	return filePath


if __name__ == '__main__':
	from src.midiParser import *

	parser = MidiParser(parsePath(sys.argv), verbose=False)
	
	trackFilter = NoteTrackFilter(parser)

	#print(str(parser.tracks))
