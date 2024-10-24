from machine import Pin
import time

# Morse class defined
class Morse:
    def __init__(self):
        self.codes = {
            ".-": "A",
            "-...": "B",
            "-.-.": "C",
            "-..": "D",
            ".": "E",
            "..-.": "F",
            "--.": "G",
            "....": "H",
            "..": "I",
            ".---": "J",
            "-.-": "K",
            ".-..": "L",
            "--": "M",
            "-.": "N",
            "---": "O",
            ".--.": "P",
            "--.-": "Q",
            ".-.": "R",
            "...": "S",
            "-": "T",
            "..-": "U",
            "...-": "V",
            ".--": "W",
            "-..-": "X",
            "-.--": "Y",
            "--..": "Z",
            ".-.-.": "1",
            "..-.": "2",
            "...-.": "3",
            "....-": "4",
            ".....": "5",
            "-....": "6",
            "--...": "7",
            "---..": "8",
            "----.": "9",
            "----": "0"
        }
        self.min_press = 20
        self.short = 200
        self.long = 600
        self.letter_space = 500
        self.word_space = 1000
        self.timeout = 3000

    def decode(self, str):
        msg = ""
        letters = str.split()
        for letter in letters:
            msg += self.codes.get(letter, f"?{str}?")

        return msg

    def run(self):
        button = Button(Pin(10, mode=Pin.IN, pull=Pin.PULL_UP), self.min_press, self.timeout)
        msg_morse = ""
        msg = ""
        while(True):
            try:
                u, d = button.read()
                # If the release was a word release (longer than self.word_space)
                # add decoded current word, add space to msg, and reset msg_morse (for next word)
                if self.word_space < u:
                    msg += self.decode(msg_morse)
                    msg += " "
                    msg_morse = ""
                else:
                    # If the release was a letter release, we delimit using a space
                    if self.letter_space < u:
                        msg_morse += " "
                # Check if input was a dot or a dash
                if d <= self.long:
                    msg_morse += "."
                else:
                    msg_morse += "-"
            except Button.ButtonException:
                break
            print(f"PRESS: Up for {u:5d} ms, down for {d:5d} ms")
        
        if msg_morse != "":
            msg += self.decode(msg_morse)
        
        print(f"The morse code message: {msg}")


# Button class taken from read.py
class Button:
    def __init__(self, pin, min_press, timeout):
        self.pin = pin
        self.min_press_ms = min_press
        self.timeout_ms = timeout

    def read(self):
        if self.pin.value == 0:
            self.wait_release(self.timeout_ms)
        p = self.wait_press(self.timeout_ms)
        r = self.wait_release(self.timeout_ms)
        return p, r

    # Calculates how long the button has been pressed for
    def wait_release(self, timeout):
        start_time = time.ticks_ms()
        current_time = time.ticks_ms()
        release_time = time.ticks_ms()
        release_duration = time.ticks_diff(current_time, release_time)
        total_duration = 0

        # while release duration is less than min press
        while release_duration < self.min_press_ms:
            # update current time
            current_time = time.ticks_ms()
            # if button is pressed again, reset release time to current time
            if self.pin.value() == 0:
                release_time = current_time
            # calculate release duration
            release_duration = time.ticks_diff(current_time, release_time)
            # calculate total duration
            total_duration = current_time - start_time
            # If button pressed for too long, we timeout
            if total_duration > timeout:
                raise Button.ButtonException("Button has been pressed for too long")

        return total_duration

    # Calculates how long the button has been released for
    def wait_press(self, timeout):
        start_time = time.ticks_ms()
        current_time = time.ticks_ms()
        press_time = time.ticks_ms()
        press_duration = time.ticks_diff(current_time, press_time)
        total_duration = 0

        # while release duration is less than min press
        while press_duration < self.min_press_ms:
            # update current time
            current_time = time.ticks_ms()
            # if button is released again, reset press time to current time
            if self.pin.value() == 1:
                press_time = current_time
            # calculate release duration
            press_duration = time.ticks_diff(current_time, press_time)
            # calculate total duration
            total_duration = current_time - start_time
            # If button released for too long, we timeout
            if total_duration > timeout:
                raise Button.ButtonException("Button has been released for too long")

        return total_duration

    class ButtonException(Exception):
        pass


# Driver code
morse = Morse()
morse.run()