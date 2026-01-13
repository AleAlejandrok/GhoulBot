import pydirectinput
import win32gui
import win32api
import time
from Map import Map
from FirstPerson import FirstPerson
from LoadScreen import LoadScreen

WINDOW_TITLE = "Fallout76"

hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
if not hwnd:
    raise RuntimeError("Window not found")





win32gui.SetForegroundWindow(hwnd)
game_map = Map(hwnd)
first_person = FirstPerson(hwnd)
load_screen = LoadScreen(hwnd)
pydirectinput.PAUSE = .35

# game_map.open()
# game_map.fast_travel_to_highway_town()

while(True):
    game_map.event_loop()
    load_screen.waitForLoadingToFinish()
    # if(first_person.is_dangerous_event()):
    #     game_map.fast_travel_on_self()
    #     load_screen.waitForLoadingToFinish()
    first_person.event_loop()
    game_map.fast_travel_to_highway_town()
    load_screen.waitForLoadingToFinish()








