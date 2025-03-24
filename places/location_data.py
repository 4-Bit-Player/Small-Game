import random
import time
from copy import deepcopy
from decoration import colors
from places import unlock, locations as loc
from places.locations import search_location


_weather_day = "sunny"
_unlocks = {}
_unlocked = {}
_location = {}
_past_location = {}
_weather_timer = 0


def unlocks_init():
    global _unlocks
    _unlocks = deepcopy(unlock.unlocks)

def get_current_weather() -> str:
    return _weather_day

def set_current_weather(weather:str) -> None:
    global _weather_day
    _weather_day = weather


def location_init():
    global _location, _past_location, _weather_timer
    loc.locations = deepcopy(loc.default_locations)
    _location = loc.locations[0]
    _past_location = _location
    _weather_timer = 0



def location_back():
    global _past_location, _location
    _location, _past_location = _past_location, _location


def go_to_location(location_name):
    global _past_location, _location
    _past_location = _location
    _location = search_location(location_name["name"])


def search_for_unlock(name:str):
    if name in _unlocks:
        return _unlocks[name]
    else:
        print(colors.red + "Failed To Get Unlock!!\n"+name + colors.reset)
        time.sleep(0.2)
        # wait_for_keypress()

def get_unlocked():
    return _unlocked

def get_location():
    return _location

def get_past_location():
    return _past_location


def weather(current_location):
    global _weather_timer
    if current_location["type"] != "shop":
        if _weather_timer == 0:
            weather_r = random.randint(1, 100)
            if weather_r <= int(current_location["weather"][0]):
                set_current_weather("sunny")
            elif weather_r <= int(current_location["weather"][1]):
                set_current_weather("cloudy")
            else:
                set_current_weather("rainy")

            _weather_timer += 4
        _weather_timer -= 1
        current_location["true_weather"] = _weather_day
    return current_location
