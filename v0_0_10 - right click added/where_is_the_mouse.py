# ============================================================================
import pyautogui, tkinter, time
# ============================================================================
def main():

    print('Press ctrl-C to quit.')

    try:
        while True:
            # get and print the mouse coordinates
            x, y = pyautogui.position()
            pos_string = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(pos_string)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print('\nDone!')

    return
# ============================================================================
main()
