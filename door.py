import RPi.GPIO as GPIO  
import time
from threading import Thread
from pad4pi import rpi_gpio
import SimpleHTTPServer
import SocketServer


GPIO.setmode(GPIO.BCM)

PORT_RELAY_GATE = 19
PORT_RELAY_DOOR = 20
PORT_RELAY_UNUSED_2 = 26
PORT_RELAY_UNUSED_3 = 21

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
GPIO.setup(PORT_RELAY_DOOR, GPIO.OUT, initial=1)
GPIO.setup(PORT_RELAY_UNUSED_2, GPIO.OUT, initial=1)
GPIO.setup(PORT_RELAY_UNUSED_3, GPIO.OUT, initial=1)

# set buttons as inputs
# pins need to be pull down since the buttons are pull ups
GPIO.setup(PORT_BUZZER_BUTTON_DOWNSTAIRS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PORT_BUZZER_BUTTON_UPSTAIRS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PORT_DOOR_BELL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

door_buzzing = False

def button_pressed(channel):
    print "button pressed", channel
    if channel in [PORT_BUZZER_BUTTON_DOWNSTAIRS, PORT_BUZZER_BUTTON_UPSTAIRS]:
        open_door()

def do_open_door():
    global door_buzzing
    if door_buzzing:
        return
    door_buzzing = True
    print "activating buzzer"
    GPIO.output(PORT_RELAY_GATE, 0)
    #GPIO.output(PORT_RELAY_DOOR, 0)
    time.sleep(3)
    print "deactivating buzzer"
    GPIO.output(PORT_RELAY_GATE, 1)
    #GPIO.output(PORT_RELAY_DOOR, 1)
    time.sleep(0.2)
    door_buzzing = False

def open_door():
    thread = Thread(target = do_open_door)
    thread.start()


GPIO.add_event_detect(PORT_BUZZER_BUTTON_DOWNSTAIRS, GPIO.FALLING, callback=button_pressed, bouncetime=300)
GPIO.add_event_detect(PORT_BUZZER_BUTTON_UPSTAIRS, GPIO.FALLING, callback=button_pressed, bouncetime=300)
GPIO.add_event_detect(PORT_DOOR_BELL_BUTTON, GPIO.FALLING, callback=button_pressed, bouncetime=300)


KEYPAD = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']
]

ROW_PINS = [PORT_KEYPAD_ROW1,PORT_KEYPAD_ROW2,PORT_KEYPAD_ROW3,PORT_KEYPAD_ROW4] # BCM numbering
COL_PINS = [PORT_KEYPAD_COLUMN1,PORT_KEYPAD_COLUMN2, PORT_KEYPAD_COLUMN3] # BCM numbering

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS, key_delay=150)


def read_door_code():
    f = open('door_code.txt', 'r')
    lines = f.read().splitlines()
    if len(lines) != 1:
        raise ValueError('door code text file has too many lines.')
    door_code = lines[0].split(',')
    if len(door_code) != 4:
        raise ValueError('door code needs to be length 4')
    # todo validate
    return door_code

keys_pushed = []
door_code = read_door_code()
time_left = 5




def timer_thread():
    global time_left
    global keys_pushed

    while True:
        if time_left == 0:
            if len(keys_pushed) > 0:
                keys_pushed = []
                print "Reseted input"
        if time_left > 0:
            time_left = time_left - 1
        time.sleep(1)
        
timer = Thread(target = timer_thread)
timer.daemon = True
timer.start()

def keypad_pressed(key):
    print key
    global keys_pushed
    global door_code
    global time_left
    keys_pushed.append(key)

    time_left = 5
    if keys_pushed == door_code:
        open_door()
    if len(keys_pushed) >= 4:
        keys_pushed = []

keypad.registerKeyPressHandler(keypad_pressed)

PAGE = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<script>
function openDoor() {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", '/', true);

  xhr.onreadystatechange = function() { // Call a function when the state changes.
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      // Request finished. Do processing here.
    }
  }
  xhr.send();
}
</script>
</head>
<body>
<button onclick="openDoor()">Open da door</button>
</body>
"""
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        global PAGE
        self.send_response(200)
        self.end_headers()
        self.wfile.write(PAGE)
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("door buzzing!")
        open_door()


server = SocketServer.TCPServer(('0.0.0.0', 8080), MyRequestHandler)

try:
    server.serve_forever()
finally:
    keypad.cleanup()
