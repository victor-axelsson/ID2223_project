import os
import sys
from src.filters.NoteTrackFilter import NoteTrackFilter
from src.timeInterpreters.AbsoluteOffsetParser import AbsoluteOffsetParser
from src.outputFormats.ImageFormat import ImageFormat
from src.outputFormats.TextFormat import TextFormat
import glob
import datetime


def parsePath(args):
	scriptDir = os.path.dirname(os.path.abspath(__file__))
	#fileName = "01 Menuet.mid"
	fileName = "bach_846.mid"
	filePath = "{}/{}".format(scriptDir, fileName)
	return filePath

def getFiles():
	files = []
	counter = 0
	for filename in glob.iglob('midi_files/**/*.mid', recursive=True):
		saveFilepath = '/'.join(filename.replace("midi_files", "midi_text").split("/")[:-1]) + "/"
		name = filename.split("/")[-1].replace(".mid", "")
		files.append({
			'saveFilepath': saveFilepath,
			'name': name
		})
		counter += 1
	return files, counter
	

if __name__ == '__main__':
	from src.midiParser import *

	print("Getting the file count...")
	inputFolder = "midi_files_partitioned/" + sys.argv[1]
	outputFolder = "midi_text"


	total = 0
	for root, dirs, files in os.walk(inputFolder):
		total += len(files)

	print("Total: " + str(total))


	counter = 0
	for filename in glob.iglob( inputFolder +'/**/*.mid', recursive=True):

		#filename = 'midi_files/9/911.mid'
		print(filename)

		saveFilepath = '/'.join(filename.replace(inputFolder, outputFolder).split("/")[:-1]) + "/"
		name = filename.split("/")[-1].replace(".mid", "")
		message = "[" + str(datetime.datetime.now().time()) + "] PARSING => " + str(counter) + "/" + str(total) + " " + str(counter/total * 100) + "%" + " FILE => " + saveFilepath + name
		print(message)
		print(saveFilepath)
		
		if not os.path.exists(saveFilepath):
			os.makedirs(saveFilepath)

		parser = MidiParser(filename, verbose=False)
		trackFilter = NoteTrackFilter(parser)

		#Only parse type one
		if trackFilter.isTypeOne:
			drawer = TextFormat(saveFilepath, name)
			#drawer = ImageFormat(saveFilepath, name)
			formatter = AbsoluteOffsetParser(trackFilter, drawer)
		else:
			print("Skipping type 2 format")

		counter += 1
		sys.stdout.flush()
