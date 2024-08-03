import random
from player import user, crafting
from decoration import deco, colors
import time
import enemies
from places import quest_logic


def combat(current_location):

    enemy = enemies.encounter(current_location)

    fighting = True
    log = []
    temp_log = []
    total_hp_lost = 0
    hp_lost = 0
    deco.clear_l(1, "")
    while fighting:
        deco.clear_l()
        print(f'You spotted a {enemy["name"]} Level {enemy["lvl"]}')
        deco.clear_l()
        if temp_log:
            log.append(temp_log)
        for i in log:
            print(i)

        if user.Player["hp"] <= 0:
            fighting = False
        else:
            pick = user.show_pick_actions_list(fighting_options)
            deco.clear_l(1, "")
            if pick == 3:
                check_health_combat()
            elif pick == 2:
                if dex_check(enemy):
                    return
                else:
                    enemy, temp_log, hp_lost = attack(enemy, 1)
            elif pick == 1:
                till_death = True

                deco.clear_l(1)
                print(f'You spotted a {enemy["name"]} Level {enemy["lvl"]}')
                deco.clear_l()
                if log:
                    for line in log:
                        print(line)
                    time.sleep(.5)

                while till_death:
                    enemy, temp_log, hp_lost = attack(enemy, 0)
                    print(temp_log)
                    total_hp_lost += hp_lost
                    time.sleep(.5)

                    if user.Player["hp"] <= 0:
                        fighting = False
                        break
                    elif enemy["hp"] <= 0:
                        break

            else:
                enemy, temp_log, hp_lost = attack(enemy, 0)
                total_hp_lost += hp_lost

            if enemy["hp"] <= 0:
                fight_won(enemy, total_hp_lost, temp_log)
                fighting = False


def fight_won(enemy, hp_lost, temp_log):

    event = {
        "type": "Hunt",
        "enemy": enemy,
    }
    quest_logic.progress(event)


    deco.clear_l(1)
    print(temp_log)
    print(f'You\'ve slain the {enemy["name"]}.')
    print(f'The {enemy["name"]} (lvl {enemy["lvl"]}) damaged you for {colors.red}{round(hp_lost, 1)} hp{colors.reset} '
          f'and you have {colors.green}{user.Player["hp"]:.1f} {colors.reset}hp left.')
    print(f'You gained {colors.gold}{enemy["gold"]:.1f} Gold{colors.reset} and '
          f'{colors.pink}{enemy["xp"]} XP{colors.reset}')

    enemy_drop(enemy)

    user.player_add_xp(enemy["xp"])
    user.Player["gold"] += enemy["gold"]
    user.Player["score"] += enemy["xp"]

    deco.clear_l()
    print()
    str(input("Press enter to continue."))
    deco.clear_l(1, "")


def enemy_drop(enemy):
    for item in enemy["drop"]:
        pick = random.randint(1, 1000)
        for amount, chance in enemy["drop"][item].items():
            if pick <= chance:
                crafting.item_add(item, amount)
                print(f'The {enemy["name"]} dropped {amount}x {item}')
                break


def check_health_combat():
    if user.Player["hp"] > 0.7 * user.Player["hp_max"]:
        deco.clear_l(1)
        print(colors.green, "You feel fine.", colors.reset)
        deco.clear_l()

    elif user.Player["hp"] > 0.4 * user.Player["hp_max"]:
        deco.clear_l(1)
        print(colors.gold, "You don't feel that well...", colors.reset)
        deco.clear_l()

    else:
        deco.clear_l(1)
        print(colors.red, "You are felling unwell!", colors.reset)
        deco.clear_l()


def dex_check(enemy):
    player_dex = random.randint(1, round(user.Player["dex"]))
    enemy_dex = random.randint(1, round(enemy["dex"]))
    result = player_dex - enemy_dex
    if result >= 0:
        return True
    else:
        return False


def attack(enemy, failed=0):
    enemy_damage = 0
    if failed == 1:
        user.Player["hp"] -= enemy["str"]
        temp_log = f'You stumbled and got hit for {colors.red}{round(enemy["str"], 1)} damage{colors.reset}.'
        return enemy, temp_log, enemy_damage

    player_action_speed = random.uniform(1, user.Player["dex"])
    enemy_action_speed = random.uniform(1, enemy["dex"])

    if player_action_speed >= enemy_action_speed:
        enemy, temp_log = pl_attack(enemy)
        return enemy, temp_log, enemy_damage

    else:
        enemy, temp_log, enemy_damage = en_attack(enemy)
        return enemy, temp_log, enemy_damage


def pl_attack(enemy):

    if pl_crit_attack(enemy):
        player_damage = user.player_atk() * 1.3
        enemy["hp"] -= player_damage
        temp_log = f'You surprised the {enemy["name"]} with a quick attack' \
                   f' dealing {colors.light_green}{round(player_damage, 1)} damage{colors.reset}.'

    elif en_defended(enemy):
        player_damage = max(0, user.player_atk() - enemy["def"] * 2)
        enemy["hp"] -= player_damage
        temp_log = f'The {enemy["name"]} expected your attack and defended. You' \
                   f' dealt {colors.light_green}{round(player_damage, 1)} damage{colors.reset}.'

    elif pl_missed(enemy):
        player_damage = max(0, user.player_atk() / 2 - enemy["def"])
        enemy["hp"] -= player_damage
        temp_log = f'The {enemy["name"]} was to quick and you weren\'t able to hit it correctly.' \
                   f' You dealt {colors.light_green}{round(player_damage, 1)} damage{colors.reset}.'

    else:
        player_damage = max(0, user.player_atk() - enemy["def"])
        enemy["hp"] -= player_damage
        temp_log = f'You were faster and hit the {enemy["name"]}' \
                   f' dealing {colors.light_green}{round(player_damage, 1)} damage{colors.reset}.'

    return enemy, temp_log


def en_attack(enemy):
    if en_crit_attack(enemy):
        enemy_damage = enemy["str"] * 1.1
        user.Player["hp"] -= enemy_damage
        temp_log = (f'The {enemy["name"]} surprised you with a swift attack and hit you for {colors.red}'
                    f'{round(enemy_damage, 1)} damage{colors.reset}.')

    elif pl_defended(enemy):
        enemy_damage = max(0, enemy["str"] - user.player_def() * 2)
        user.Player["hp"] -= enemy_damage
        temp_log = (f'You managed to partially block the attack from the {enemy["name"]}. {colors.red}'
                    f'You took {round(enemy_damage, 1)} damage{colors.reset}.')

    elif en_missed(enemy):
        enemy_damage = max(0, enemy["str"] / 2 - user.player_def())
        user.Player["hp"] -= enemy_damage
        temp_log = (f'You managed to partially dodge the attack. You took {colors.red}'
                    f'{round(enemy_damage, 1)} damage{colors.reset}.')

    else:
        enemy_damage = max(0, enemy["str"] - user.player_def())
        user.Player["hp"] -= enemy_damage
        temp_log = (f'The {enemy["name"]} was faster and hit you for {colors.red}'
                    f'{round(enemy_damage, 1)} damage{colors.reset}.')

    return enemy, temp_log, enemy_damage


def en_crit_attack(enemy):
    player_action_speed = random.uniform(1, user.Player["dex"])
    en_action_speed = random.uniform(1, enemy["dex"])
    return en_action_speed > (player_action_speed * 8)


def en_defended(enemy):
    player_action_speed = random.uniform(1, user.Player["dex"])
    en_action_speed = random.uniform(1, enemy["dex"])
    return en_action_speed > (player_action_speed * 5)


def en_missed(enemy):
    player_action_speed = random.uniform(1, user.Player["dex"])
    en_action_speed = random.uniform(1, enemy["dex"])
    return (en_action_speed * 10) < player_action_speed


def pl_crit_attack(enemy):
    player_action_speed = random.uniform(1, user.Player["dex"])
    en_action_speed = random.uniform(1, enemy["dex"])
    return (en_action_speed * 5) < player_action_speed


def pl_defended(enemy):
    player_action_speed = random.uniform(1, user.Player["dex"])
    en_action_speed = random.uniform(1, enemy["dex"])
    return (en_action_speed * 2) < player_action_speed


def pl_missed(enemy):
    player_action_speed = random.uniform(1, user.Player["dex"])
    en_action_speed = random.uniform(1, enemy["dex"])
    return en_action_speed > (player_action_speed * 15)


fighting_options = ["Fight!", "Fight till one DIES!", "Flee!", "Check Health"]
