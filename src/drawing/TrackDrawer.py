from PIL import Image, ImageDraw

class TrackDrawer:

	def drawTrack(self, notes, width):
		
		scale = 10000
		w = int(width / scale)
		height = 128

		canvas = (w, height)
		# init canvas
		im = Image.new('RGBA', canvas, (255, 255, 255, 255))
		draw = ImageDraw.Draw(im)

		# Example of a track
		# {'x': 27950880, 'y': 60, 'type': 144, 'track': 1}
		
		for note in notes:
			x1 = int(note['x'] / scale)
			y1 = height - note['y']
			x2 = x1 +5
			y2 = y1 +1 
			draw.rectangle([x1, y1, x2, y2], outline=(0, 0, 0, 255))

		im.save('/Users/victoraxelsson/Desktop/data_projects/ML_project/track'+str(note['track'])+'.png')
		
		#print(notes)