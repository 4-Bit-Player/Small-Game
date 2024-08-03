from copy import deepcopy

active_quests = []
finished_quests = []


def init_quests():
    global active_quests
    global finished_quests
    active_quests = [
        get_quest("Unlock Dark Forest"),
        get_quest("Unlock Bottom Of Mountain"),
    ]
    finished_quests = []


def get_quest(quest_name):
    return deepcopy(quests[quest_name])


quests = {
    "Unlock Dark Forest": {
        "name": "Unlock Dark Forest",
        "type": "Hunt",
        "req": {"Wild Boar": 1},
        "progress": {"Wild Boar": 0},
        "unlocks": "Unlock Dark Forest",
        "refresh_on_load": True,
        "hidden": True,
        "repeatable": False,
        "unlock_header": "A Hidden Path",
        "unlock_text": ["You spot a hidden path.", "Maybe you can look around and find out where it leads to."]
    },
    "Unlock Bottom Of Mountain": {
        "name": "Unlock Bottom Of Mountain",
        "type": "Hunt",
        "req": {"Big Wild Boar": 1},
        "progress": {"Big Wild Boar": 0},
        "unlocks": "Unlock Bottom Of Mountain",
        "refresh_on_load": True,
        "hidden": True,
        "repeatable": False,
        "unlock_header": "The Deer",
        "unlock_text": ["While skinning the Boar you spot a rather large Deer looking in your direction.",
                        "It's fur looks like it has a faint white glow.",
                        "Once you noticed it, the deer runs away.",
                        "Maybe you can look around to see if you can follow it's trail?"]
    }
}


















































