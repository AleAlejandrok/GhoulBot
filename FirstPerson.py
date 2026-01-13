import os
import time
from PIL import Image
import numpy as np
import pydirectinput
from Screen import Screen
class FirstPerson(Screen):
	@property
	def quest_icon(self):
		path = os.path.abspath('ui/quest.png')
		print(path)
		return np.array(Image.open(path))
	
	def find_active_quest(self):
		self.find(self.quest_icon)

	def get_in_quest_area(self):
		# Calculate upper-right ROI (top 25% height, right 30% width)
		roi_w = int(self.client_width * 0.30)
		roi_h = int(self.client_height * 0.25)
		roi_x = self.client_width - roi_w
		roi_y = 10

		text = self.get_text_in_region(roi_x, roi_y, roi_w, roi_h)
		print(f"UI Text Found: {text}")
		#Eveni and EVE is a common miss from the OCR
		isEvent = "EVE" in text.upper() or "EVENI" in text.upper() or "BOUNTY" in text.upper()
		if isEvent:	
			return True
		else:
			return False
	
	def is_dangerous_event(self):
		roi_w = int(self.client_width * 0.30)
		roi_h = int(self.client_height * 0.25)
		roi_x = self.client_width - roi_w
		roi_y = 10

		text = self.get_text_in_region(roi_x, roi_y, roi_w, roi_h)

		if "LODE BARING" in text.upper():	
			return True
		else:
			return False


	def jiggle(self):
		self.game_relative_mouse_movement(50, 0, 50, .01)
		self.game_relative_mouse_movement(-50, 0, 50, .01)

	def event_loop(self):
		self.game_relative_mouse_movement(0, 1000, 50, .01)
		event_loaded = self.get_in_quest_area()
		start_time = time.time()
		while(not event_loaded):
			#start a timer if timer runs out and no text, return
			event_loaded = self.get_in_quest_area()
			if(time.time() - start_time > 30 and not event_loaded):
				print("Are we late to the event?")
				return
		while(event_loaded):    
			self.jiggle()	
			event_loaded = self.get_in_quest_area()

