import time
from decoration import deco
from player import user, u_KeyInput
from printing.print_queue import n_print


def intro_1():
    options = [
        [deco.line_r(), "You can navigate using numbers or using", "the arrow keys.", "", "Skip Intro?"],
        "No",
        "Yes",
        [deco.line_r()]
    ]
    intro_a = int(u_KeyInput.keyinput(options))

    if intro_a == 0:
        out = show_text(intro_text)
        n_print(out + "Start adventure!")
        u_KeyInput.wait_for_keypress()



def outro_alive():
    if user.Player["score"] == 0:
        return show_text(outro_a0)

    elif user.Player["score"] < 100:
        return show_text(outro_a100)

    elif user.Player["score"] < 300:
        return show_text(outro_a300)

    elif user.Player["score"] > 500:
        return show_text(outro_a501)

    else:
        return show_text(outro_a500)


def outro_death():
    out = deco.print_header_r("You died. :(")
    if user.Player["score"] > 500:
        outro_d500.insert(0, out)
        return show_text(outro_d500)
    else:
        return out


def show_text(text, previous_text=""):
    out = deco.line_r() + "\n"
    for i, line in enumerate(text):
        out += deco.format_text_in_line([line]) + "\n"
        n_print(out)
        if i < len(text):
            if not user.test:
                time.sleep((len(line)/25))
    out += deco.line_r() + "\n"
    n_print(out)
    return previous_text + out

outro_a0 = [
    "On the other hand...",
    "Maybe fighting is not for everyone.",
    "You've decided to live the rest of your live somewhere save.",
    "Hoping that you won't face the same fate as your friend."
]
outro_a100 = [
    "The boars were way too strong...",
    'Or maybe you were just unlucky...',
    "But you didn't really want to die as well, so you stopped fighting after one try or two",
    "Hoping that you won't face the same fate as your friend..."
]
outro_a300 = [
    "After a while you decided to stop fighting.",
    '"Is it really appropriate to kill that many boars", you questioned.'
]
outro_a501 = [
    "You've sworn yourself to kill as many boars as possible",
    "And in your opinion, you absolutely did!",
    "You've cleared a wide range around the village and the traveler are safe."
]
outro_a500 = [
    "You've decided to retire after revenging your friend."
]

outro_d500 = [
    "You've sworn yourself to kill as many boars as possible to revenge your friend.",
    "And you did!",
    "You've cleared a wide area around the village so the travelers are safe.",
    "You are seen as a hero by the villagers!",
]

intro_text = [
    "Hello and welcome to my little game.",
    "You are a villager living in a small village.",
    "There are many wild boars lurking outside that are making the passage difficult for everyone to travel.",
    "Because an old friend of you got murdered by one you've sworn yourself to revenge him.",
    "By killing as many boars as possible.",
]
