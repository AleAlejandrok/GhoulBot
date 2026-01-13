from Screen import Screen
import pydirectinput
from PIL import Image
import numpy as np
import os
import time

class Map(Screen):
	@property
	def highway_town_image(self):
		path = os.path.abspath('ui/highway_town.png')
		return np.array(Image.open(path))

	@property
	def expand_icon_image(self):
		path = os.path.abspath('ui/expand.png')
		return np.array(Image.open(path))
	
	@property
	def normal_event_icon_image(self):
		path = os.path.abspath('ui/normal_event.png')
		return np.array(Image.open(path))
	
	@property
	def mutated_event_icon_image(self):
		path = os.path.abspath('ui/mutated_event.png')
		return np.array(Image.open(path))
	
	def find_expand_icon(self):
		return self.find(self.expand_icon_image)
	
	def fast_travel_on_self(self):
		self.open()
		time.sleep(1)
		x, y = pydirectinput.position()
		self.game_click(x, y)
		pydirectinput.press('enter', duration=.02)

	def find_event_icons(self):
		events = list(filter(None, self.find(self.normal_event_icon_image) + self.find(self.mutated_event_icon_image)))
		return events
	
	def fast_travel_to_event(self, x, y):
		self.game_click(x, y)
		time.sleep(.5)
		pydirectinput.press('enter', duration=.2)
		time.sleep(.5)
		pydirectinput.press('enter', duration=.2)

	def open(self):
		expand_icon = []
		while(not len(expand_icon) > 0):
			pydirectinput.press('m', duration=.02)
			time.sleep(.5)
			expand_icon = self.find_expand_icon()


	def event_loop(self):
		self.open()
		expand_x, expand_y = self.find_expand_icon().pop()
		pydirectinput.moveTo(expand_x, expand_y)
		self.game_click(expand_x, expand_y)
		time.sleep(1)
		pydirectinput.press('z', duration=.02)
		pydirectinput.moveRel(0,-100)
		pydirectinput.moveRel(None, -1000)
		event_found = False
		while(not event_found):
			scraped_events = self.find_event_icons()
			print(f"found {len(scraped_events)}")
			event_found = scraped_events.__len__() > 0
			time.sleep(.5)
		print(f'found event{scraped_events}')
		#just grab the first one for rn, we can do decision trees later
		event_x, event_y = scraped_events.pop()
		self.fast_travel_to_event(event_x, event_y)
		self.fast_travel_to_event(event_x, event_y)


	def zoom_out(self):
		pydirectinput.scroll(-3000)

	def zoom_in(self):
		pydirectinput.scroll(3000)
	
	def pan_left(self):
		center_y = self.client_top + (self.client_height // 2)

		pydirectinput.moveTo(self.client_left, center_y)
		pydirectinput.mouseDown() 
		time.sleep(0.1)

		self.game_relative_mouse_movement(self.client_width, 0, steps=20, duration=0.5)

		time.sleep(0.1)
		pydirectinput.mouseUp()

	def pan_right(self):
		center_y = self.client_top + (self.client_height // 2)
		right_edge = self.client_left + self.client_width - 50
		
		pydirectinput.moveTo(right_edge, center_y)
		pydirectinput.mouseDown() 
		time.sleep(0.1)

		self.game_relative_mouse_movement(-self.client_width + 100, 0, steps=20, duration=0.5)

		time.sleep(0.1)
		pydirectinput.mouseUp()
	
	def tilt_down(self):
		center_x = self.client_left + (self.client_width // 2)
		
		pydirectinput.moveTo(center_x, self.cb)
		pydirectinput.mouseDown()
		time.sleep(0.1)


		self.game_relative_mouse_movement(0, -self.client_height, steps=30, duration=0.8)

		time.sleep(0.1)
		pydirectinput.mouseUp()
	
	def tilt_up(self):
		center_x = self.client_left + (self.client_width // 2)
		start_y = self.client_top + 50  
		
		pydirectinput.moveTo(center_x, start_y)
		
		pydirectinput.mouseDown()
		time.sleep(0.1)

		self.game_relative_mouse_movement(0, self.client_height - 100, steps=30, duration=0.8)

		time.sleep(0.1)
		pydirectinput.mouseUp()

	def fast_travel_to_highway_town	(self):
		self.open()
		time.sleep(1)
		self.zoom_out()
		self.tilt_down()
		self.tilt_down()
		self.tilt_down()	
		self.tilt_down()
		self.tilt_down()

		self.pan_left()
		self.pan_left()

		self.tilt_up()
		self.tilt_up()

		pydirectinput.moveTo(self.client_left, self.client_top + self.client_height)
		self.zoom_in()


		x,y = self.find(self.highway_town_image).pop()
		pydirectinput.moveTo(x,y)
		pydirectinput.moveRel(-1, -1)
		pydirectinput.click()
		time.sleep(1)
		pydirectinput.press('enter', duration=.02)
		pydirectinput.press('enter', duration=.02)
		time.sleep(1)
		pydirectinput.press('down', duration=.02)
		pydirectinput.press('enter', duration=.02)






