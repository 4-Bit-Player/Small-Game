import time
from player import user, u_KeyInput
from places import quests, locations, unlock
from decoration import deco, story


def generate_quests_for_save():
    finished = []
    for quest in quests.finished_quests:
        finished.append(quest["name"])

    active = []
    for quest in quests.active_quests:
        active.append((quest["name"], quest["progress"]))
    return finished, active


def load_saved_quests(finished, active):
    quests.init_quests()
    tmp_quests = []
    # Converting the saved quests to real quests
    for quest_name in finished:
        if quest_name in quests.quests:
            r_quest = quests.get_quest(quest_name)
            if r_quest["refresh_on_load"]:
                unlock_quest(r_quest)
            quests.finished_quests.append(r_quest)

    for quest in active:
        if quest[0] in quests.quests:
            r_quest = quests.get_quest(quest[0])
            for key, val in quest[1].items():
                if key in r_quest["progress"]:
                    r_quest["progress"][key] = val
            tmp_quests.append(r_quest)

    # Check if other start quests are added
    for quest in quests.active_quests:
        name = quest["name"]
        found = [d for d in quests.finished_quests if d.get("name") == name]
        if found:
            continue
        found = [d for d in tmp_quests if d.get("name") == name]
        if found:
            continue
        tmp_quests.append(quest)

    quests.active_quests = tmp_quests


def check_active_quests():
    show = []
    for quest in quests.active_quests:
        if not quest["hidden"]:
            show.append(quest)
    deco.print_header("Quests", 1, "~")
    output = ["Back"]
    for quest in show:
        output.append(quest["name"])
        for req, amount in quest["req"].items():
            output.append([f"   {quest['type']} {req}: {quest['progress'][req]}/{amount}"])
    u_KeyInput.keyinput(output)
    deco.clear_l(1, "")


def progress(event: dict):
    updated = False
    if event["type"] == "Hunt":
        for quest in quests.active_quests:
            if quest["type"] == "Hunt":
                for enemy in quest["req"].keys():
                    if enemy == event["enemy"]["name"]:
                        quest["progress"][enemy] += 1
                        updated = True
    if updated:
        check_quests()


def check_quests():
    deco.clear_l(1, "")
    absolved_quest = []
    for quest in quests.active_quests:
        done = 0
        for req, amount in quest["progress"].items():
            if amount >= quest["req"][req]:
                done += 1

        if done == len(quest["progress"]):
            absolved_quest.append(quest)

    if absolved_quest:
        for quest in absolved_quest:
            quests.active_quests.remove(quest)

            # find a better solution:
            if quest["repeatable"]:
                quests.active_quests.append(quests.get_quest(quest["name"]))
            else:
                quests.finished_quests.append(quest)

            unlock_quest(quest)
            if "unlock_header" in quest:
                deco.print_header(quest['unlock_header'], 0, "~")
            else:
                deco.print_header(f"Quest {quest['name']} completed.", 0, "~")
            if quest["unlock_text"]:
                time.sleep(0.2)
                story.show_text(quest["unlock_text"], False)
                print()

        input("Press enter to continue")


def unlock_quest(quest):
    q_type = quest["u_type"]
    if q_type == "stat_boost":
        stat_boost(quest)
        return
    if q_type == "inspect":
        location = locations.search_location(quest["place"])
        location["inspect"].append(unlock.unlocks[quest["unlocks"]])



def stat_boost(quest):
    for stat, val in quest["stat_boost"]:
        user.Player[stat] += val


