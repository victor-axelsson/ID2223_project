from collections import Hashable

class Events(object):
	"""Storage class for common event codes in stringified binary"""
	MetaOrSysex = '1111'        # All meta and system exlusive events begin with 0xF

	class Meta(object):
		Start = '1111'          # Meta events extend metaOMetaOrSysex with another F, as 0xFF
		Text            = '00000001'
		CopyrightNotice = '00000010'
		TrackName       = '00000011'
		InstrumentName  = '00000100'
		Lyric           = '00000101'
		Marker          = '00000110'
		CuePoint        = '00000111'

		EndOfTrack      = '00101111' # TODO This should really be 0x2F00 = b'0010 1111 0000 0000'

	class Channel(object):
		NoteOff             = '1000'
		NoteOn              = '1001'
		PolyAftertouch      = '1010'
		ControlChange       = '1011'
		ProgramChange       = '1100'
		ChannelAftertouch   = '1101'


	def __init__(self):
		pass
