from machine import Pin
import time


class Button:
    def __init__(self, pin, min_press_ms = 20):
        self.pin = pin
        self.min_press_ms = min_press_ms 

    def read(self, timeout_ms):
        if self.pin.value == 0:
            self.wait_release(timeout_ms)
        p = self.wait_press(timeout_ms)
        r = self.wait_release(timeout_ms)
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


button = Button(Pin(10, mode=Pin.IN, pull=Pin.PULL_UP))
while(True):
    try:
        u,d = button.read(timeout_ms=3000)
    except Button.ButtonException:
        continue
    print(f"PRESS: Up for {u:5d} ms, down for {d:5d} ms")