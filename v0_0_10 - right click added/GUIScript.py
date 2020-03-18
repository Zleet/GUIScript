# ====================================================================================================
# GUIScript
# A small scripting language for GUI automation, built on top of Python 3 and Pyautogui
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
letter_delay = 0.06

# make the settings_window global so that it can be referenced from both
# display_settings_window() and save_settings()
settings_window = -1

# let's make the widgets in the settings window global so that we can reference them from
# both display_settings_window() and save_settings()
keyboard_q_x_text_box = -1
keyboard_q_y_text_box = -1

# make click_locations global so that it can be referenced from read_click_locations()
# and execute_press_command()
click_locations = -1

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

# data read from the DATA text widget. It's in list form, one item per line
data = []

# index of current data item; incremented as data is read
current_data_index = 0 # start at item number one
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
    horizontal_key_distance = 41    # updated for Madrid servers 22/9/17
    vertical_key_distance = 39      # updated for Madrid servers 22/9/17

    # map the number row plus the three rows of letters
    letter_rows = ['Z1234567890-=', 'qwertyuiop[]', "asdfghjkl;'#", 'zxcvbnm,./'] # ignore initial Z kludge (22/8/17)
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
    x = keys["Z"]["x"] - (horizontal_key_distance * 2)
    y = keys["Z"]["y"]
    keys["shift"] = {"x" : x, "y" : y}

    # map the control key on the bottom left of the onscreen keyboard
    x = keys["Z"]["x"] - (3 * horizontal_key_distance)
    y = keys["Z"]["y"] + vertical_key_distance
    keys["control"] = {"x" : x, "y" : y}

    # map the space key
    x = keys["B"]["x"]
    y = keys["B"]["y"] + vertical_key_distance
    keys[" "] = {"x" : x, "y" : y}
    keys["space"] = {"x" : x, "y" : y}

    # map the enter key
    x = keys["P"]["x"] + (4 * horizontal_key_distance)
    y = keys["P"]["y"]
    keys["enter"] = {"x" : x, "y" : y}

    # map the hm (home) key
    x = keys["]"]["x"] + (4 * horizontal_key_distance)
    y = keys["="]["y"] - vertical_key_distance
    keys["hm"] = {"x" : x, "y" : y}
    keys["home"] = {"x" : x, "y" : y}

    # map the delete key
    x = keys["="]["x"] + horizontal_key_distance
    y = keys["="]["y"]
    keys["delete"] = {"x" : x, "y": y}

    # map the end key
    x = keys["home"]["x"]
    y = keys["P"]["y"]
    keys["end"] = {"x" : x, "y" : y}

    # map up, down, left and right keys
    # up
    x = keys["]"]["x"] + (horizontal_key_distance * 1.5)
    y = keys["N"]["y"]
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
            # print('x =', x)
            # print('y =', y)
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
# Called when the RUN button is pressed; run the script the user has entered into the GUIScript
# GUI.
# ====================================================================================================
def guiscript_run():

    # map the keys on the windows onscreen keyboard
    map_keys()

    # read pre-loop lines
    text = pre_loop_text_box.get("1.0", END).strip()
    pre_loop_lines = text.split("\n")
    pre_loop_lines = adios_whitespace_lines_and_comment_lines(pre_loop_lines)

    # read main loop lines
    text = main_loop_text_box.get("1.0", END).strip()
    main_loop_lines = text.split("\n")
    main_loop_lines = adios_whitespace_lines_and_comment_lines(main_loop_lines)

    # read post-loop lines
    text = post_loop_text_box.get("1.0", END).strip()
    post_loop_lines = text.split("\n")
    post_loop_lines = adios_whitespace_lines_and_comment_lines(post_loop_lines)

    # read total_loops
    text = total_loops_text_box.get("1.0", END).strip()
    # if the user hasn't entered a value for total loops, run the main loop once
    if len(text) == 0:
        total_loops = 1
    else:
        total_loops = int(text)

    # lines = pre-loop lines + (total_loops * main loop lines) + post-loop lines
    lines = pre_loop_lines
    for count in range(total_loops):
        lines.extend(main_loop_lines)
    lines.extend(post_loop_lines)

    # read subroutine #1 lines
    text = subroutine_1_text_box.get("1.0", END).strip()
    sub1_lines = text.split("\n")
    sub1_lines = adios_whitespace_lines_and_comment_lines(sub1_lines)

    # read subroutine #2 lines
    text = subroutine_2_text_box.get("1.0", END).strip()
    sub2_lines = text.split("\n")
    sub2_lines = adios_whitespace_lines_and_comment_lines(sub2_lines)

    # read subroutine #3 lines
    text = subroutine_3_text_box.get("1.0", END).strip()
    sub3_lines = text.split("\n")
    sub3_lines = adios_whitespace_lines_and_comment_lines(sub3_lines)

    # replace all subroutine calls with the relevant lines
    # e.g. replace the line "sub1" with the lines for subroutine #1 etc.
    new_lines = []
    for line in lines:
        is_subroutine_line = 0
        if ((line.strip() == 'sub1') or (line.strip() == 'sub2')) or line.strip() == 'sub3':
            is_subroutine_line = 1
        if is_subroutine_line:
            if line.strip() == 'sub1':
                for inner_line in sub1_lines:
                    new_lines.append(inner_line)
            if line.strip() == 'sub2':
                for inner_line in sub2_lines:
                    new_lines.append(inner_line)
            if line.strip() == 'sub3':
                for inner_line in sub3_lines:
                    new_lines.append(inner_line)
        else:
            new_lines.append(line)
    lines = new_lines
    
    # read data
    read_data()

    # read click locations
    click_locations = read_click_locations()

    # loop through all the lines and process them, one by one
    # Possible commands are:
    # click x, y
    # click save_button
    # type "text to type"
    # pause 0.5 # pause 0.5 seconds
    # press up
    for line in lines:
        process_line(line)

    return
# ====================================================================================================
# Process a single GUIScript line
# Possible commands/line formats are:
# click x, y
# click save_button
# type "text to type"
# pause 0.5 # pause 0.5 seconds
# press "up"
#
# Here we'll determine what command the line represents and pass it off to the relevant function
# ====================================================================================================
def process_line(line):

    line = line.strip()

    # if the line has a comment at the end of it, remove the comment
    if '#' in line:
        hash_loc = line.find('#')
        line = line[:hash_loc].strip()
    
    space_loc = line.find(' ')
    first_word = line[:space_loc].lower()
    # determine command
    if line == 'data increment':
        data_index_increment()
    if line == 'data_decrement':
        data_index_decrement()
    if first_word == 'click':
        execute_click_command(line)
    if first_word == 'right_click':         # added 8/5/19
        execute_right_click_command(line)
    if first_word == 'pause':
        execute_pause_command(line)
    if first_word == 'press':
        execute_press_command(line)
    if first_word == 'type':
        execute_type_command(line)

    return
# ====================================================================================================
# Execute a click command. A command in the format:
# click x_coordinate, y_coordinate
# e.g.
# click 345, 746
# ====================================================================================================
def execute_click_command(line):

    line = line.strip()
    space_loc = line.find(' ')
    last_bit_of_line = line[space_loc + 1:].strip()

    # if there's a comma in last_big_of_line, the click command is in the format:
    # click 345, 746
    # otherwise it's in the format:
    # click top_left_cell
    # and the coordinates for the click location need to be looked up in the global
    # dictionary click_locations
    if ',' in last_bit_of_line:
        coord_strings = last_bit_of_line.split(',')
        x = int(coord_strings[0].strip())
        y = int(coord_strings[1].strip())
    else:
        # 1. read click locations
        # 2. look up coordinates of the click location
        read_click_locations()
        print('click_locations:')
        print(click_locations)
        x = 1 # default
        y = 1 # default
        for click_location in click_locations:
            if click_location["name"].lower() == last_bit_of_line.lower():
                x = click_location["x"]
                y = click_location["y"]

    pyautogui.click(x, y)

    return
# ====================================================================================================
# Execute a click command. A command in the format:
# right_click x_coordinate, y_coordinate
# e.g.
# click 345, 746
# ====================================================================================================
def execute_right_click_command(line):

    line = line.strip()
    space_loc = line.find(' ')
    last_bit_of_line = line[space_loc + 1:].strip()

    # if there's a comma in last_big_of_line, the right click command is in the format:
    # right_click 345, 746
    # otherwise it's in the format:
    # right_click top_left_cell
    # and the coordinates for the click location need to be looked up in the global
    # dictionary click_locations
    if ',' in last_bit_of_line:
        coord_strings = last_bit_of_line.split(',')
        x = int(coord_strings[0].strip())
        y = int(coord_strings[1].strip())
    else:
        # 1. read click locations
        # 2. look up coordinates of the click location
        read_click_locations()
        print('click_locations:')
        print(click_locations)
        x = 1 # default
        y = 1 # default
        for click_location in click_locations:
            if click_location["name"].lower() == last_bit_of_line.lower():
                x = click_location["x"]
                y = click_location["y"]

    pyautogui.moveTo(x, y)
    time.sleep(0.5)
    pyautogui.click(button='right')

    return
# ====================================================================================================
# Execute a pause command. A command in the format:
# pause <time_in_seconds>
# e.g.
# pause 0.5
# (pause half a second)
# ====================================================================================================
def execute_pause_command(line):

    line = line.strip()

    space_loc = line.find(' ')
    rest_of_line = line[space_loc + 1:].strip()
    pause_time = float(rest_of_line.strip())

    time.sleep(pause_time)

    return
# ====================================================================================================
# Execute a press command. A command in the format:
# press <button>
# e.g.
# press down
# or
# press left
# ====================================================================================================
def execute_press_command(line):

    line = line.strip()

    space_loc = line.find(' ')
    rest_of_line = line[space_loc + 1:].strip()

    # loop through the list click_locations and make a new list containing all the click location
    # names
    click_location_names = []
    for click_location_dictionary in click_locations:
        click_location_name = click_location_dictionary["name"]
        click_location_names.append(click_location_name)

    # If the user has entered a click location name (e.g. "save_button" or "next_market" etc.)
    # after the word "press":
    #   1. look up the coordinates for the click location
    #   2. pyautogui.click() the coordinates
    # otherwise:
    #   kb_press(rest_of_line)
    if rest_of_line in click_location_names:
        # get coordinates of click location
        for click_location_dictionary in click_locations:
            if click_location_dictionary["name"].lower() == rest_of_line.lower():
                x = click_location_dictionary["x"]
                y = click_location_dictionary["y"]
                break
        # pyautogui.click() the coordinates of the click location
        pyautogui.click(x, y)
    else:
        kb_press(rest_of_line)

    return
# ====================================================================================================
# Execute a type command. A command in the format:
# type "string"
# where the string is enclosed by double quotes
# e.g.
# Type "Weekend Football"
# or
# type ""
#
# If the command is "type data", type the current data item in the global list data[current_data_index]
# ====================================================================================================
def execute_type_command(line):

    line = line.strip()

    space_loc = line.find(' ')
    rest_of_line = line[space_loc + 1:].strip()

    if rest_of_line.lower() == 'data':
        global data
        global current_data_index
        kb_type(data[current_data_index])
    else:
        kb_type(rest_of_line)

    return
# ====================================================================================================
# Read the click locations. Each click location should be a line in the format:
# <click_location_name> <x_coordinate>, <y_coordinate>
# e.g.
# save_button 123, 675
#
# For each click location, create a click location dictionary in the form:
# {
#   "name"  : "save_button",
#   "x"     : 456,
#   "y"     : 942
# }
# Append all the click location dictionaries onto a list named click_locations
# ====================================================================================================
def read_click_locations():

    global click_locations

    # get the text from the click_locations_text_box
    text = click_locations_text_box.get("1.0", END).strip()
    lines = text.split("\n")
    lines = adios_whitespace_lines_and_comment_lines(lines)

    # parse the click locations
    click_locations = []
    for line in lines:
        space_location = line.find(' ')
        name = line[:space_location]
        rest_of_line = line[space_location:].strip()
        coord_strings = rest_of_line.split(',')
        x = int(coord_strings[0].strip())
        y = int(coord_strings[1].strip())
        click_location_dictionary = {
                                "name"  : name,
                                "x"     : x,
                                "y"     : y
                                    }
        click_locations.append(click_location_dictionary)

    # test print
    for click_location_dictionary in click_locations:
        print(click_location_dictionary)

    return click_locations
# ====================================================================================================
# Passed a list of lines, this function filters out whitespace lines and comment lines (i.e. lines that
# begin with #) then returns a list containing all the other lines
# ====================================================================================================
def adios_whitespace_lines_and_comment_lines(lines):

    kept_lines = []

    for line in lines:
        line = line.strip()
        if (len(line) > 0) and (line[0] != '#'):
            kept_lines.append(line)

    return kept_lines
# ====================================================================================================
# Called when the LOAD SCRIPT button is pressed. Prompts the user to select a GUIScript script
# to load from the Open File dialogue.
# ====================================================================================================
def load_script():

    # prompt the user for a file from which to read the script
    infile = filedialog.askopenfile(mode='r')

    # read the script from the file the user has specified
    guiscript = infile.read()
    infile.close()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # parse the script; place all relevant texts in the appropriate Text widgets
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # extract pre-loop text, place it in the pre_loop_text_box Text widget
    text = extract_substring(guiscript, '<pre_loop>', '</pre_loop>').strip()
    pre_loop_text_box.delete(1.0, END) # delete old text
    pre_loop_text_box.insert(END, text) # insert new text
    
    # extract main-loop text, place it in the main_loop_text_box Text widget
    text = extract_substring(guiscript, '<main_loop>', '</main_loop>').strip()
    main_loop_text_box.delete(1.0, END) # delete old text
    main_loop_text_box.insert(END, text) # insert new text

    # extract post-loop text, place it in the post_loop_text_box Text widget
    text = extract_substring(guiscript, '<post_loop>', '</post_loop>').strip()
    post_loop_text_box.delete(1.0, END) # delete old text
    post_loop_text_box.insert(END, text) # insert new text

    # extract click locations text, place it in the click_locations_text_box Text widget
    text = extract_substring(guiscript, '<click_locations>', '</click_locations>').strip()
    click_locations_text_box.delete(1.0, END) # delete old text
    click_locations_text_box.insert(END, text) # insert new text

    # extract data text, place it in the data_text_box Text widget
    text = extract_substring(guiscript, '<data>', '</data>').strip()
    data_text_box.delete(1.0, END) # delete old text
    data_text_box.insert(END, text) # insert new text

    # extract notes text, place it in the notes_text_box Text widget
    text = extract_substring(guiscript, '<notes>', '</notes>').strip()
    notes_text_box.delete(1.0, END) # delete old text
    notes_text_box.insert(END, text) # insert new text

    # extract subroutine #1 text, place it in the subroutine_1_text_box Text widget
    text = extract_substring(guiscript, '<subroutine_1>', '</subroutine_1>').strip()
    subroutine_1_text_box.delete(1.0, END) # delete old text
    subroutine_1_text_box.insert(END, text) # insert new text

    # extract subroutine #2 text, place it in the subroutine_2_text_box Text widget
    text = extract_substring(guiscript, '<subroutine_2>', '</subroutine_2>').strip()
    subroutine_2_text_box.delete(1.0, END) # delete old text
    subroutine_2_text_box.insert(END, text) # insert new text

    # extract subroutine #3 text, place it in the subroutine_3_text_box Text widget
    text = extract_substring(guiscript, '<subroutine_3>', '</subroutine_3>').strip()
    subroutine_3_text_box.delete(1.0, END) # delete old text
    subroutine_3_text_box.insert(END, text) # insert new text

    # extract total loops text, place it in the total_loops_text_box Text widget
    text = extract_substring(guiscript, '<total_loops>', '</total_loops>').strip()
    total_loops_text_box.delete(1.0, END) # delete old text
    total_loops_text_box.insert(END, text) # insert new text

    return
# ====================================================================================================
# Helper function; returns the substring in big_string that is located between string_1 and string_2
# Doesn't include string_1 or string_2 in the substring returned.
# ====================================================================================================
def extract_substring(big_string, string_1, string_2):

    # sanity test #1; if either string_1 or string_2 are not located in big_string, return an empty string
    if (not string_1 in big_string) or (not string_2 in big_string):
        return ''

    # sanity test #2; if string_2 is located earlier than string_1 in big_string, return an empty string
    if big_string.find(string_2) < big_string.find(string_1):
        return ''

    # if we've fallen through, extract the substring and return it already
    start = big_string.find(string_1) + len(string_1)
    big_string = big_string[start:]
    end = big_string.find(string_2)
    the_substring = big_string[:end]

    return the_substring
# ====================================================================================================
# Called when the SAVE SCRIPT button is pressed. Prompts the user for a filename to save the GUIScript
# script.
# ====================================================================================================
def save_script():

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # First, let's get all the text from all the Text widgets and built a big text string, enclosing
    # the chunk of text from each Text widget in an appropriate pair of tags.
    # The text from the click_locations_text_box, for example, will be enclosed in the tags
    # <click_locations> and </click_locations>
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    big_string = ''

    # get pre-loop text, wrap it in tags, append it to big_string
    text = pre_loop_text_box.get("1.0", END).strip()
    big_string += '<pre_loop>\n' + text + '\n</pre_loop>\n\n'

    # get main loop text, wrap it in tags, append it to big_string
    text = main_loop_text_box.get("1.0", END).strip()
    big_string += '<main_loop>\n' + text + '\n</main_loop>\n\n'

    # get post loop text, wrap it in tags, append it to big_string
    text = post_loop_text_box.get("1.0", END).strip()
    big_string += '<post_loop>\n' + text + '\n</post_loop>\n\n'

    # get click locations text, wrap it in tags, append it to big_string
    text = click_locations_text_box.get("1.0", END).strip()
    big_string += '<click_locations>\n' + text + '\n</click_locations>\n\n'

    # get data text, wrap it in tags, append it to big_string
    text = data_text_box.get("1.0", END).strip()
    big_string += '<data>\n' + text + '\n</data>\n\n'

    # get notes text, wrap it in tags, append it to big_string
    text = notes_text_box.get("1.0", END).strip()
    big_string += '<notes>\n' + text + '\n</notes>\n\n'

    # get subroutine #1 text, wrap it in tags, append it to big_string
    text = subroutine_1_text_box.get("1.0", END).strip()
    big_string += '<subroutine_1>\n' + text + '\n</subroutine_1>\n\n'

    # get subroutine #2 text, wrap it in tags, append it to big_string
    text = subroutine_2_text_box.get("1.0", END).strip()
    big_string += '<subroutine_2>\n' + text + '\n</subroutine_2>\n\n'

    # get subroutine #3 text, wrap it, append it to big_string
    text = subroutine_3_text_box.get("1.0", END).strip()
    big_string += '<subroutine_3>\n' + text + '\n</subroutine_3>\n\n'

    # get total_loops, wrap it, append it to big_string
    text = total_loops_text_box.get("1.0", END).strip()
    big_string += '<total_loops>\n' + text + '\n</total_loops>\n\n'

    # prompt the user for a filename under which to save the script
    outfile = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if outfile == None:
        return
    else:
        outfile.write(big_string)
        outfile.close()

    return
# ====================================================================================================
# Display the settings window. This will contain two Text widgets in which the user can enter the
# X and Y coordinates of the letter Q on the virtual keyboard. (This will be used by the program
# to map all of the remaining keys on the virtual keyboard)
#
# The settings window will be laid out like this:
#
#                        X            Y
#   Keyboard Q    <Text widget> <Text widget>
#
#                 <Save button>
# ====================================================================================================
def display_settings_window():

    global settings_window

    global keyboard_q_x_text_box
    global keyboard_q_y_text_box

    # create a new settings window
    settings_window = Toplevel()
    settings_window.wm_title("Settings")

    # frame to hold the widgets in the settings window
    settings_frame = ttk.Frame(settings_window)

    # Set up X and Y labels and grid them onto settings_frame
    x_label = Label(settings_frame, text="X")
    x_label.grid(row=0, column=1)
    y_label = Label(settings_frame, text="Y")
    y_label.grid(row=0, column=2)

    # Set up Keyboard Q label, grid it onto settings_frame
    keyboard_q_label = Label(settings_frame, text="Keyboard Q")
    keyboard_q_label.grid(row=1, column=0)

    # Set up keyboard_q_x_text widget and keyboard_q_y text widget, grid them onto settings_frame
    keyboard_q_x_text_box = Text(settings_frame, width=6, height=1, background='#000000',
                             foreground='#FFFF00', font=('Courier', 10, 'bold'))
    keyboard_q_x_text_box.grid(row=1, column=1)
    keyboard_q_x_text_box.config(insertbackground="#FFFFFF")
    keyboard_q_y_text_box = Text(settings_frame, width=6, height=1, background='#000000',
                             foreground='#FFFF00', font=('Courier', 10, 'bold'))
    keyboard_q_y_text_box.grid(row=1, column=2)
    keyboard_q_y_text_box.config(insertbackground="#FFFFFF")

    # spacer label (blank) to separate the save button from the stuff above
    spacer_label = Label(settings_frame, text="")
    spacer_label.grid(row=2, column=0)

    # save button
    save_button = ttk.Button(settings_frame, text='SAVE', command=save_settings, width=6)
    save_button.grid(row=3, column=1, sticky=EW)

    # read settings from 'settings.txt'
    # They are in the form:
    # keyboard_q_x,<value>
    # keyboard_q_y,<value>
    #
    # For example:
    # keyboard_q_x,123
    # keyboard_q_y,1240
    infile = open('settings.txt', 'r')
    settings_lines = infile.readlines()
    infile.close()

    for line in settings_lines:
        line = line.strip()
        if 'keyboard_q_x' in line:
            elements = line.split(',')
            keyboard_q_x = int(elements[1])
        if 'keyboard_q_y' in line:
            elements = line.split(',')
            keyboard_q_y = int(elements[1])

    # populate keyboard_q_x_text_box and keyboard_q_y_text_box with the settings we've just read
    keyboard_q_x_text_box.delete(1.0, END)          # delete old text
    keyboard_q_x_text_box.insert(END, keyboard_q_x) # insert new text
    keyboard_q_y_text_box.delete(1.0, END)          # delete old text
    keyboard_q_y_text_box.insert(END, keyboard_q_y) # insert new text

    # grid the settings frame
    settings_frame.grid(row=0, column=0, sticky=W)

    return
# ====================================================================================================
# Called when the SAVE button in the settings window is pressed; saves the settings (surprisingly!!!)
# ====================================================================================================
def save_settings():

    global keyboard_q_x
    global keyboard_q_y

    # read keyboard_q_x from keyboard_q_x_text_box
    text = keyboard_q_x_text_box.get("1.0", END).strip()
    keyboard_q_x = int(text)
        
    # read keyboard_q_y from keyboard_q_y_text_box
    text = keyboard_q_y_text_box.get("1.0", END).strip()
    keyboard_q_y = int(text)

    # write both values to the file 'settings.txt'
    #
    # Format will be:
    # keyboard_q_x,<value>
    # keyboard_q_y,<value>
    #
    # For example:
    # keyboard_q_x,123
    # keyboard_q_y,1240
    settings_text = 'keyboard_q_x,' + str(keyboard_q_x) + "\n"
    settings_text += 'keyboard_q_y,' + str(keyboard_q_y)
    outfile = open('settings.txt', 'w')
    outfile.write(settings_text)
    outfile.close()

    # close the settings_window
    settings_window.destroy()

    return
# ====================================================================================================
# Read the data from the DATA text widget. Stick it in the data global list, one item per line of data.
# ====================================================================================================
def read_data():

    text = data_text_box.get("1.0", END).strip()
    lines = text.split("\n")
    lines = adios_whitespace_lines_and_comment_lines(lines)

    # remove comments from the end of data lines
    decommented_lines = []
    for line in lines:
        if '#' in line:
            hash_pos = line.find('#')
            line = line[:hash_pos].strip()
        decommented_lines.append(line)

    global data
    data = decommented_lines
    
    global current_data_index
    current_data_index = 0

    return
# ====================================================================================================
# Increment the global current_data_index. If it's incremented past the end of the global data list,
# loop around and reset it to zero
# ====================================================================================================
def data_index_increment():

    global current_data_index
    current_data_index += 1

    global data

    if (current_data_index == len(data)):
        current_data_index = 0

    return
# ====================================================================================================
# Decrement the global current_data_index. If it's decremented past zero, set it to len(data) - 1
# i.e. the index of the last item in the global data list
# ====================================================================================================
def data_index_decrement():

    global current_data_index
    current_data_index -= 1

    global data

    if (current_data_index < 0):
        current_data_index = len(data) - 1

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 1
# ==============================================================================
def set_total_loops_to_1():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "1")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 2
# ==============================================================================
def set_total_loops_to_2():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "2")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 3
# ==============================================================================
def set_total_loops_to_3():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "3")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 4
# ==============================================================================
def set_total_loops_to_4():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "4")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 5
# ==============================================================================
def set_total_loops_to_5():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "5")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 6
# ==============================================================================
def set_total_loops_to_6():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "6")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 7
# ==============================================================================
def set_total_loops_to_7():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "7")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 8
# ==============================================================================
def set_total_loops_to_8():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "8")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 9
# ==============================================================================
def set_total_loops_to_9():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "9")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 10
# ==============================================================================
def set_total_loops_to_10():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "10")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 11
# ==============================================================================
def set_total_loops_to_11():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "11")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 12
# ==============================================================================
def set_total_loops_to_12():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "12")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 13
# ==============================================================================
def set_total_loops_to_13():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "13")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 14
# ==============================================================================
def set_total_loops_to_14():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "14")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 15
# ==============================================================================
def set_total_loops_to_15():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "15")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 16
# ==============================================================================
def set_total_loops_to_16():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "16")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 17
# ==============================================================================
def set_total_loops_to_17():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "17")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 18
# ==============================================================================
def set_total_loops_to_18():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "18")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 19
# ==============================================================================
def set_total_loops_to_19():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "19")

    return
# ==============================================================================
# Set the total loops in the total_loops_text_box to 20
# ==============================================================================
def set_total_loops_to_20():

    # clear out the text in the total loops text box
    total_loops_text_box.delete(1.0, END)

    # set the text in the total loops text box to total_loops
    total_loops_text_box.insert(END, "20")

    return
# ==============================================================================
# Activate small mode; make the main window smaller
# ==============================================================================
def activate_small_mode():

    pre_loop_label["width"] = 9
    pre_loop_text_box["width"] = 9
    pre_loop_text_box["height"] = 1

    main_loop_label["width"] = 9
    main_loop_text_box["width"] = 9
    main_loop_text_box["height"] = 1

    post_loop_label["width"] = 9
    post_loop_text_box["width"] = 9
    post_loop_text_box["height"] = 1

    click_locations_label["width"] = 9
    click_locations_text_box["width"] = 9
    click_locations_text_box["height"] = 1

    data_label["width"] = 9
    data_text_box["width"] = 9
    data_text_box["height"] = 1

    notes_label["width"] = 9
    notes_text_box["width"] = 9
    notes_text_box["height"] = 1

    subroutine_1_label["width"] = 9
    subroutine_1_text_box["width"] = 9
    subroutine_1_text_box["height"] = 1

    subroutine_2_label["width"] = 9
    subroutine_2_text_box["width"] = 9
    subroutine_2_text_box["height"] = 1

    subroutine_3_label["width"] = 9
    subroutine_3_text_box["width"] = 9
    subroutine_3_text_box["height"] = 1

    return
# ==============================================================================
# Activate large mode; make the main window larger
# ==============================================================================
def activate_large_mode():

    pre_loop_label["width"] = 30
    pre_loop_text_box["width"] = 30
    pre_loop_text_box["height"] = 5

    main_loop_label["width"] = 30
    main_loop_text_box["width"] = 30
    main_loop_text_box["height"] = 5

    post_loop_label["width"] = 30
    post_loop_text_box["width"] = 30
    post_loop_text_box["height"] = 5

    click_locations_label["width"] = 30
    click_locations_text_box["width"] = 30
    click_locations_text_box["height"] = 5

    data_label["width"] = 30
    data_text_box["width"] = 30
    data_text_box["height"] = 5

    notes_label["width"] = 30
    notes_text_box["width"] = 30
    notes_text_box["height"] = 5

    subroutine_1_label["width"] = 30
    subroutine_1_text_box["width"] = 30
    subroutine_1_text_box["height"] = 5

    subroutine_2_label["width"] = 30
    subroutine_2_text_box["width"] = 30
    subroutine_2_text_box["height"] = 5

    subroutine_3_label["width"] = 30
    subroutine_3_text_box["width"] = 30
    subroutine_3_text_box["height"] = 5

    return
# ==============================================================================
# Set up the interface
# Basic window
root = Tk()
root.wm_title("GUIScript (Amelyn Technologies 2017)")

# Frame to hold most of the widgets (3 x 3 text widgets and their accompanying labels)
xy_frame = ttk.Frame(root)

# Set up pre-loop label and text box and grid them into xy_frame
pre_loop_label = Label(xy_frame, text="PRE-LOOP (RUNS ONCE)")
pre_loop_label.grid(row=0, column=0, sticky=EW)
pre_loop_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
pre_loop_text_box.grid(row=1, column=0)
pre_loop_text_box.config(insertbackground="#FFFFFF")

# Set up main loop label and text box and grid them into xy_frame
main_loop_label = Label(xy_frame, text="MAIN LOOP (RUNS Total Loops TIMES)")
main_loop_label.grid(row=2, column=0, sticky=EW)
main_loop_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
main_loop_text_box.grid(row=3, column=0)
main_loop_text_box.config(insertbackground="#FFFFFF")

# Set up post-loop label and text box and grid them into xy_frame
post_loop_label = Label(xy_frame, text="POST LOOP (RUNS ONCE)")
post_loop_label.grid(row=4, column=0, sticky=EW)
post_loop_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
post_loop_text_box.grid(row=5, column=0)
post_loop_text_box.config(insertbackground="#FFFFFF")

# spacer label #1 to separate columns zero and 2
spacer_label_1 = Label(xy_frame, text="  ")
spacer_label_1.grid(row=1, column=1, sticky=EW)

# Set up click locations label and text box and grid them into xy_frame
click_locations_label = Label(xy_frame, text="CLICK LOCATIONS (name, x, y)")
click_locations_label.grid(row=0, column=2, sticky=EW)
click_locations_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
click_locations_text_box.grid(row=1, column=2)
click_locations_text_box.config(insertbackground="#FFFFFF")

# Set up data label and text box and grid them into xy_frame
data_label = Label(xy_frame, text="DATA")
data_label.grid(row=2, column=2, sticky=EW)
data_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
data_text_box.grid(row=3, column=2)
data_text_box.config(insertbackground="#FFFFFF")

# Set up notes label and text box and grid them into xy_frame
notes_label = Label(xy_frame, text="NOTES")
notes_label.grid(row=4, column=2, sticky=EW)
notes_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
notes_text_box.grid(row=5, column=2)
notes_text_box.config(insertbackground="#FFFFFF")

# spacer label #2 to separate columns 2 and 4
spacer_label_2 = Label(xy_frame, text="  ")
spacer_label_2.grid(row=1, column=3, sticky=EW)

# Set up subroutine #1 label and text box and grid them into xy_frame
subroutine_1_label = Label(xy_frame, text="SUBROUTINE #1")
subroutine_1_label.grid(row=0, column=4, sticky=EW)
subroutine_1_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
subroutine_1_text_box.grid(row=1, column=4)
subroutine_1_text_box.config(insertbackground="#FFFFFF")

# Set up subroutine #2 label and text box and grid them into xy_frame
subroutine_2_label = Label(xy_frame, text="SUBROUTINE #2")
subroutine_2_label.grid(row=2, column=4, sticky=EW)
subroutine_2_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
subroutine_2_text_box.grid(row=3, column=4)
subroutine_2_text_box.config(insertbackground="#FFFFFF")

# Set up subroutine #3 label and text box and grid them into xy_frame
subroutine_3_label = Label(xy_frame, text="SUBROUTINE #3")
subroutine_3_label.grid(row=4, column=4, sticky=EW)
subroutine_3_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
subroutine_3_text_box.grid(row=5, column=4)
subroutine_3_text_box.config(insertbackground="#FFFFFF")

# button frame to hold the RUN, LOAD SCRIPT and SAVE SCRIPT buttons and the label and text widget
# for entering total loops (i.e. the number of times the user wants the main loop to run)
button_frame = ttk.Frame(root)

# run button
run_button = ttk.Button(button_frame, text='RUN SCRIPT', command=guiscript_run)
run_button.grid(row=0, column=0, sticky=EW)

# load script button
load_script_button = ttk.Button(button_frame, text='LOAD SCRIPT', command=load_script)
load_script_button.grid(row=0, column=1, sticky=EW)

# save script button
save_script_button = ttk.Button(button_frame, text='SAVE SCRIPT', command=save_script)
save_script_button.grid(row=0, column=2, sticky=EW)

# Grid xy_frame into root
xy_frame.grid(row=0, column=0, sticky=W)

# Grid button_frame into root
button_frame.grid(row=1, column=0, sticky=W)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Frame to hold the SETTINGS button and the total loops label and total loops text widget
second_button_frame = ttk.Frame(root)

# settings button
settings_button = ttk.Button(second_button_frame, text='SETTINGS', command=display_settings_window)
settings_button.grid(row=0, column=0, sticky=EW)

# spacer label #3 in between settings button and total loops label
spacer_label_3 = Label(second_button_frame, text="  ")
spacer_label_3.grid(row=0, column=1, sticky=EW)

# "total loops" label and text widget in which the user can enter total number of times the main loop
# will run
total_loops_label = Label(second_button_frame, text="Total loops")
total_loops_label.grid(row=0, column=2, sticky=EW)
total_loops_text_box = Text(second_button_frame, width=4, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
total_loops_text_box.grid(row=0, column=3)
total_loops_text_box.config(insertbackground="#FFFFFF")

# grid second_button_frame onto root
second_button_frame.grid(row=2, column=0, sticky=EW)
# START OF NEW 6/6/18 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# "Set Total Loops" window
set_total_loops_window = Tk()
set_total_loops_window.wm_title("Set Total Loops")

# Frame to hold the "Set total loops" label
set_total_loops_label_frame = ttk.Frame(set_total_loops_window)

# Set up "Set Total Loops" label and grid it into the set_total_loops_label_frame
set_total_loops_label = Label(set_total_loops_label_frame, text="Set Total Loops")
set_total_loops_label.grid(row=0, column=0, sticky=EW)

# Frame to hold the "buttons for setting total loops from 1 to 20
set_total_loops_frame = ttk.Frame(set_total_loops_window)

# "Set total loops to 1" button
total_loops_button_1 = ttk.Button(set_total_loops_frame, text='1', width=3,
					command=set_total_loops_to_1)
total_loops_button_1.grid(row=1, column=0, sticky=W)

# "Set total loops to 2" button
total_loops_button_2 = ttk.Button(set_total_loops_frame, text='2', width=3,
					command=set_total_loops_to_2)
total_loops_button_2.grid(row=1, column=1, sticky=W)

# "Set total loops to 3" button
total_loops_button_3 = ttk.Button(set_total_loops_frame, text='3', width=3,
					command=set_total_loops_to_3)
total_loops_button_3.grid(row=1, column=2, sticky=W)

# "Set total loops to 4" button
total_loops_button_4 = ttk.Button(set_total_loops_frame, text='4', width=3,
					command=set_total_loops_to_4)
total_loops_button_4.grid(row=1, column=3, sticky=W)

# "Set total loops to 5" button
total_loops_button_5 = ttk.Button(set_total_loops_frame, text='5', width=3,
					command=set_total_loops_to_5)
total_loops_button_5.grid(row=1, column=4, sticky=W)

# "Set total loops to 6" button
total_loops_button_6 = ttk.Button(set_total_loops_frame, text='6', width=3,
					command=set_total_loops_to_6)
total_loops_button_6.grid(row=2, column=0, sticky=W)

# "Set total loops to 7" button
total_loops_button_7 = ttk.Button(set_total_loops_frame, text='7', width=3,
					command=set_total_loops_to_7)
total_loops_button_7.grid(row=2, column=1, sticky=W)

# "Set total loops to 8" button
total_loops_button_8 = ttk.Button(set_total_loops_frame, text='8', width=3,
					command=set_total_loops_to_8)
total_loops_button_8.grid(row=2, column=2, sticky=W)

# "Set total loops to 9" button
total_loops_button_9 = ttk.Button(set_total_loops_frame, text='9', width=3,
					command=set_total_loops_to_9)
total_loops_button_9.grid(row=2, column=3, sticky=W)

# "Set total loops to 10" button
total_loops_button_10 = ttk.Button(set_total_loops_frame, text='10', width=3,
					command=set_total_loops_to_10)
total_loops_button_10.grid(row=2, column=4, sticky=W)

# "Set total loops to 11" button
total_loops_button_11 = ttk.Button(set_total_loops_frame, text='11', width=3,
					command=set_total_loops_to_11)
total_loops_button_11.grid(row=3, column=0, sticky=W)

# "Set total loops to 12" button
total_loops_button_12 = ttk.Button(set_total_loops_frame, text='12', width=3,
					command=set_total_loops_to_12)
total_loops_button_12.grid(row=3, column=1, sticky=W)

# "Set total loops to 13" button
total_loops_button_13 = ttk.Button(set_total_loops_frame, text='13', width=3,
					command=set_total_loops_to_13)
total_loops_button_13.grid(row=3, column=2, sticky=W)

# "Set total loops to 14" button
total_loops_button_14 = ttk.Button(set_total_loops_frame, text='14', width=3,
					command=set_total_loops_to_14)
total_loops_button_14.grid(row=3, column=3, sticky=W)

# "Set total loops to 15" button
total_loops_button_15 = ttk.Button(set_total_loops_frame, text='15', width=3,
					command=set_total_loops_to_15)
total_loops_button_15.grid(row=3, column=4, sticky=W)

# "Set total loops to 16" button
total_loops_button_16 = ttk.Button(set_total_loops_frame, text='16', width=3,
					command=set_total_loops_to_16)
total_loops_button_16.grid(row=4, column=0, sticky=W)

# "Set total loops to 17" button
total_loops_button_17 = ttk.Button(set_total_loops_frame, text='17', width=3,
					command=set_total_loops_to_17)
total_loops_button_17.grid(row=4, column=1, sticky=W)

# "Set total loops to 18" button
total_loops_button_18 = ttk.Button(set_total_loops_frame, text='18', width=3,
					command=set_total_loops_to_18)
total_loops_button_18.grid(row=4, column=2, sticky=W)

# "Set total loops to 19" button
total_loops_button_19 = ttk.Button(set_total_loops_frame, text='19', width=3,
					command=set_total_loops_to_19)
total_loops_button_19.grid(row=4, column=3, sticky=W)

# "Set total loops to 20" button
total_loops_button_20 = ttk.Button(set_total_loops_frame, text='20', width=3,
					command=set_total_loops_to_20)
total_loops_button_20.grid(row=4, column=4, sticky=W)

# grid the set_total_loops_label_frame
set_total_loops_label_frame.grid(row=0, column=0, sticky=EW)

# grid the set_total_loops_frame
set_total_loops_frame.grid(row=1, column=0, sticky=W)

# new frame to hold the second "Run Script" button, at the bottom of the
# "set total loops" window
second_run_button_frame = ttk.Frame(set_total_loops_window)

# second "Run Script" button, in the set total loops window
run_button_2 = ttk.Button(second_run_button_frame, text='RUN SCRIPT', command=guiscript_run)
run_button_2.grid(row=0, column=0, sticky=EW)

# grid the second_run_button_frame
second_run_button_frame.grid(row=2, column=0, sticky=EW)

# size mode button frame to hold "small mode" and "large mode"
size_mode_button_frame = ttk.Frame(set_total_loops_window)

# small mode button
small_mode_button = ttk.Button(size_mode_button_frame, text='SMALL', width=8,
                               command=activate_small_mode)
small_mode_button.grid(row=0, column=0, sticky=W)

# large mode button
large_mode_button = ttk.Button(size_mode_button_frame, text='LARGE', width=8,
                               command=activate_large_mode)
large_mode_button.grid(row=0, column=1, sticky=W)

# grid the size_mode_button_frame
size_mode_button_frame.grid(row=3, column=0, sticky=EW)

# END OF NEW 6/6/18 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Start 'er up!
root.mainloop()
