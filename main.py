import os
import sys



def parse_path(args):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "01 Menuet.mid"
    file_path = "{}/{}".format(script_dir, file_name)
    return file_path


if __name__ == '__main__':
    from src.midiParser import *

    file_path = parse_path(sys.argv)
    parser = MidiParser(file_path)
    print(parser.tracks)
