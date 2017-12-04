import binascii
from src.midiParser import * 


#filepath = "/Users/victoraxelsson/Desktop/data_projects/ML_project/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/Classical_www.midiworld.com_MIDIRip/bach/acttrag.mid"
filepath = "/Users/victoraxelsson/Desktop/data_projects/ML_project/01 Menuet.mid"


parser = MidiParser(filepath)

print(parser.tracks)
