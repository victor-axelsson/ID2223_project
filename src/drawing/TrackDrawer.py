from PIL import Image, ImageDraw
from pilkit.utils import save_image

class TrackDrawer:

	folder = None
	name = None

	def __init__(self, folder, name):
		self.folder = folder
		self.name = name

	def isOfType(self, value, type):
		return value == type or ((value & 0xF0) >> 4) == type

	def drawTrack(self, notes, width):
		
		scale = 1
		w = int(width / scale)
		height = 128

		canvas = (w, height)
		if(w > 2147483647):
			print("Here is seems like we have a very big canvas")
			print(w)

		# init canvas
		im = Image.new('RGBA', canvas, (255, 255, 255, 0))
		draw = ImageDraw.Draw(im)

		# Example of a track
		# {'x': 27950880, 'y': 60, 'type': 144, 'track': 1}
		
		x1 = 0
		x2 = 0

		for note in notes:
			if self.isOfType(note['type'], 0x9):
				x1 = int(note['x'] / scale)
			elif self.isOfType(note['type'], 0x8):
				y1 = height - note['y']
				x2 = int(note['x'] / scale)
				y2 = y1 +1
				draw.rectangle([x1, y1, x2, y2], outline=(0, 0, 0, 255))


		filename = self.folder + self.name + '_track[' + str(note['track']) + '].png'
		save_image(im, filename, 'PNG', options={}, autoconvert=True)
		#im.save(filename)

		return filename

	def mergeTracks(self, files):
		background = Image.open(files[0])

		for i in range(1, len(files)):
			foreground = Image.open(files[i])
			background.paste(foreground, (0, 0), foreground)

		filename =  self.folder + self.name + "_track_all" + '.png'
		save_image(background, filename, 'PNG', options={}, autoconvert=True)
		#background.save(filename)

		return filename