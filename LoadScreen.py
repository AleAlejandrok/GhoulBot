from Screen import Screen
import pydirectinput
from PIL import Image
import numpy as np
import os
import time

class LoadScreen(Screen):
	@property
	def loading_icon(self):
		path = os.path.abspath('ui/76_loading.png')
		print(path)
		return np.array(Image.open(path))
	
	def waitForLoadingToFinish(self):
		print('Waiting for load screen')
		time.sleep(1)
		loading_cog = list(filter(None, self.find(self.loading_icon)))
		while(len(loading_cog) == 0):
			loading_cog = self.find(self.loading_icon)
		while(len(loading_cog) > 0):
			loading_cog = self.find(self.loading_icon)
		print('Game has loaded')
		time.sleep(10)
