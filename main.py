import os
import sys
from src.filters.NoteTrackFilter import NoteTrackFilter
from src.outputFormats.MatrixFormat import MatrixFormat
from src.drawing.TrackDrawer import TrackDrawer
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
		saveFilepath = '/'.join(filename.replace("midi_files", "midi_images").split("/")[:-1]) + "/"
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
	folder = "midi_files_partitioned/" + sys.argv[1]
	

	total = 0
	for root, dirs, files in os.walk(folder):
		total += len(files)

	print("Total: " + str(total))


	counter = 0
	for filename in glob.iglob( folder +'/**/*.mid', recursive=True):

		print(filename)
	#filename = 'midi_files/9/911.mid'

		saveFilepath = '/'.join(filename.replace(folder, "midi_images").split("/")[:-1]) + "/"
		name = filename.split("/")[-1].replace(".mid", "")
		message = "[" + str(datetime.datetime.now().time()) + "] PARSING => " + str(counter) + "/" + str(total) + " " + str(counter/total * 100) + "%" + " FILE => " + saveFilepath + name
		print(message)
		
		if not os.path.exists(saveFilepath):
			os.makedirs(saveFilepath)

		parser = MidiParser(filename, verbose=False)
		trackFilter = NoteTrackFilter(parser)
		drawer = TrackDrawer(saveFilepath, name)
		formatter = MatrixFormat(trackFilter, drawer)

		counter += 1
		sys.stdout.flush()
