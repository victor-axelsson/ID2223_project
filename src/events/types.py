from collections import Hashable


class Events(object):
	"""Storage class for common event codes in stringified binary"""
	MetaOrSysex = '1111'        # All meta and system exlusive events begin with 0xF

	fromType = dict((v, k) for (k, v) in locals().items() if not str(k).startswith("__") )

	class Meta(object):
		StartSeq = '1111'          # Meta events extend metaOMetaOrSysex with another F, as 0xFF
		Text            = '00000001'
		CopyrightNotice = '00000010'
		TrackName       = '00000011'
		InstrumentName  = '00000100'
		Lyric           = '00000101'
		Marker          = '00000110'
		CuePoint        = '00000111'
		ChannelPrefix   = '00100000'
		EndOfTrack      = '00101111'
		SetTempo        = '01010001'
		SMTPEOffset     = '01010100'
		TimeSignature   = '01011000'
		KeySignature    = '01011001'

		fromType = dict((v, k) for (k, v) in locals().items() if not str(k).startswith("__") )


	class Channel(object):
		NoteOff             = '1000'
		NoteOn              = '1001'
		PolyAftertouch      = '1010'
		ControlChange       = '1011'
		ProgramChange       = '1100'
		ChannelAftertouch   = '1101'

		fromType = dict((v, k) for (k, v) in locals().items())


	def __init__(self):
		pass
