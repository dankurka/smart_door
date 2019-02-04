import RPi.GPIO as GPIO  
import time
from threading import Thread
from pad4pi import rpi_gpio

GPIO.setmode(GPIO.BCM)

PORT_RELAY_GATE = 21
PORT_RELAY_UNUSED_1 = 20
PORT_RELAY_UNUSED_2 = 19
PORT_RELAY_UNUSED_3 = 26

PORT_KEYPAD_COLUMN1 = 15
PORT_KEYPAD_COLUMN2 = 14
PORT_KEYPAD_COLUMN3 = 27
PORT_KEYPAD_ROW1 = 22
PORT_KEYPAD_ROW2 = 4
PORT_KEYPAD_ROW3 = 18
PORT_KEYPAD_ROW4 = 17

PORT_BUZZER_BUTTON_DOWNSTAIRS = 16
PORT_BUZZER_BUTTON_UPSTAIRS = 12

PORT_DOOR_BELL_BUTTON = 13

# set relays as output
GPIO.setup(PORT_RELAY_GATE, GPIO.OUT, initial=1)
GPIO.setup(PORT_RELAY_UNUSED_1, GPIO.OUT, initial=1)
GPIO.setup(PORT_RELAY_UNUSED_2, GPIO.OUT, initial=1)
GPIO.setup(PORT_RELAY_UNUSED_3, GPIO.OUT, initial=1)

# set buttons as inputs
# pins need to be pull down since the buttons are pull ups
GPIO.setup(PORT_BUZZER_BUTTON_DOWNSTAIRS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PORT_BUZZER_BUTTON_UPSTAIRS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PORT_DOOR_BELL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed(channel):
    print "button pressed", channel
    if channel in [PORT_BUZZER_BUTTON_DOWNSTAIRS, PORT_BUZZER_BUTTON_UPSTAIRS]:
        open_door()

def do_open_door():
    print "activating buzzer"
    GPIO.output(PORT_RELAY_GATE, 0)
    time.sleep(5)
    print "deactivating buzzer"
    GPIO.output(PORT_RELAY_GATE, 1)

def open_door():
    thread = Thread(target = do_open_door)
    thread.start()


GPIO.add_event_detect(PORT_BUZZER_BUTTON_DOWNSTAIRS, GPIO.FALLING, callback=button_pressed, bouncetime=300)
GPIO.add_event_detect(PORT_BUZZER_BUTTON_UPSTAIRS, GPIO.FALLING, callback=button_pressed, bouncetime=300)
GPIO.add_event_detect(PORT_DOOR_BELL_BUTTON, GPIO.FALLING, callback=button_pressed, bouncetime=300)


KEYPAD = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    ["*",0,"#"]
]

ROW_PINS = [PORT_KEYPAD_ROW1,PORT_KEYPAD_ROW2,PORT_KEYPAD_ROW3,PORT_KEYPAD_ROW4] # BCM numbering
COL_PINS = [PORT_KEYPAD_COLUMN1,PORT_KEYPAD_COLUMN2, PORT_KEYPAD_COLUMN3] # BCM numbering

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS, key_delay=150)

keys_pushed = []
door_code = [1,2,3,4]

def keypad_pressed(key):
    print key
    global keys_pushed
    global door_code
    keys_pushed.append(key)

    if keys_pushed == door_code:
        open_door()
    if len(keys_pushed) >= 4:
        keys_pushed = []

keypad.registerKeyPressHandler(keypad_pressed)


try:
    while True:
        time.sleep(1)
finally:
    keypad.cleanup()
