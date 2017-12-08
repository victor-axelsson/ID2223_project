from collections import Hashable

class Events(object):
	"""Storage class for common event codes in stringified binary"""
	MetaOrSysex = '1111'        # All meta and system exlusive events begin with 0xF

	class Meta(object):
		Start = '1111'
		EndOfTrack = '00101111'

	class Channel(object):
		NoteOff             = '1000'
		NoteOn              = '1001'
		PolyAftertouch      = '1010'
		ControlChange       = '1011'
		ProgramChange       = '1100'
		ChannelAftertouch   = '1101'


	def __init__(self):
		pass
