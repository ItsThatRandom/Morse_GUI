from tkinter import *
from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Morse code lengths
dot = 0.5
dash = 1.5
# Below are one unit (0.5) shorter than normal as a dot is always played after an element in translate().
gap = 1.0 
end = 3.0

# Morse code dictionary
mc_dict = { 'a':[dot, dash], 'b':[dash, dot, dot, dot], 'c':[dash, dot, dash, dot], 'd':[dash, dot, dot],
            'e':[dot], 'f':[dot, dot, dash, dot], 'g':[dash, dash, dot], 'h':[dot, dot, dot, dot], 'i':[dot, dot],
            'j':[dot, dash, dash, dash], 'k':[dash, dot, dash], 'l':[dot, dash, dot, dot], 'm':[dash, dash],
            'n':[dash, dot], 'o':[dash, dash, dash], 'p':[dot, dash, dash, dot], 'q':[dash, dash, dot, dash],
            'r':[dot, dash, dot], 's':[dot, dot, dot], 't':[dash], 'u':[dot, dot, dash], 'v':[dot, dot, dot, dash],
            'w':[dot, dash, dash], 'x':[dash, dot, dot, dash], 'y':[dash, dot, dash, dash], 'z':[dash, dash, dot, dot]}

# Hardware
g_led = LED(21)

# GUI
window = Tk()
window.title("5.2C")


# Functions
# Translates message into morse code using our morse code dictionary.
def translate():
    result = message.get().lower()
    for letter in result:
        if letter in mc_dict:
            
            # interval is our dash or dot
            for interval in mc_dict[letter]:
                g_led.on()
                sleep(interval)
                g_led.off()
                sleep(dot)
            sleep(gap)
        else:
            sleep(end)

# Ensures a max of 12 characters and only one word.
def valid(P):
    if len(P) > 12 or ' ' in P:
        return False
    return True

def close():
    GPIO.cleanup()
    window.destroy()

# Registering our validation command used to limit character input.
vcmd = (window.register(valid), '%P')

# Buttons/Input Text
exit_button = Button(window, text = "Exit", command = close, bg = "bisque2", height = 1, width = 3)
message = Entry(validate = "key", validatecommand = vcmd)
g_button = Button(window, text = "Blink in morse code", command = translate, bg = "lime green", height = 1, width = 15)

# Positions in window
exit_button.grid(row = 0, column = 0)
message.grid(row = 1, column = 0)
g_button.grid(row = 2, column = 0)

# If default close 'x' in window is used, still use function close().
window.protocol("WM_DELETE_WINDOW", close)

# loop
window.mainloop()