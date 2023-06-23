import time
from decoration import deco
from player import user


def intro_1():
    deco.clear_l(1)
    print("Please navigate using numbers.")
    print("Skip Intro?")
    print("1. No")
    print("2. Yes")

    intro_a = int(user.user_input(2))

    if intro_a == 0:
        show_text(intro_text)

        deco.clear_l()

        str(input("Start adventure!"))


def outro_alive():
    if user.Player["score"] == 0:
        show_text(outro_a0)

    elif user.Player["score"] < 100:
        show_text(outro_a100)

    elif user.Player["score"] < 300:
        show_text(outro_a300)

    elif user.Player["score"] > 500:
        show_text(outro_a501)

    else:
        show_text(outro_a500)


def outro_death():
    print("You died. :(")
    if user.Player["score"] > 500:
        show_text(outro_d500)


def show_text(text):
    deco.clear_l(1)
    for i in text:
        print(i)
        time.sleep(len(i)/25)


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

outro_d500 =[
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
