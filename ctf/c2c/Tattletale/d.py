#!/usr/bin/env python3
import struct

# -------------------------------
# Configuration
# -------------------------------
FILE = "cron.aseng"
FORMAT = "QQHHi"
EVENT_SIZE = struct.calcsize(FORMAT)

# Base Keymap (Keys 1-88)
KEYMAP = {
    1: "ESC", 2: "1", 3: "2", 4: "3", 5: "4", 6: "5", 7: "6", 8: "7", 9: "8", 10: "9", 11: "0", 12: "-", 13: "=",
    14: "BACKSPACE", 15: "TAB", 16: "q", 17: "w", 18: "e", 19: "r", 20: "t", 21: "y", 22: "u", 23: "i", 24: "o", 25: "p",
    26: "[", 27: "]", 28: "ENTER", 29: "LEFTCTRL", 30: "a", 31: "s", 32: "d", 33: "f", 34: "g", 35: "h", 36: "j", 37: "k", 38: "l",
    39: ";", 40: "'", 41: "`", 42: "LEFTSHIFT", 43: "\\", 44: "z", 45: "x", 46: "c", 47: "v", 48: "b", 49: "n", 50: "m",
    51: ",", 52: ".", 53: "/", 54: "RIGHTSHIFT", 56: "LEFTALT", 57: "SPACE", 58: "CAPSLOCK",
    87: "F11", 88: "F12",
}

# Shift Map (What happens when Shift + Key is pressed)
SHIFT_MAP = {
    "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(", "0": ")",
    "-": "_", "=": "+", "[": "{", "]": "}", "\\": "|", ";": ":", "'": "\"", "`": "~", ",": "<", ".": ">", "/": "?"
}

decoded = []
shift_pressed = False
caps_lock = False

with open(FILE, "rb") as f:
    while True:
        data = f.read(EVENT_SIZE)
        if not data:
            break
            
        tv_sec, tv_usec, ev_type, code, value = struct.unpack(FORMAT, data)

        # ev_type 1 is EV_KEY
        if ev_type == 1:
            # value 0 = Release, 1 = Press, 2 = Repeat
            
            # 1. Handle Shift State (Press=1, Release=0)
            if code in (42, 54): # Left or Right Shift
                shift_pressed = (value == 1 or value == 2)
                continue
            
            # 2. Handle CapsLock Toggle (Press=1 only)
            if code == 58 and value == 1:
                caps_lock = not caps_lock
                continue

            # 3. Process other keys ONLY on Press (1) or Repeat (2)
            if value in (1, 2):
                key = KEYMAP.get(code, "")
                
                if key == "BACKSPACE":
                    if decoded: decoded.pop()
                elif key == "SPACE":
                    decoded.append(" ")
                elif key == "ENTER":
                    decoded.append("\n")
                elif key == "TAB":
                    decoded.append("\t")
                elif len(key) == 1:
                    # Handle Letters
                    if key.isalpha():
                        # Logic: If Shift OR Caps (but not both) -> Uppercase
                        if shift_pressed ^ caps_lock: 
                            decoded.append(key.upper())
                        else:
                            decoded.append(key.lower())
                    # Handle Symbols/Numbers
                    else:
                        if shift_pressed and key in SHIFT_MAP:
                            decoded.append(SHIFT_MAP[key])
                        else:
                            decoded.append(key)
                # Handle Ctrl+C (End of capture often)
                elif key == "c" and "LEFTCTRL" in decoded[-5:]: 
                     decoded.append("^C")

output = "".join(decoded)
print(output)