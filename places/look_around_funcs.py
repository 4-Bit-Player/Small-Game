from threading import Thread
import combat, random
from decoration.deco import player_hud, line_r
from player import user
from decoration import colors
from player import crafting
from player.keyinput_index_class import LAClass
from player.u_KeyInput import wait_for_keypress, non_blocking_keyinput, get_char
from printing.print_queue import n_print
from time import sleep, perf_counter


def look_around(current_location: dict[str:any]):
    la_class = LAClass(current_location)
    thread = Thread(target=_thread_func, args=[la_class], daemon=True)
    thread.start()
    while la_class.active:
        key = get_char()
        if non_blocking_keyinput(key, la_class) != 0:
            continue
        if la_class.combat:
            combat.combat(current_location)
            la_class.combat = False
            la_class.paused = False
            if user.Player["hp"] <= 0:
                la_class.active = False
                break
            continue
        la_class.active = False
    thread.join()



def _thread_func(la_class:LAClass):
    old_time = perf_counter()
    new_time = old_time
    delta_time = 0
    la_state = LAState(la_class)

    while la_class.active:
        if la_class.paused:
            la_class.updated = True
            while la_class.paused:
                sleep(0.1)
            delta_time = 0
            old_time = perf_counter()
        la_state.update(delta_time)
        if la_class.updated:
            la_class.updated = False
            n_print(la_class.get_text(player_hud()))
        sleep(1/60)
        delta_time = new_time-old_time
        old_time = new_time
        new_time = perf_counter()
    pass

class LAState:
    def __init__(self, la_class:LAClass):
        self.la_class = la_class
        self._delay = random.uniform(0.5, 1.2)
        self._pick = -1
        self.current_location = la_class.location
        self._combat_delay = 1
        self.findable_items = list(la_class.location["findable_items"].keys())
        self.drop_malus = 0
        self._draw_item_index = 0
        random.shuffle(self.findable_items)

    def update(self, delta_time:float) -> None:
        if self._delay > 0:
            self._delay -= delta_time
            return None

        if self._pick == -1:
            self._pick = random.randint(1, 1000)
            if self._pick <= self.current_location["enemy_chance"]:
                self.la_class.add_event("Suddenly you hear something behind you.")
                self.la_class.combat_init = True
                return None

        if self._pick <= self.current_location["enemy_chance"]:
            self._combat_delay -= delta_time
            if self._combat_delay > 0:
                return None
            self.la_class.combat = True
            self.la_class.combat_init = False
            self.la_class.updated = True
            self.la_class.paused = True
            self._delay = 1.3
            self._combat_delay = 1
            self._pick = -1
            return None

        if self._draw_item_index == len(self.current_location["findable_items"]):
            self._reset_item_draws()


        if self._pick <= self.current_location["item_find_chance"]:
            self._draw_item()
            return None
        return None


    def _reset_item_draws(self):
        self._draw_item_index = 0
        random.shuffle(self.findable_items)
        self.drop_malus = 0
        self._pick = -1

    def _draw_item(self):
        for i in range(self._draw_item_index, len(self.findable_items)):
            item = self.findable_items[i]
            self._draw_item_index += 1
            it_pick = random.randint(1, 1000)
            item_ending = ""
            drop_chances = self.current_location["findable_items"][item]
            for amount, chance in drop_chances.items():
                if it_pick <= chance - self.drop_malus:
                    self._delay = 1.3
                    crafting.item_add(item, amount)
                    self.drop_malus += 100
                    if amount >= 2:
                        item_ending = "s"
                    self.la_class.add_event(f'You found {colors.green}{amount}x {item}{item_ending}{colors.reset}.')
                    return None

        if self.drop_malus == 0:
            self._delay = 1.3
            self.la_class.add_event("You didn't find anything useful...")
        self.drop_malus = 0
        random.shuffle(self.findable_items)
        self._pick = -1
        return None



def old_look_around(current_location):
    pick = random.randint(1, 1000)
    out = line_r() + f'\nYou are wandering through the {current_location["name"]} looking for usable Items...\n'
    n_print(out)
    sleep(random.uniform(0.5, 1.2))
    if pick <= current_location["enemy_chance"]:
        out += "Suddenly you hear something behind you.\n"
        n_print(out)
        sleep(1)
        combat.combat(current_location)
        return

    if pick <= current_location["item_find_chance"]:
        drop_malus = 0
        findable_items = list(current_location["findable_items"].keys())
        random.shuffle(findable_items)

        for item in findable_items:
            it_pick = random.randint(1, 1000)

            item_ending = ""

            drop_chances = current_location["findable_items"][item]
            for amount, chance in drop_chances.items():
                if it_pick <= chance - drop_malus:
                    crafting.item_add(item, amount)
                    drop_malus += 100
                    if amount >= 2:
                        item_ending = "s"

                    out += f'You found {colors.green}{amount}x {item}{item_ending}{colors.reset}.\n'
                    n_print(out)
                    sleep(1.3)

                    break

        if drop_malus == 0:
            out += "You didn't find anything useful...\n"

        out += "Press enter to continue...\n"
        n_print(out)
        wait_for_keypress()