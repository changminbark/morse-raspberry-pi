# Button and Morse Code Decoder Project

This project consists of two Python files, `read.py` and `morse.py`, that utilize a physical button connected to a microcontroller for different purposes: button press detection and Morse code decoding.

## Project Structure

- **`read.py`**: A button handler that detects and measures how long a button is pressed and released, printing the duration in milliseconds.
- **`morse.py`**: A Morse code decoder that uses the button input to interpret short and long presses as Morse code dots and dashes, and decodes them into human-readable messages.

## Requirements

- **Hardware**: A microcontroller compatible with Python (such as ESP32 or Raspberry Pi Pico) and a button.
- **Software**: Python with the `machine` and `time` libraries.

## File Descriptions

### 1. `read.py`

This file defines a `Button` class to detect button presses and releases, calculating the duration of each. The program continuously monitors button activity and prints how long the button is pressed and released in milliseconds.

#### Features:

- **Button Press Detection**: Detects when the button is pressed and released.
- **Timeout Handling**: Ensures the button isn't pressed or released for too long, triggering a timeout exception if necessary.

### 2. `morse.py`

This file defines a `Morse` class that decodes button presses into Morse code and translates them into letters and words. It reads the button press durations to distinguish between dots (short presses), dashes (long presses), letter spaces, and word spaces.

#### Features:

- **Morse Code Decoding**: Short presses are interpreted as dots, long presses as dashes.
- **Letter and Word Separation**: Spaces between button presses are used to detect the end of letters and words.
- **Timeout Handling**: Similar to `read.py`, this file also handles timeouts when a button is pressed or released for too long.

## How to Run

1. **Connect the Button**: Attach a button to a suitable pin on your microcontroller. For example, in both scripts, the button is connected to pin 10 with a pull-up resistor.
   
2. **Run `read.py`**: This file will print the button press durations for every press and release cycle.

3. **Run `morse.py`**: This file will decode your button presses into Morse code. Short presses (less than 200ms) are interpreted as dots, and long presses (more than 600ms) are dashes. Spaces between words and letters are also detected based on release time.

## Customization

You can modify parameters such as the minimum press duration (`min_press`), time thresholds for dots and dashes (`short`, `long`), and the timeout period to adapt to your specific use case or hardware configuration.

---

Feel free to adapt and extend this project for other button-based applications or to add additional Morse code functionality!

