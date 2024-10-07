from copy import deepcopy
from decoration import colors
active_quests = []
finished_quests = []


def init_quests():
    global active_quests
    global finished_quests
    active_quests = [
        get_quest("Unlock Dark Forest"),
        get_quest("Unlock Bottom Of Mountain"),
        get_quest("Unlock The Cave"),
        get_quest("Hunt 10 Boars"),
        get_quest("Hunt 10 Big Boars"),
        get_quest("Hunt 10 Skeletons"),
    ]
    finished_quests = []


def get_quest(quest_name):
    return deepcopy(quests[quest_name])

quests = {
    "Unlock Dark Forest": {
        "name": "Unlock Dark Forest",
        "type": "Hunt",
        "req": {"Wild Boar": 11},
        "progress": {"Wild Boar": 0},
        "unlocks": "Unlock Dark Forest",
        "u_type": "inspect",
        "place": "Forest",
        "refresh_on_load": True,
        "hidden": True,
        "repeatable": False,
        "unlock_header": "A Hidden Path",
        "unlock_text": ["You spot a hidden path.", "Maybe you can look around and find out where it leads to."]
    },
    "Unlock Bottom Of Mountain": {
        "name": "Unlock Bottom Of Mountain",
        "type": "Hunt",
        "req": {"Big Wild Boar": 8},
        "progress": {"Big Wild Boar": 0},
        "unlocks": "Unlock Bottom Of Mountain",
        "u_type": "inspect",
        "place": "Dark Forest",
        "refresh_on_load": True,
        "hidden": True,
        "repeatable": False,
        "unlock_header": "The Deer",
        "unlock_text": ["While skinning the Boar you spot a rather large Deer looking in your direction.",
                        "It's fur looks like it has a faint white glow.",
                        "Once you noticed it, the deer runs away.",
                        "Maybe you can look around to see if you can follow it's trail?"]
    },
    "Unlock The Cave": {
        "name": "Unlock The Cave",
        "type": "Hunt",
        "req": {"Big Wild Boar": 15},
        "progress": {"Big Wild Boar": 0},
        "unlocks": "Unlock The Cave",
        "u_type": "inspect",
        "place": "Bottom of the Mountain",
        "refresh_on_load": True,
        "hidden": True,
        "repeatable": False,
        "unlock_header": "An old Map",
        "unlock_text": ["As you walk slowly through the dark, green undergrowth, you notice a small, withered, sack.",
                        "Inside you find a map of the camp on the bottom of the Mountain.",
                        "It has a location marked at the mountain with a small path leading to it.",
                        "Maybe you can look around and see where it leads to?"
                        ]
    },
    "Hunt 10 Boars": {
        "name": "Hunt 10 Boars",
        "type": "Hunt",
        "req": {"Wild Boar": 10},
        "progress": {"Wild Boar": 0},
        "unlocks": "",
        "u_type": "stat_boost",
        "stat_boost": [("dex", 2)],
        "refresh_on_load": False,
        "hidden": False,
        "repeatable": True,
        "unlock_text": ["You feel a bit faster...", f"{colors.light_blue}dex +2{colors.reset}"]
    },
    "Hunt 10 Big Boars": {
        "name": "Hunt 10 Big Boars",
        "type": "Hunt",
        "req": {"Big Wild Boar": 10},
        "progress": {"Big Wild Boar": 0},
        "unlocks": "",
        "u_type": "stat_boost",
        "stat_boost": [("dex", 3)],
        "refresh_on_load": False,
        "hidden": False,
        "repeatable": True,
        "unlock_text": ["You feel a bit faster...", f"{colors.light_blue}dex +3{colors.reset}"]
    },
    "Hunt 10 Skeletons": {
        "name": "Hunt 10 Skeletons",
        "type": "Hunt",
        "req": {"Skeleton": 10},
        "progress": {"Skeleton": 0},
        "unlocks": "",
        "u_type": "stat_boost",
        "stat_boost": [("dex", 5)],
        "refresh_on_load": False,
        "hidden": True,
        "repeatable": True,
        "unlock_text": ["You feel a bit faster...", f"{colors.light_blue}dex +5{colors.reset}"]
    },





}


















































