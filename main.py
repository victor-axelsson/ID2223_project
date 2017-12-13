import os
import sys
from src.filters.NoteTrackFilter import NoteTrackFilter
from src.outputFormats.MatrixFormat import MatrixFormat
from src.drawing.TrackDrawer import TrackDrawer
import glob
import datetime
import multiprocessing
import _thread as thread
import threading


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
		files.append(filename)
		counter += 1
	return files, counter

print_lock = threading.Lock()
def safe_print(content):
    with print_lock:
        print(content)

def runThread(files, threadCounter):
	counter = 0
	for filename in files:
		
		saveFilepath = '/'.join(filename.replace("midi_files", "midi_images").split("/")[:-1]) + "/"
		name = filename.split("/")[-1].replace(".mid", "")
		message = "[] PARSING => " + str(counter) + "/" + str(total) + " " + str(counter/total * 100) + "%" + " FILE => " + saveFilepath + name
		safe_print(message)
		
		if not os.path.exists(saveFilepath):
			os.makedirs(saveFilepath)

		parser = MidiParser(filename, verbose=False)
		trackFilter = NoteTrackFilter(parser)
		drawer = TrackDrawer(saveFilepath, name)
		formatter = MatrixFormat(trackFilter, drawer)

		counter += 1
		

if __name__ == '__main__':
	from src.midiParser import *


	files, count = getFiles()
	useThreading = False

	if useThreading:
		print("Getting the file count...")
		cpu_count = multiprocessing.cpu_count()
		
		print(count)
		print(cpu_count)
		print(str(int(count / cpu_count)))

		for i in range(0, cpu_count):
			print("Starting thread")
			f = files[i:int(count / cpu_count)]
			thread.start_new_thread( runThread, (f, i))
	else:
		counter = 0

		#/Users/victoraxelsson/Desktop/data_projects/ML_project/midi_files/9/911.mid
		# midi_images/9/911
		files = ['midi_files/9/911.mid']

		for filename in files:

			saveFilepath = '/'.join(filename.replace("midi_files", "midi_images").split("/")[:-1]) + "/"
			name = filename.split("/")[-1].replace(".mid", "")
			message = "[" + str(datetime.datetime.now().time()) + "] PARSING => " + str(counter) + "/" + str(count) + " " + str(counter/count * 100) + "%" + " FILE => " + saveFilepath + name
			print(message)
			
			if not os.path.exists(saveFilepath):
				os.makedirs(saveFilepath)

			parser = MidiParser(filename, verbose=False)
			trackFilter = NoteTrackFilter(parser)
			drawer = TrackDrawer(saveFilepath, name)
			formatter = MatrixFormat(trackFilter, drawer)

			counter += 1
			

			#print(saveFilepath)

			#parser = MidiParser(filename, verbose=False)
			#trackFilter = NoteTrackFilter(parser)
			#formatter = MatrixFormat(trackFilter)


			#print(str(parser.tracks))
		
