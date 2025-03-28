from player import user
from decoration import colors
import sys

line_len = 46

def clear_screen(lines_to_remove=20, lines_to_remove_ahead=5):
    sys.stdout.write("\033[E"*lines_to_remove_ahead + "\033[F\033[K"*(lines_to_remove_ahead+lines_to_remove))
    return 
    for i in range(lines_to_remove_ahead):
        sys.stdout.write("\033[E") # Cursor down one line

    for i in range(lines_to_remove + lines_to_remove_ahead):
        sys.stdout.write("\033[F")  # Cursor up one line
        sys.stdout.write("\033[K")  # Clear to the end of line
    #sys.stdout.flush()


def full_clear():
    sys.stdout.write("\033c") # resets the console
    pass

def clear_l(clear_first=0, s='='):
    if clear_first:
        clear_screen()
    sys.stdout.write(s * line_len + "\n")


def line_r(s='='):
    return s * line_len


def print_header(text, clear_first=0, s="="):
    if clear_first:
        clear_screen()
    if len(text) + 2 >= line_len:
        print(text)
        return
    header = " " + text + " "
    header = str.center(header, line_len, s)
    print(header)


def print_header_r(text, s="="):
    if len(text) + 2 >= line_len:
        return text
    header = " " + text + " "
    header = str.center(header, line_len, s)
    return header


def player_hud():
    global line_len
    hp = str(round(user.Player["hp"], 1))
    hp_max = str(round(user.Player["hp_max"], 1))
    lvl = str(user.Player["lvl"])
    xp = str(round(user.Player["xp"], 1))
    xp_max = str(round(90 * pow(1.1, user.Player["lvl"]), 1))
    score = str(round(user.Player["score"], 1))
    damage = str(round(user.player_atk(), 1))
    defense = str(round(user.player_def(), 1))
    dex = str(round(user.player_dex(), 1))
    gold = str(round(user.Player["gold"], 1))

    characters = [
        {"line": "═", "corner_tl": "╔", "corner_tr": "╗", "corner_bl": "╚", "corner_br": "╝",
         "middle_l": "╠", "middle_r": "╣", "middle_c": "╬", "top_d": "╦", "bottom_u": "╩",
         "middle_s": "║"}
    ]

    lvl_name = "Level"
    lvl_len = max(len(lvl), len(lvl_name))
    lvl = str.center(lvl, lvl_len)
    lvl_name = str.center(lvl_name, lvl_len)

    xp = xp + "/" + xp_max
    xp_name = "XP"
    xp_len = max(len(xp), len(xp_name))
    xp = str.center(xp, xp_len)
    xp_name = str.center(xp_name, xp_len)

    hp = hp + "/" + hp_max
    hp_name = "HP"
    hp_len = max(len(hp), len(hp_name))
    hp = str.center(hp, hp_len)
    hp_name = str.center(hp_name, hp_len)

    dam_name = "STR"
    dam_len = max(len(damage), len(dam_name))
    damage = str.center(damage, dam_len)
    dam_name = str.center(dam_name, dam_len)

    defense_name = "DEF"
    defense_len = max(len(defense), len(defense_name))
    defense = str.center(defense, defense_len)
    defense_name = str.center(defense_name, defense_len)

    dex_name = "DEX"
    dex_len = max(len(dex), len(dex_name))
    dex = str.center(dex, dex_len)
    dex_name = str.center(dex_name, dex_len)

    gold_name = "Gold"
    gold_len = max(len(gold), len(gold_name))
    gold = str.center(gold, gold_len)
    gold_name = str.center(gold_name, gold_len)

    sc_name = "Score"
    sc_len = max(len(score), len(sc_name))
    score = str.center(score, sc_len)
    sc_name = str.center(sc_name, sc_len)
    straight_line = characters[0]["line"]
    header = (characters[0]["corner_tl"] +
              straight_line * lvl_len + characters[0]["top_d"] +
              straight_line * xp_len + characters[0]["top_d"] +
              straight_line * hp_len + characters[0]["top_d"] +
              straight_line * dam_len + characters[0]["top_d"] +
              straight_line * defense_len + characters[0]["top_d"] +
              straight_line * dex_len + characters[0]["top_d"] +
              straight_line * gold_len + characters[0]["top_d"] +
              straight_line * sc_len + characters[0]["corner_tr"])

    header2 = str(characters[0]["middle_s"] +
                  colors.turquoise + lvl_name + colors.reset + characters[0]["middle_s"] +
                  colors.pink + xp_name + colors.reset + characters[0]["middle_s"] +
                  colors.green + hp_name + colors.reset + characters[0]["middle_s"] +
                  colors.red + dam_name + colors.reset + characters[0]["middle_s"] +
                  colors.gray + defense_name + colors.reset + characters[0]["middle_s"] +
                  colors.light_blue + dex_name + colors.reset + characters[0]["middle_s"] +
                  colors.gold + gold_name + colors.reset + characters[0]["middle_s"] +
                  colors.light_blue + sc_name + colors.reset + characters[0]["middle_s"])

    header3 = str(characters[0]["middle_l"] +
                  straight_line * lvl_len + characters[0]["middle_c"] +
                  straight_line * xp_len + characters[0]["middle_c"] +
                  straight_line * hp_len + characters[0]["middle_c"] +
                  straight_line * dam_len + characters[0]["middle_c"] +
                  straight_line * defense_len + characters[0]["middle_c"] +
                  straight_line * dex_len + characters[0]["middle_c"] +
                  straight_line * gold_len + characters[0]["middle_c"] +
                  straight_line * sc_len + characters[0]["middle_r"])

    header4 = str(characters[0]["middle_s"] +
                  colors.turquoise + lvl + colors.reset + characters[0]["middle_s"] +
                  colors.pink + xp + colors.reset + characters[0]["middle_s"] +
                  colors.green + hp + colors.reset + characters[0]["middle_s"] +
                  colors.red + damage + colors.reset + characters[0]["middle_s"] +
                  colors.gray + defense + colors.reset + characters[0]["middle_s"] +
                  colors.light_blue + dex + colors.reset + characters[0]["middle_s"] +
                  colors.gold + gold + colors.reset + characters[0]["middle_s"] +
                  colors.light_blue + score + colors.reset + characters[0]["middle_s"])

    last_line = str(characters[0]["corner_bl"] +
                    straight_line * lvl_len + characters[0]["bottom_u"] +
                    straight_line * xp_len + characters[0]["bottom_u"] +
                    straight_line * hp_len + characters[0]["bottom_u"] +
                    straight_line * dam_len + characters[0]["bottom_u"] +
                    straight_line * defense_len + characters[0]["bottom_u"] +
                    straight_line * dex_len + characters[0]["bottom_u"] +
                    straight_line * gold_len + characters[0]["bottom_u"] +
                    straight_line * sc_len + characters[0]["corner_br"])
    line_len = len(last_line)
    out = header + "\n" + header2 + "\n" + header3 + "\n" + header4 + "\n" + last_line
    return out


def print_in_line(text:str):
    if len(text) <= line_len:
        print(text)
        return
    start = 0
    end = start + line_len
    while end < len(text):
        newline = text.find("\n", start)
        if newline != -1:
            if newline - start - 1 <= line_len:
                print(text[start:newline])
                start = newline + 1
                end = start+line_len
                continue
        while end > start and text[end] != ' ':
            end -= 1
        if end == start:
            end = start + line_len
        line = text[start:end]
        while line[0] == " ":
            line = line[1:]
            end+=1
        start = end + 1
        end = start + line_len
        print(line)
    print(text[start:])


def format_text_in_line(text_list: list[str]):
    out = ""
    for line in text_list:
        if len(line) <= line_len:
            out += line + "\n"

        else:
            start = 0
            end = line_len
            while end < len(line):
                if line[end] != ' ':
                    while end > start and line[end] != ' ':
                        end -= 1
                    if end == start:
                        end = start + line_len
                n_line: str = line[start:end]
                n_line = n_line.lstrip()
                out += n_line + "\n"
                start = end + 1
                end = start + line_len
            out += line[start:] + "\n"

    return out[:-1]

def print_in_line_wb(text):
    true_line_length = line_len - 2
    characters = {
        "corner_tl": "╭", "line_vert": "─", "corner_tr": "╮",
        "line_down": "│", "corner_bl": "╰", "corner_br": "╯"
    }
    print(characters["corner_tl"] + characters["line_vert"] * true_line_length + characters["corner_tr"])
    if len(text) <= true_line_length:
        text = text.center(true_line_length)
        print(characters["line_down"] + text + characters["line_down"])
    else:
        start = 0
        end = true_line_length
        while end < len(text):
            if text[end] != ' ':
                while end > start and text[end] != ' ':
                    end -= 1
                if end == start:
                    end = start + true_line_length
            line = text[start:end]

            if line[0] == " ":
                line = line[1:]
            line = line.center(true_line_length)
            print(characters["line_down"] + line + characters["line_down"])

            start = end + 1
            end = start + line_len
        last_line = text[start:].center(true_line_length)
        print(characters["line_down"] + last_line + characters["line_down"])
    print(characters["corner_bl"] + characters["line_vert"] * true_line_length + characters["corner_br"])
