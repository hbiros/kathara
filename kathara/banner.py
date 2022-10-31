import pyfiglet
import time
import os

def banner():
    ascii_banner = pyfiglet.figlet_format("Kathara Net Creator")
    ascii_banner_segments = str(ascii_banner).split('\n')
    for segment in ascii_banner_segments:
        print(segment)
        time.sleep(0.02)

def print_menu(prompt, options):
    col, _ = os.get_terminal_size()
    print("+"+"-"*(col-2)+"+")
    if len(prompt) > col - 2:
        words = prompt.split()
        line = ""
        for word in words:
            if len(line) + len(word) < col - 3:
                line += word + " "
            else:
                padding = (int(col - 2 - len(line)) / 2) * " "
                line = padding + line + padding
                line += (col - 2 - len(line)) * "  "
                print("|" + line + "|")         
                line = ""
    else:
        padding = int((col - 2 - len(prompt)) / 2) * " "
        prompt = padding + prompt + padding
        prompt += int((col - 2 - len(prompt))) * " "
        print("|"+prompt+"|")
    line = ""
    for index, option in enumerate(options, start=1):
        if len(line) + len(option) < col-4 and index != len(options):
            line += str(index) + "." + option + " "
        else:
            padding = int((col - 2 - len(line)) / 2 )* " "
            line = padding + line + padding
            line += int(col - 2 - len(line)) * " "
            print("|" + line + "|")
            line = ""
    print("+"+"-"*(col-2)+"+")
    choices = []
    while True:
        choice = input()
        if choice == "" and len(choices) != 0:
            break
        while True:
            if choice == "":
                print("Nothing was selected")
                choice = input()
            try:
                choice = int(choice)
                break
            except ValueError:
                print("Input is not a number. It's a string")
                choice = input()
                continue
        if choice <= len(options) and choice >= 1 and choice not in choices:
            print(options[choice-1] + " enabled")
            choices.append(choice)
        elif choice in choices:
            print(options[choice-1] + " already enabled")        
        else:
            print(choice + " is not valid option")
    return choices