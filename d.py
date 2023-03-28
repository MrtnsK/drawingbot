from time import sleep
from PIL import Image
import mouse
import numpy as np
from math import sqrt, pow

class Drawer:
	def __init__(self, coord):
		self.up_left = coord
		self.x_offset = self.up_left[0]
		self.y_offset = self.up_left[1]
		self.width = 500 # x
		self.height = 500 # y
		self.nb_color = 20
		self.pic_path = './test.png'
		self.pic = None
		self.encountered_colors = set()
		self.colors_pos = {'black': (880, 60), 'grey': (904, 60), 'dark_red': (924, 60), 'red': (946, 60), 'orange': (968, 60), 'yellow': (990, 60), 'green': (1012, 60), 'light_blue': (1035, 60), 'blue': (1056, 60), 'purple': (1075, 60), 'white': (880, 80), 'light_grey': (904, 80), 'brown': (924, 80), 'pink': (946, 80), 'gold': (968, 80), 'light_yellow': (990, 80), 'light_green': (1012, 80), 'lighter_blue': (1035, 80), 'grey_blue': (1056, 80), 'light_purple': (1075, 80)}
		self.colors = {'black': (0, 0, 0, 0), 'grey': (127, 127, 127, 0), 'dark_red': (136, 0, 21, 0), 'red': (237, 28, 36, 0), 'orange': (255, 127, 39, 0), 'yellow': (255, 242, 0, 0), 'green': (34, 177, 76, 0), 'light_blue': (0, 162, 232, 0), 'blue': (63, 72, 204, 0), 'purple': (163, 73, 164, 0), 'white': (255, 255, 255, 0), 'light_grey': (195, 195, 195, 0), 'brown': (185, 122, 87, 0), 'pink': (255, 174, 201, 0), 'gold': (255, 201, 14, 0), 'light_yellow': (239, 228, 176, 0), 'light_green': (181, 230, 29, 0), 'lighter_blue': (153, 217, 234, 0), 'grey_blue': (112, 146, 190, 0), 'light_purple': (200, 191, 231, 0)}
		# self.colors = {'black': (0, 0, 0), 'grey': (127, 127, 127), 'dark_red': (136, 0, 21), 'red': (237, 28, 36), 'orange': (255, 127, 39), 'yellow': (255, 242, 0), 'green': (34, 177, 76), 'light_blue': (0, 162, 232), 'blue': (63, 72, 204), 'purple': (163, 73, 164), 'white': (255, 255, 255), 'light_grey': (195, 195, 195), 'brown': (185, 122, 87), 'pink': (255, 174, 201), 'gold': (255, 201, 14), 'light_yellow': (239, 228, 176), 'light_green': (181, 230, 29), 'lighter_blue': (153, 217, 234), 'grey_blue': (112, 146, 190), 'light_purple': (200, 191, 231)}

	def change_color(self, color):
		print(f'changing color to {color} in {self.colors_pos[color]}')
		x, y = self.colors_pos[color]
		mouse.move(x, y)
		sleep(0.5)
		mouse.click('left')
		sleep(2)

	def place_dot(self, x, y):
		x += self.x_offset
		y += self.y_offset
		mouse.move(x, y)
		mouse.click('left')
		sleep(0.005)

	def compute_distance(self, rgb_ori, rgb_rep):
		return sqrt(pow(rgb_ori[0] - rgb_rep[0], 2) + pow(rgb_ori[1] - rgb_rep[1], 2) + pow(rgb_ori[2] - rgb_rep[2], 2))

	def replace_color(self, x, y):
		highest = 100000000
		color = None
		name = ''
		for key, value in self.colors.items():
			distance = np.linalg.norm(self.pic[y][x] - value)
			if distance < highest:
				color = value
				name = key
				highest = distance
		self.encountered_colors.add(name)
		self.pic[y][x] = color

	def compare_rgb(self, rgb1, rgb2):
		if rgb1[0] == rgb2[0] and rgb1[1] == rgb2[1] and rgb1[2] == rgb2[2]:
			return True
		return False


	def load_pic(self):
		print(f'loading pic from {self.pic_path}')
		image = Image.open(self.pic_path)

		print(f'resizing pic to {self.width}x{self.height}')
		resized = image.resize((self.width, self.height))
		self.pic = np.array(resized)

		for x in range(0, self.width):
			for y in range(0, self.height):
				self.replace_color(x,y)

	def place_line(self, pos1, pos2):
		x1, y1 = pos1
		x2, y2 = pos2
		x1 += self.x_offset
		y1 += self.y_offset
		x2 += self.x_offset
		y2 += self.y_offset
		mouse.drag(x1, y1, x2, y2)
		sleep(0.005)


	def draw(self):
		self.load_pic()
		start_pos = (0, 0)
		end_pos = (0, 0)

		# self.place_line((0, 0), (self.width, 0))
		# self.place_line((0, 0), (0, self.height))

		for color in self.colors_pos.keys():
			if color not in self.encountered_colors:
				# print(f'skipping {color} because pic do not contain this color')
				continue
			self.change_color(color)
			pixel_to_color = np.where((self.pic == self.colors[color]).all(axis=-1))
			for x, y in zip(pixel_to_color[1], pixel_to_color[0]):
				# print(start_pos, end_pos, (x, y))
				if start_pos == (0, 0):
					start_pos = (x, y)
					end_pos = (x, y)
				# print((x, y) == (end_pos[0]+1, end_pos[1]))
				if (x, y) == (end_pos[0]+1, end_pos[1]):
					end_pos = (x, y)
				else:
					self.place_line(start_pos, end_pos)
					start_pos = (x, y)
					end_pos = (x, y)



if __name__ == '__main__':
	print('right click to the upper left zone where you want to draw')
	while True:
		sleep(0.1)
		if mouse.is_pressed('right'):
			coord = mouse.get_position()
			print(coord)
			break
	drawer = Drawer(coord=coord)
	print(drawer.width, drawer.height)
	drawer.draw()

	# while True:
	# 	if mouse.is_pressed('left'):
	# 		print(mouse.get_position())
	# 		sleep(2)
	# 	sleep(1)
