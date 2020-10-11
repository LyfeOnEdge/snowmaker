from numpy import zeros, asarray, uint8, copy, full, shape, roll, repeat
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import io, os
import random as rdm

def hex_to_rgba(hex): return [int(hex[i:i+2], 16) for i in range(1,8,2)]
def split_id(self, id): return [int(x) for x in id.split("x")]

#A canvas object used to interface between PIL Image objects and Numpy arrays
#Has some basic drawing methods and load / export options
class Canvas:
	__slots__ = ["width", "height", "array"]
	def __init__(self, width = 1, height = 1, color = (255,255,255,255)):
		assert width > 0 and type(width) is int, "Canvas width must be a postive integer"
		assert height > 0 and type(height) is int, "Canvas height must be a postive integer"
		self.width, self.height = width, height
		self.array = full((height, width, 4), color, dtype = uint8) #Depth of 4 for rgba
	
	def format_id_pair(self, ida, idb):
		x0, y0 = split_id(ida)
		x1, y1 =  split_id(idb)
		return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
	
	def load_bytes(self, bytestring):
		self.load_image(Image.open(io.BytesIO(bytestring)))
	def load_image_from_file(self, imagepath):
		with open(imagepath, "rb") as f: self.load_image(f.read())
	def load_image(self, image):
		self.array, self.width, self.height = asarray(image), image.size[0], image.size[1]
	def load_array(self, array):
		self.array, self.width, self.height = array, len(array[0]), len(array)

	def export_array(self): return copy(self.array)
	def export_image(self): return Image.fromarray(self.array).convert("RGBA")
	def export_tk_image(self): return ImageTk(self.export_image())
	
	def get_pixel_color(self, id):
		x, y = self.split_id(id)
		color = self.array[y][x]
		return color
	def set_pixel_color_id(self, id, color):
		self.set_pixel_color(self.split_id(id), color)
	def set_pixel_color(self, coords, color):
		x,y = coords
		self.array[y][x] = color
	
	def draw_column_id(self, id, color):
		self.draw_row(split_id(id)[0])
	def draw_column(self, x, color):
		self.array[:, x] = color
	
	def draw_row_id(self, id, color):
		self.draw_row(split_id(id)[1])
	def draw_row(self, y, color):
		self.array[y, :] = color
	
	def draw_rectangle_id(self, ida, idb, color):
		self.draw_rectangle(format_id_pair(ida, idb), color)
	def draw_rectangle(self, coords, color):
		x0, y0, x1, y1 = coords
		self.array[y0:y1+1, x0:x1+1] = full((y1-y0+1, x1-x0+1,4), color, dtype = uint8)
	
	def fill_canvas(self, color):
		self.array = full((self.height, self.width, 4), color, dtype = uint8)
	
	def paste_image(self, image, *args, **kwargs):
		self.paste_image_from_array(asarray(image), *args, **kwargs)
	def paste_image_from_file(self, imagepath, *args, **kwargs):
		self.paste_image(Image.open(imagepath), *args, **kwargs)
	def paste_image_from_bytes(self, bytestring, *args, **kwargs):
		self.paste_image(Image.open(io.BytesIO(bytestring)))
	def paste_image_from_array(self, in_array, coords = (0, 0), pastesize = (None, None)):
		x0, y0 = coords #Where in main array to paste
		# if x0 < 0 or y0 < 0 or not type(x0) is int or not type(y0) is int: raise ValueError(f"Paste coordinates must be postive integers, X - {0}, Y - {0}")
		paste_width, paste_height = pastesize #Width and height of passed array to paste
		in_array_width, in_array_height = len(in_array[0]), len(in_array)
		paste_width = paste_width or in_array_width
		paste_height = paste_height or in_array_height
		if paste_width - 1 > in_array_width: raise ValueError("Passed paste width is wider than array")
		if paste_height - 1 > in_array_height: raise ValueError("Passed paste height is taller than array")
		right_paste_boundary = min(x0 + paste_width - 1, self.width)
		bottom_paste_boundary = min(y0 + paste_height - 1, self.height)
		self.array[y0:bottom_paste_boundary, x0:right_paste_boundary] = in_array[0:bottom_paste_boundary-y0, 0:right_paste_boundary-x0]

def shift_array_up(array, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[0:delta, :]
	array[0:-delta, :] = array[delta:, :]
	if wrap: array[-delta:, :] = cpy
	else: array[-delta:, :] = full((delta, len(array[0]), len(array[0][0])), background, dtype = uint8)
def shift_array_down(array, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[-delta:, :]
	array[delta: , :] = array[0:-delta, :]
	if wrap: array[0:delta, :] = cpy
	else: array[0:delta, :] = full((delta, len(array[0]), len(array[0][0])), background, dtype = uint8)
def shift_array_left(array, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[:, 0:delta]
	array[:, 0:-delta] = array[:, delta:]
	if wrap: array[:, -delta:] = cpy
	else: array[:, -delta:, ] = full((delta, len(array), len(array[0][0])), background, dtype = uint8)
def shift_array_right(array, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[:, -delta:]
	array[:, delta:] = array[:, 0:-delta]
	if wrap: array[:, 0:delta] = cpy
	else: array[:, 0:delta] = full((len(array), delta, len(array[0][0])), background, dtype = uint8)
def shift_row_left(array, row, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[row][0:delta]
	array[row][0:-delta] = array[row][delta:]
	if wrap: array[row][-delta:] = cpy
	else: array[row][-delta:] = full((delta, len(array[0][0])), background, dtype = uint8)
def shift_row_right(array, row, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[row][-delta:]
	array[row][delta:] = array[row][0:-delta]
	if wrap: array[row][0:delta] = cpy
	else: array[row][0:delta] = full((delta, len(array[0][0])), background, dtype = uint8)
def shift_column_up(array, column, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[0:delta, column]
	array[0:-delta, column] = array[delta:, column]
	if wrap: array[-delta:, column] = cpy
	else: array[-delta:, column] = full((delta, len(array[0][0])), background, dtype = uint8)
def shift_column_down(array, column, delta, wrap = False, background = (0,0,0,0)):
	if delta < 1: return
	if wrap: cpy = array[-delta:, column]
	array[delta:, column] = array[:-delta, column]
	if wrap: array[:delta, column] = cpy
	else: array[:delta, column] = full((delta, len(array[0][0])), background, dtype = uint8)
def rescale_array_by_width(array, scale):
	return repeat(repeat(array, scale, axis=0), scale, axis=1)

#Vector is a tuple of two ints like (0,-1) [which would make the particles move south]
#Scale is an integer to scale the output frames by
#Rate is the number of new particles spawned per frame
#frames is the number of frames to produce
#color is the rgba color value to set the droplet particles
#background is the rgba color value to set the background to
#the wrap_*_shift arguments specify if the area introduced after the move of the array should be filled with a wrapped copy of the overwritten data or a different value
#*_drift is the number of row / column shifts to attempt each frame advance
#*_drift_radius is the max number of pixels a particle can move in that dimension each frame advance
#*wrap_*_drift argumewnts specify if random drift should cause partciles to wrap
def generate_snow(
		canvas_size,
		scale : int = 1,
		rate : int = 4,
		vector : tuple = (0,1),
		frames : int = 10,
		color : tuple = (255,255,255,255),
		background : tuple = (0,0,0,0),
		wrap_left_shift : bool = False,
		wrap_right_shift : bool = False,
		wrap_up_shift : bool = False,
		wrap_down_shift : bool = False,
		h_drift : int = 50,
		h_drift_radius : int = 4,
		wrap_h_drift : int = True,
		v_drift : int = 10,
		v_drift_radius : int = 4,
		wrap_v_drift : bool = False
	):
	width, height = canvas_size
	assert width > 0 and type(width) is int, "Canvas width must be a postive integer"
	assert height > 0 and type(height) is int, "Canvas height must be a postive integer"
	assert scale > 0 and type(scale) is int, "Scale must be a postive integer"
	assert rate > 0 and type(rate) is int, "Rate must be a postive integer"
	h_shift, v_shift = vector
	assert type(h_shift) is int, "h_shift must be an integer"
	assert type(v_shift) is int, "v_shift must be an integer"
	assert frames > 0 and type(frames) is int, "Frames must be a postive integer"
	assert all((type(v) is int for v in color)), "Color must be a tuple of ints"
	assert all((type(v) is int for v in background)), "background must be a tuple of ints"
	assert type(h_drift) is int, "h_drift must be an integer"
	assert h_drift_radius >= 0 and type(h_drift_radius) is int, "h_drift_radius must be a postive integer or 0"
	assert type(v_drift) is int, "v_drift must be an integer"
	assert v_drift_radius >= 0 and type(v_drift_radius) is int, "v_drift_radius must be a postive integer or 0"
	frame_list = []
	canvas = Canvas(width, height, background)
	array = canvas.array
	def generate_frame(img):
		return img
		"""
		Abstract here to return an image in numpy array format 
		Can be used to draw images like raindrops or snow etc from the points on the array.
		"""
	def advance_frame(add = True): #Steps a frame in the animation, when true adds a frame to the list
		#Generate image from array and get its pallet space
		if h_drift: #Make snow randomly drift back and forth
			for _ in range(rdm.randrange(0,h_drift)):
				shift_row_right(array, rdm.randrange(height), rdm.randrange(1, h_drift_radius),
					background = background, wrap = wrap_h_drift)
				shift_row_left(array, rdm.randrange(height), rdm.randrange(1, h_drift_radius),
					background = background, wrap = wrap_h_drift)
		if v_drift: #Make snow randomly drift up and down
			for _ in range(rdm.randrange(0,int(v_drift))): 
				shift_column_up(array, rdm.randrange(width), rdm.randrange(1, v_drift_radius),
					background = background, wrap = wrap_v_drift)
				shift_column_down(array, rdm.randrange(width), rdm.randrange(1, v_drift_radius),
					background = background, wrap = wrap_v_drift)
		# #Spawn Drops
		for _ in range(rdm.randrange(0, 2*rate)):
			canvas.array[0][rdm.randrange(width)] = color
		#Apply vector
		if h_shift < 0:
			shift_array_left(array, abs(h_shift),
				background = background, wrap = wrap_left_shift)
		elif h_shift > 0:
			shift_array_right(array, abs(h_shift),
				background = background, wrap = wrap_right_shift)
		if v_shift < 0:
			shift_array_down(array, abs(v_shift),
				background = background, wrap = wrap_down_shift)
		elif v_shift > 0:
			shift_array_up(array, abs(v_shift),
				background = background, wrap = wrap_up_shift)
		if add: #Export array, rescale it, convert to pil image, apply effects, and append to framelist
			img = canvas.export_array()
			if scale > 1: img = rescale_array_by_width(img, scale)
			frame_list.append(Image.fromarray(generate_frame(img))) 
	for _ in range(height): advance_frame(False) #Generate a fully populated screen before grabbing frames
	for _ in range(frames): advance_frame(True) #Generate frames and add to list
	return frame_list

def test():
	frame_list = generate_snow(
		(500, 500),
		scale = 2,
		frames = 300,
		vector = (1,-2),
		rate = 10,
		wrap_right_shift = True,
		wrap_left_shift = True,
		wrap_h_drift = True,
		wrap_v_drift = True
	)#Snow

	frame_list[0].save("test.gif", format='GIF', save_all=True, append_images=frame_list[1:], duration=int(33), loop=0, transparency=255, optimize = False, disposal = 2)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	# parser.add_argument("target", help = "Target dir to archive")
	parser.add_argument("output", help = "Output gif path")
	parser.add_argument("--width", help = "Width of canvas, defaults to 500")
	parser.add_argument("--height", help = "Height of canvas, defaults to 500")
	parser.add_argument("-fg", "--foreground", help = "Color of flakes in hex RGBA, defaults to #FFFFFFFF")
	parser.add_argument("-bg", "--background", help = "Color of background in hex RGBA, defaults to #00000000")
	parser.add_argument("-f", "--frames", help = "Number of frames to output, defaults to 300")
	parser.add_argument("-s", "--scale", help = "Output scale of image, defaults to 1")
	parser.add_argument("-r", "--rate", help = "Particle generation rate, defaults to 2")
	parser.add_argument("-x", "--xvelocity", help = "X velocity of particles on the canvas, defaults to 0")
	parser.add_argument("-y", "--yvelocity", help = "Y velocity of particles on the canvas, defaults to -1")
	parser.add_argument("-wl", "--wrapleft", action='store_true', help = "Wrap particles on canvas shift left")
	parser.add_argument("-wr", "--wrapright", action='store_true', help = "Wrap particles on canvas shift right")
	parser.add_argument("-wu", "--wrapup", action='store_true', help = "Wrap particles on canvas shift up")
	parser.add_argument("-wd", "--wrapdown", action='store_true', help = "Wrap particles on canvas shift down")
	parser.add_argument("-hd", "--horizontaldrift", help = "Number of horizontal drifts to apply in each direction to the canvas to simulate flutter, defaults to 50.")
	parser.add_argument("-hr", "--horizontaldriftradius", help = "Max size of horizontal drift, defaults to 4")
	parser.add_argument("-whd", "--wraphorizontaldrift", action='store_true', help = "Wrap particles on horizontal drift")
	parser.add_argument("-vd", "--verticaldrift", help = "Number of vertical drifts to apply in each direction to the canvas to simulate flutter, defaults to 50.")
	parser.add_argument("-vr", "--verticaldriftradius", help = "Max size of vertical drift, defaults to 10")
	parser.add_argument("-wvd", "--wrapverticaldrift", action='store_true', help = "Wrap particles on vertical drift")

	args = parser.parse_args()
	output = os.path.abspath(args.output)
	frames = int(args.frames) if args.frames else 300
	width = int(args.width) if args.width else 500
	height = int(args.height) if args.height else 500
	foreground = hex_to_rgba(args.foreground) if args.foreground else (255,255,255,255)
	background = hex_to_rgba(args.background) if args.background else (0,0,0,0)
	xvelocity = int(args.xvelocity) if args.xvelocity else 0
	yvelocity = int(args.yvelocity) if args.yvelocity else -1
	scale = int(args.scale) if args.scale else 1
	rate = int(args.rate) if args.rate else 10
	wrapleft = args.wrapleft
	wrapright = args.wrapright
	wrapup = args.wrapup
	wrapdown = args.wrapdown
	h_drift = int(args.horizontaldrift) if args.horizontaldrift else 50
	h_drift_radius = int(args.horizontaldriftradius) if args.horizontaldriftradius else 4
	wrap_h_drift = args.wraphorizontaldrift
	v_drift = int(args.verticaldrift) if args.verticaldrift else 10
	v_drift_radius = int(args.verticaldriftradius) if args.verticaldriftradius else 4
	wrap_v_drift = args.wrapverticaldrift

	frame_list = generate_snow(
		(width, height),
		scale = scale,
		rate = rate,
		vector = (xvelocity,yvelocity),
		frames = frames,
		color = foreground,
		background = background,
		wrap_left_shift = wrapleft,
		wrap_right_shift = wrapright,
		wrap_up_shift = wrapup,
		wrap_down_shift = wrapdown,
		h_drift = h_drift,
		h_drift_radius = h_drift_radius,
		wrap_h_drift = wrap_h_drift,
		v_drift = v_drift,
		v_drift_radius = v_drift_radius,
		wrap_v_drift = wrap_v_drift
	)#Snow
	frame_list[0].save(output, format='GIF', save_all=True, append_images=frame_list[1:], duration=int(33), loop=0, transparency=255, optimize = False, disposal = 2)