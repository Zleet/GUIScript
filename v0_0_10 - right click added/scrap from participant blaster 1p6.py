# ====================================================================================================
# Participant Blaster
#
# A program that finds participants in the mcleans system and enters them, one by one.
# Also types participants into blank cells.
#
# Requires Python 3 and the pyautogui GUI automation library to be installed on the computer
#
# Written by Michael McLarnon (bigbadmick2000@hotmail.com) 28/10/16
# ====================================================================================================
# Thursday 27th October 2016 - Stuff To Add:
# 1. A status text line that displays:
#    1. the participant currently being entered
#    2. what number the current participant is in the list of participants (e.g. 15/28 or 3/7 etc.)
#    3. Percentage of participants that have been successfully entered, to a single decimal place
#       (e.g. 53.2%)
#    *** DONE ***
# 2. A Letter Delay text entry box for the user to enter the delay (in seconds) between the program
#    typing successive letters
#    *** DONE ***
# 3. Scroll bar for the big text space that holds the list of participants
#    *** DONE ***
# 4. Highlight the participant being currently entered in the big list of participants
#
# 5. Ensure that the big list of participants scrolls down to always keep the participant being
#    currently entered in view
#
# ====================================================================================================
# imports
import pyautogui, time
from tkinter import *
from tkinter import ttk
# ====================================================================================================
# global variables
current_line_no = 0 # keep a record of the current line index (from zero upwards)

# coordinate information for:
# (1) the save button
# (2) the input line where you search for participants in the McLeans computer system
# (3) the Q button on the top left of the onscreen accessibility keyboard
save_x = -1
save_y = -1
plus_x = -1
plus_y = -1
input_x = -1
input_y = -1
keyboard_q_x = -1
keyboard_q_y = -1
letter_delay = 0.2

# global dictionary to hold the pixel coordinates for the letter keys
# It's structured like this:
# keys = {
#       "a" : {"x" : 345, "y" : 75},
#       "b" : {"x" : 127, "y" : 439},
#       etc...
#       }
keys = {
        "A" : {"x" : -1, "y" : -1},
        "B" : {"x" : -1, "y" : -1},
        "C" : {"x" : -1, "y" : -1},
        "D" : {"x" : -1, "y" : -1},
        "E" : {"x" : -1, "y" : -1},
        "F" : {"x" : -1, "y" : -1},
        "G" : {"x" : -1, "y" : -1},
        "H" : {"x" : -1, "y" : -1},
        "I" : {"x" : -1, "y" : -1},
        "J" : {"x" : -1, "y" : -1},
        "K" : {"x" : -1, "y" : -1},
        "L" : {"x" : -1, "y" : -1},
        "M" : {"x" : -1, "y" : -1},
        "N" : {"x" : -1, "y" : -1},
        "O" : {"x" : -1, "y" : -1},
        "P" : {"x" : -1, "y" : -1},
        "Q" : {"x" : -1, "y" : -1},
        "R" : {"x" : -1, "y" : -1},
        "S" : {"x" : -1, "y" : -1},
        "T" : {"x" : -1, "y" : -1},
        "U" : {"x" : -1, "y" : -1},
        "V" : {"x" : -1, "y" : -1},
        "W" : {"x" : -1, "y" : -1},
        "X" : {"x" : -1, "y" : -1},
        "Y" : {"x" : -1, "y" : -1},
        "Z" : {"x" : -1, "y" : -1},
        "," : {"x" : -1, "y" : -1},
        "backspace" : {"x" : -1, "y" : -1},
        "delete"    : {"x" : -1, "y" : -1},
        "tab"       : {"x" : -1, "y" : -1},
        "shift"     : {"x" : -1, "y" : -1},
        "control"   : {"x" : -1, "y" : -1},
        " "         : {"x" : -1, "y" : -1},
        "enter"     : {"x" : -1, "y" : -1},
        "home"      : {"x" : -1, "y" : -1},
        "end"       : {"x" : -1, "y" : -1},
        "up"        : {"x" : -1, "y" : -1},
        "down"      : {"x" : -1, "y" : -1},
        "left"      : {"x" : -1, "y" : -1},
        "right"     : {"x" : -1, "y" : -1}
        }
# ====================================================================================================
# Map the letters a to z to the pixel coordinates of their keys on the
# onscreen keyboard. The global dictionary that holds the pixel coordinates
# for the letter keys is structured like this:
# keys = {
#       "a" : {"x" : 345, "y" : 75},
#       "b" : {"x" : 127, "y" : 439},
#       etc...
#       }
# ====================================================================================================
def map_keys():

    global keys
    global keyboard_q_x
    global keyboard_q_y

    # horizontal distance between letters on the onscreen keyboard (in pixels)
    # and vertical distance between letter rows
    horizontal_key_distance = 27
    vertical_key_distance = 24

    # read and set the values of the global variables:
    # keyboard_q_x (the x coordinate of the q key on the onscreen keyboard)
    # keyboard_q_y (the y coordinate of the q key on the onscreen keyboard)
    keyboard_q_x = keyboard_q_key_x_text_box.get("1.0", END)
    keyboard_q_x = int(keyboard_q_x.strip())
    print('keyboard_q_x =', keyboard_q_x)

    keyboard_q_y = keyboard_q_key_y_text_box.get("1.0", END)
    keyboard_q_y = int(keyboard_q_y.strip())
    print('keyboard_q_y =', keyboard_q_y)

    # map the three rows of letters
    letter_rows = ['1234567890-=', 'qwertyuiop[]#', "asdfghjkl;'", 'zxcvbnm,./']
    for count in range(len(letter_rows)):
        current_letter_row = letter_rows[count]
        row_start_x = keyboard_q_x - (horizontal_key_distance / 2) + (0.5 * horizontal_key_distance * count) # changed
        row_y = keyboard_q_y - vertical_key_distance + (count * vertical_key_distance)
        for inner_count in range(len(current_letter_row)):
            current_letter = current_letter_row[inner_count]
            keys[current_letter.upper()] = {"x": -1, "y" : -1}
            keys[current_letter.upper()]["x"] = int(row_start_x + (inner_count * horizontal_key_distance))
            keys[current_letter.upper()]["y"] = row_y

    # map the backspace (delete) key to the right of the equals sign at the top of
    # the onscreen keyboard
    x = keys["="]["x"] + horizontal_key_distance
    y = keys["="]["y"]
    keys["backspace"] = {"x" : x, "y" : y}

    # map the tab key on the left of the screen
    x = keys["Q"]["x"] - horizontal_key_distance
    y = keys["Q"]["y"]
    keys["tab"] = {"x" : x, "y" : y}

    # map the shift key on the left of the screen
    x = keys["Z"]["x"] - horizontal_key_distance
    y = keys["Z"]["y"]
    keys["shift"] = {"x" : x, "y" : y}

    # map the control key on the bottom left of the onscreen keyboard
    x = keys["Z"]["x"] - (2 * horizontal_key_distance)
    y = keys["Z"]["y"] + vertical_key_distance
    keys["control"] = {"x" : x, "y" : y}

    # map the space key
    x = keys["B"]["x"]
    y = keys["B"]["y"] + vertical_key_distance
    keys[" "] = {"x" : x, "y" : y}
    keys["space"] = {"x" : x, "y" : y}

    # map the enter key
    x = keys["L"]["x"] + (3 * horizontal_key_distance)
    y = keys["L"]["y"]
    keys["enter"] = {"x" : x, "y" : y}

    # map the hm (home) key
    x = keys["]"]["x"] + (4 * horizontal_key_distance)
    y = keys["="]["y"]
    keys["hm"] = {"x" : x, "y" : y}
    keys["home"] = {"x" : x, "y" : y}

    # map the delete key
    x = keys["home"]["x"] - horizontal_key_distance
    y = keys["["]["y"]
    keys["delete"] = {"x" : x, "y": y}

    # map the end key
    x = keys["home"]["x"]
    y = keys["P"]["y"]
    keys["end"] = {"x" : x, "y" : y}

    # map up, down, left and right keys
    # up
    x = keys["home"]["x"]
    y = keys["M"]["y"]
    keys["up"] = {"x" : x, "y" : y}
    # left
    x = keys["up"]["x"] - horizontal_key_distance
    y = keys["space"]["y"]
    keys["left"] = {"x" : x, "y" : y}
    # down
    x = keys["up"]["x"]
    y = keys["space"]["y"]
    keys["down"] = {"x" : x, "y" : y}
    # right
    x = keys["down"]["x"] + horizontal_key_distance
    y = keys["space"]["y"]
    keys["right"] = {"x" : x, "y" : y}

    return
# ====================================================================================================
# Read all the coordinate information:
# save_x, save_y (x and y coordinates of the SAVE button at the top of the screen)
# plus_x, plus_y (x and y coordinates of the plus button at the top left of the
#                 input cells at the bottom of the screen)
# input_x, input_y (x and y coordinates of the text line where you search for
#                   a participant in the McLeans system)
# ====================================================================================================
def read_coordinate_information():

    global save_x
    global save_y
    global plus_x
    global plus_y
    global input_x
    global input_y
    global keyboard_q_x
    global keyboard_q_y
    global letter_delay

    save_x = save_x_text_box.get("1.0", END)
    save_x = int(save_x.strip())
    print('save_x =', save_x)
    save_y = save_y_text_box.get("1.0", END)
    save_y = int(save_y.strip())
    print('save_y =', save_y)

    plus_x = plus_x_text_box.get("1.0", END)
    plus_x = int(plus_x.strip())
    print('plus_x =', plus_x)

    plus_y = plus_y_text_box.get("1.0", END)
    plus_y = int(plus_y.strip())
    print('plus_y =', plus_y)

    input_x = input_x_text_box.get("1.0", END)
    input_x = int(input_x.strip())
    print('input_x =', input_x)

    input_y = input_y_text_box.get("1.0", END)
    input_y = int(input_y.strip())
    print('input_y =', input_y)

    keyboard_q_x = keyboard_q_key_x_text_box.get("1.0", END)
    keyboard_q_x = int(keyboard_q_x.strip())
    print('keyboard_q_x =', keyboard_q_x)

    keyboard_q_y = keyboard_q_key_y_text_box.get("1.0", END)
    keyboard_q_y = int(keyboard_q_y.strip())
    print('keyboard_q_y =', keyboard_q_y)

    letter_delay = letter_delay_text_box.get("1.0", END)
    letter_delay = float(letter_delay.strip())
    print('letter_delay =', letter_delay)

    return
# ====================================================================================================
# Type text by using pyautogui to click on the windows accessibility onscreen
# keyboard. In between each character, pause pause_between_letters seconds
def kb_type(text):

    for character in text:
        if character.upper() in keys.keys():
            x = keys[character.upper()]["x"]
            y = keys[character.upper()]["y"]
            # if uppercase character, press shift first
            if (character.upper() == character) and character.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                kb_press("shift")
            pyautogui.click(x, y)
            time.sleep(letter_delay)

    return
# ====================================================================================================
# Press one or more special keys on the keyboard e.g. enter, up, down, shift etc.
# Accepts either a list of key strings or a single key string as parameters
# e.g. "up" or ["down", "right", "shift"]
def kb_press(key_param, pause_between_keys = 0.1):

    # if key_param is a string, get the x and y coordinate for the key and
    # pyautogui.click() it
    if isinstance(key_param, str):
        x = keys[key_param]["x"]
        y = keys[key_param]["y"]
        pyautogui.click(x, y)

    # if key_param is a list, loop through each key in the list, look up its
    # x and y coordinates and pyautogui.click() it, pausing pause_between_keys
    # seconds between keys
    if isinstance(key_param, list):
        for key in key_param:
            x = keys[key]["x"]
            y = keys[key]["y"]
            pyautogui.click(x, y)
            time.sleep(pause_between_keys)

    return
# ====================================================================================================
# Loop through the lines in csv_data_text_box
# Swop first and last names along commas
# e.g. Change "Woods,Tiger" to "Tiger,Woods" etc.
# ====================================================================================================
def swop_names_along_commas():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get the participants from the csv_data_text_box
    text = csv_data_text_box.get("1.0", END)

    # test print
    print(text)

    text = text.strip()
    lines = text.split("\n")

    swopped_lines = []
    for line in lines:
        line = line.strip()
        if ',' in line:
            comma_loc = line.find(',')
            first_bit = line[:comma_loc].strip()
            second_bit = line[comma_loc + 1:].strip()
            rebuilt_line = second_bit + ', ' + first_bit
            rebuilt_line = rebuilt_line.strip()
            swopped_lines.append(rebuilt_line)
    lines = swopped_lines

    new_text = "\n".join(lines)

    # delete old text, insert new text
    csv_data_text_box.delete(1.0, END)
    csv_data_text_box.insert(END, new_text)

    return
# ====================================================================================================
# Loop through participants. For each participant, search for it in the participant search area in
# the mcleans system, then press down, then enter to enter it. After processing all participants,
# press the save button in the mcleans system.
# ====================================================================================================
def find_and_enter_participants():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get the participants from the csv_data_text_box
    text = csv_data_text_box.get("1.0", END)
    text = text.strip()
    lines = text.split("\n")

    # click on the participant search box
    pyautogui.click(input_x, input_y)
    time.sleep(5)

    # 1. Loop through participants. For each:
    #    1. Type the name into the participant search box
    #    2. Press down
    #    3. Press enter
    # 2. Finally, click the save button
    total_participants = len(lines)
    for count in range(total_participants):
        line = lines[count]
        line = line.strip()
        # build the status text for the two line status Text widget
        # It will be in the form@
        # Woods, Tiger
        # 15/23 - 63.2% complete
        status_text = line + "\n" + str(count + 1) + '/' + str(total_participants) + ' - '
        if count + 1 < total_participants:
            percentage = float(count) / (float(total_participants) / 100.0)
            percentage = str(round(percentage, 1))
        else:
            percentage = "100"
        status_text += percentage + "%"
        # set text in status_text_box to status_text
        status_text_box.delete('1.0', END)
        status_text_box.insert('1.0', status_text)        
        kb_type(line)
        time.sleep(0.2)
        root.update_idletasks()
        kb_press('down')
        time.sleep(0.2)
        kb_press('enter')
        time.sleep(0.2)
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Click the top left blank cell, then loop through participants.
# For each participant, type it in, then press down.
# If we're at the final participant, press up instead of down after typing it in.
# Then press the save button. Job done.
# ====================================================================================================
def type_participants_in():

    # read coordinates information for the keys we need and map the windows onscreen accessibility
    # keyboard
    read_coordinate_information()
    map_keys()

    # get the participants from the csv_data_text_box
    text = csv_data_text_box.get("1.0", END)
    text = text.strip()
    lines = text.split("\n")

    # click on the top left empty cell, which is located at
    # (plus_x + 32, plus_y + 18)
    pyautogui.click(plus_x + 32, plus_y + 18)

    # type a bunch of test lines to get the focus on the target window
    type_test_lines() # NEW 6/2/17 AT 19:06

    # 1. Loop through participants; for each:
    #     1. Type the participant name
    #     2. If we're NOT at the last participant, press down, else press up
    # 2. Finally, click the save button
    total_participants = len(lines)
    for count in range(total_participants):
        line = lines[count]
        line = line.strip()
        # build the status text for the two line status Text widget
        # It will be in the form:
        # Woods, Tiger
        # 15/23 - 63.2% complete
        status_text = line + "\n" + str(count + 1) + '/' + str(total_participants) + ' - '
        if count + 1 < total_participants:
            percentage = float(count) / (float(total_participants) / 100.0)
            percentage = str(round(percentage, 1))
        else:
            percentage = "100"
        status_text += percentage + "%"
        # set text in status_text_box to status_text
        status_text_box.delete('1.0', END)
        status_text_box.insert('1.0', status_text)
        kb_type(line)
        root.update_idletasks()
        if count + 1 != total_participants:
            kb_press('down')
        else:
            kb_press('up')
    pyautogui.click(save_x, save_y)

    return
# ====================================================================================================
# Type a bunch of test lines; used to get the focus onto the remote desktop window as there is
# sometimes a delay before the remote window reacts to actions initiated by the pyautogui library
# ====================================================================================================
def type_test_lines():

    direction = 0
    for count in range(4):
        kb_type("test test")
        time.sleep(0.2)
        if direction == 0:
            kb_press('down')
        else:
            kb_press('up')
            kb_press('up')
        direction = 1 - direction

    kb_press('up')
    time.sleep(0.5)
    kb_press('up')
    
    return
# ====================================================================================================
# Set up the interface
# Basic window
root = Tk()
root.wm_title("Participant Blaster (Amelyn Technologies 2016)")

# Frame to hold the four X and Y coordinates the program requires.
# We're going to grid the six coordinates and their labels into the xy_frame,
# then grid the xy_frame in the root
xy_frame = ttk.Frame(root)

# Set up x and y coordinate Text boxes and their labels, grid them into xy_frame
save_x_label = Label(xy_frame, text="Save X")
save_x_label.grid(row=0, column=0, sticky=E)
save_x_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
save_x_text_box.grid(row=0, column=1)

save_y_label = Label(xy_frame, text="Save Y")
save_y_label.grid(row=0, column=2, sticky=E)
save_y_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
save_y_text_box.grid(row=0, column=3)

input_x_label = Label(xy_frame, text="Input X")
input_x_label.grid(row=1, column=0, sticky=E)
input_x_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
input_x_text_box.grid(row=1, column=1)

input_y_label = Label(xy_frame, text="Input Y")
input_y_label.grid(row=1, column=2, sticky=E)
input_y_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
input_y_text_box.grid(row=1, column=3)

plus_x_label = Label(xy_frame, text="+ X")
plus_x_label.grid(row=2, column=0, sticky=E)
plus_x_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
plus_x_text_box.grid(row=2, column=1)

plus_y_label = Label(xy_frame, text="+ Y")
plus_y_label.grid(row=2, column=2, sticky=E)
plus_y_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
plus_y_text_box.grid(row=2, column=3)

keyboard_q_key_x_label = Label(xy_frame, text="kb Q X")
keyboard_q_key_x_label.grid(row=3, column=0, sticky=E)
keyboard_q_key_x_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
keyboard_q_key_x_text_box.grid(row=3, column=1)

keyboard_q_key_y_label = Label(xy_frame, text="kb Q Y")
keyboard_q_key_y_label.grid(row=3, column=2, sticky=E)
keyboard_q_key_y_text_box = Text(xy_frame, width=5, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
keyboard_q_key_y_text_box.grid(row=3, column=3)

# Set up Swop Names Along Comma button, grid it into xy_frame
comma_swop_button = ttk.Button(xy_frame, text='Swop Names Along Commas',
                                    command=swop_names_along_commas)
comma_swop_button.grid(row=0, column=4, sticky=EW)

# Set up Find and Enter button for finding and entering participants
button_text = 'Find and Enter Participants'
find_and_enter_participants_button = ttk.Button(xy_frame, text=button_text,
                                                    command=find_and_enter_participants)
find_and_enter_participants_button.grid(row=1, column=4, sticky=EW)

# Set up Type In button for typing all the participants into blank cells
button_text = 'Type Participants Into Blank Cells'
type_participants_in_button = ttk.Button(xy_frame, text=button_text,
                                                    command=type_participants_in)
type_participants_in_button.grid(row=2, column=4, sticky=EW)

# Create frame to hold the Letter Delay label and the Text widget for the user to enter the
# Letter Delay
letter_delay_frame = ttk.Frame(xy_frame)
# Create letter delay label and letter delay text widget and grid them into the letter_delay_frame
letter_delay_label = Label(letter_delay_frame, text="Letter Delay")
letter_delay_label.grid(row=0, column=0, sticky=E)
letter_delay_text_box = Text(letter_delay_frame, width=5, height=1, background='#000000',
                             foreground='#FFFF00', font=('Courier', 12, 'bold'))
letter_delay_text_box.grid(row=0, column=1, sticky=E)
# Grid the letter_delay_frame onto root
letter_delay_frame.grid(row=3, column=4, sticky=E)

# Grid xy_frame into root
xy_frame.grid(row=0, column=0, sticky=W)

# Create status label and single line Text widget to display information about the participant
# currently beining entered (participant, X of Y for the participant in the current list and
# percentage of list entered so far
status_label = Label(root, text="Status")
status_label.grid(row=1, column=0, sticky=W)
status_text_box = Text(root, width=42, height=2, background='#000000', foreground='#FFFF00',
                font=('Courier', 12, 'bold'))
status_text_box.grid(row=2, column=0, sticky=W)

# Create CSV data label
paste_csv_data_label = Label(root, text="Paste CSV data here")
paste_csv_data_label.grid(row=3, column=0, sticky=W)


# Create frame to hold the csv_data_text_box
csv_data_frame = ttk.Frame(root)

# create csv_data_text_box
# OLD:
# csv_data_text_box = Text(root, width=42, height=30, background='#000000', foreground='#FFFF00',
#                          font=('Courier', 12, 'bold'))
# csv_data_text_box.grid(row=4, column=0, sticky=W)
# NEW:
csv_data_text_box = Text(csv_data_frame, width=41, height=30, background='#000000', foreground='#FFFF00',
                          font=('Courier', 12, 'bold'))
csv_data_text_box.pack(side=LEFT)
# create scrollbar, pack it into csv_data_text_box
scrollbar = Scrollbar(csv_data_frame)
scrollbar.pack(side=RIGHT, fill=Y)
# attach scrollbar to csv_data_text_box to each other
csv_data_text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=csv_data_text_box.yview)

# grid the csv_data_frame
csv_data_frame.grid(row=4, column=0, sticky=W)


# Start 'er up!
root.mainloop()
