import os
import sys
from src.inputFormats.TextInput import TextInput
import glob
import datetime

def parsePath(args):
	scriptDir = os.path.dirname(os.path.abspath(__file__))
	fileName = "bach_846.mid"
	filePath = "{}/{}".format(scriptDir, fileName)
	return filePath
	

if __name__ == '__main__':
	from src.midiParser import *

	print("Parsing to MIDI")

	#inputFolder = "midi_files_partitioned/" + sys.argv[1]
	inputFolder = "midi_files/Classical_Piano_piano-midi.de_MIDIRip"
	outputFolder = "midi_text"

	#Start by reading in the template
	parser = MidiParser("resources/template.mid", verbose=False)
	#textInput = TextInput(parser, "resources/template_track_all.txt")
	#textInput = TextInput(parser, "resources/bach_846_track_all.txt")
	textInput = TextInput(parser, "resources/example.txt")
	textInput.saveToFile("resources/parsed.mid")