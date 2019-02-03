import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BCM)

PORT_RELAY_GATE = 21
PORT_RELAY_UNUSED_1 = 20
PORT_RELAY_UNUSED_2 = 19
PORT_RELAY_UNUSED_3 = 26

PORT_KEYPAD_COLUMN1 = 18
PORT_KEYPAD_COLUMN2 = 27
PORT_KEYPAD_COLUMN3 = 22
PORT_KEYPAD_ROW1 = 4
PORT_KEYPAD_ROW2 = 14
PORT_KEYPAD_ROW3 = 15
PORT_KEYPAD_ROW4 = 17

PORT_BUZZER_BUTTON_DOWNSTAIRS = 16
PORT_BUZZER_BUTTON_UPSTAIRS = 13

PORT_DOOR_BELL_BUTTON = 12

# set relays as output
GPIO.setup(PORT_RELAY_GATE, GPIO.OUT, initial=0)
GPIO.setup(PORT_RELAY_UNUSED_1, GPIO.OUT, initial=0)
GPIO.setup(PORT_RELAY_UNUSED_2, GPIO.OUT, initial=0)
GPIO.setup(PORT_RELAY_UNUSED_3, GPIO.OUT, initial=0)

# set buttons as inputs
# pins need to be pull down since the buttons are pull ups
GPIO.setup(PORT_BUZZER_BUTTON_DOWNSTAIRS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PORT_BUZZER_BUTTON_UPSTAIRS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PORT_DOOR_BELL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_pressed(channel):
    print "button pressed", channel
    
GPIO.add_event_detect(PORT_BUZZER_BUTTON_DOWNSTAIRS, GPIO.RISING, callback=button_pressed, bouncetime=300)
GPIO.add_event_detect(PORT_BUZZER_BUTTON_UPSTAIRS, GPIO.RISING, callback=button_pressed, bouncetime=300)
GPIO.add_event_detect(PORT_DOOR_BELL_BUTTON, GPIO.RISING, callback=button_pressed, bouncetime=300)