import time
import easyocr
import pydirectinput
import win32gui
from PIL import ImageGrab
import numpy as np
import cv2


class Screen:
	def __init__(self, hwnd):
		self.hwnd = hwnd
		self.reader = easyocr.Reader(['en'], gpu=True)

		self.client_left, self.client_top = win32gui.ClientToScreen(hwnd, (0, 0))
		self.cl, self.ct, self.cr, self.cb = win32gui.GetClientRect(hwnd)
		self.client_width = self.cr - self.cl
		self.client_height = self.cb - self.ct
		pass

	def capture(self):
		left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
		img = ImageGrab.grab(bbox=(left, top, right, bottom))
		img_np = np.array(img)
		img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
		return img_cv, left, top

	def find(self, template, threshold=0.85):
		#I vibe-coded the fuck outta this, it may be bad
		img, x0, y0 = self.capture()
		
		gray_screen = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		if len(template.shape) == 3:
			if template.shape[2] == 4:
				template_gray = cv2.cvtColor(template, cv2.COLOR_RGBA2GRAY)
			else: 
				template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
		else:
			template_gray = template

		result = cv2.matchTemplate(gray_screen, template_gray, cv2.TM_CCOEFF_NORMED)
		_, max_val, _, max_loc = cv2.minMaxLoc(result)

		if max_val < threshold:
			print('Failed to find element')
			return []

		h, w = template_gray.shape
		x = x0 + max_loc[0] + w // 2
		y = y0 + max_loc[1] + h // 2

		return [(x, y)]
	
	def get_text_in_region(self, x_start, y_start, width, height):
		img, x0, y0 = self.capture()
		
		roi = img[y_start:y_start+height, x_start:x_start+width]
		
		results = self.reader.readtext(roi)
		
		detected_text = " ".join([res[1] for res in results])
		return detected_text.strip()
	
	def game_click(self, x, y):
		pydirectinput.mouseDown(x,y)
		time.sleep(0.1)
		pydirectinput.mouseUp()

	def game_relative_mouse_movement(self, x_offset, y_offset, steps, duration=0.5):
		pydirectinput.PAUSE = 0
		if steps <= 0:
			pydirectinput.moveRel(x_offset, y_offset)
			return

		x_step = x_offset / steps
		y_step = y_offset / steps
		delay = duration / steps

		for _ in range(steps):
			pydirectinput.moveRel(int(x_step), int(y_step), relative=True)
			time.sleep(delay)
		pydirectinput.PAUSE = .1
