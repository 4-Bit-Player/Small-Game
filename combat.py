import random
from player import user
from decoration import deco, colors
import time
import enemies


def combat(current_location):

    enemy = enemies.encounter(current_location)

    fighting = True
    log = []
    temp_log = []
    total_hp_lost = 0
    hp_lost = 0
    while fighting:
        deco.clear_l(1)
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
            if pick == 3:
                check_health_combat()
            elif pick == 2:
                dex_try = dex_check(enemy)
                if dex_try:
                    return
                else:
                    enemy, temp_log, hp_lost = attack(enemy, 1)
            elif pick == 1:
                till_death = True
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
    deco.clear_l(1)
    print(temp_log)
    print(f'You\'ve slain the {enemy["name"]}.')
    print(f'The {enemy["name"]} damaged you for {colors.red}{round(hp_lost, 1)} hp{colors.reset} '
          f'and you have {colors.green}{user.Player["hp"]:.1f} {colors.reset}hp left.')
    print(f'You gained {colors.gold}{enemy["gold"]:.1f} Gold{colors.reset} and \033[38;5;93m{enemy["xp"]} xp\033[0;0m.')

    user.player_add_xp(enemy["xp"])
    user.Player["gold"] += enemy["gold"]
    user.Player["score"] += enemy["xp"]

    deco.clear_l()
    print()


def check_health_combat():
    if user.Player["hp"] > 0.7 * user.Player["hp_max"]:
        deco.clear_l(1)
        print("You feel fine.")
        deco.clear_l()

    elif user.Player["hp"] > 0.4 * user.Player["hp_max"]:
        deco.clear_l(1)
        print("You don't feel that well...")
        deco.clear_l()

    else:
        deco.clear_l(1)
        print("You are felling unwell!")
        deco.clear_l()


def dex_check(enemy):
    player_dex = random.randint(1, round(user.Player["dex"]))
    enemy_dex = random.randint(1, round(enemy["dex"]))
    result = player_dex - enemy_dex
    if result >= 0:
        return True
    else:
        return False


def attack(enemy, failed):
    player_action_speed = random.uniform(1, user.Player["dex"])
    enemy_action_speed = random.uniform(1, enemy["dex"])
    enemy_damage = 0
    if failed == 1:
        user.Player["hp"] -= enemy["str"]
        temp_log = f'You stumbled and got hit for {colors.red}{round(enemy["str"], 1)} damage{colors.reset}.'
        return enemy, temp_log, enemy_damage
    else:
        if player_action_speed >= enemy_action_speed:
            player_damage = max(0, user.player_atk() - enemy["def"])
            enemy["hp"] -= player_damage
            temp_log = f'You were faster and hit the {enemy["name"]}' \
                       f' dealing {colors.light_green}{round(player_damage, 1)} damage{colors.reset}.'

            return enemy, temp_log, enemy_damage

        else:
            if enemy["str"] > user.player_def():
                enemy_damage = enemy["str"] - user.player_def()
                user.Player["hp"] -= enemy_damage
                temp_log = (f'The {enemy["name"]} was faster and hit you for {colors.red} '
                            f'{round(enemy_damage, 1)} damage{colors.reset}.')
            else:
                temp_log = (f'\033[38;5;202mThe {enemy["name"]}'
                            " attacked but wasn't strong enough to damage you.\033[0;0m")

            return enemy, temp_log, enemy_damage


fighting_options = ["Fight!", "Fight till one DIES!", "Flee!", "Check Health"]
