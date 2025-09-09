"""
QWERTY Keyboard Interface for Raspberry Pi Pico W
Handles keyboard input simulation and text entry
"""

import time
from machine import Pin
from config import KEYBOARD_DEBOUNCE_MS, KEYBOARD_ROWS, KEYBOARD_COLS, DEBUG_MODE


class QWERTYKeyboard:
    def __init__(self):
        # QWERTY keyboard layout
        self.key_map = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
            [' ', 'shift', 'ctrl', 'alt', 'del', 'enter', 'esc', 'tab', 'caps', 'bksp']
        ]
        
        # Special keys mapping
        self.special_keys = {
            'shift': 'SHIFT',
            'ctrl': 'CTRL',
            'alt': 'ALT',
            'del': 'DELETE',
            'enter': 'ENTER',
            'esc': 'ESCAPE',
            'tab': 'TAB',
            'caps': 'CAPS_LOCK',
            'bksp': 'BACKSPACE',
            ' ': 'SPACE'
        }
        
        # Current state
        self.current_text = ""
        self.shift_pressed = False
        self.caps_lock = False
        self.cursor_position = 0
        
        # For simulation purposes (since we don't have physical keyboard matrix)
        self.virtual_mode = True
        
        if DEBUG_MODE:
            print("QWERTY Keyboard initialized")
    
    def get_key_display(self, row, col):
        """Get the display character for a key position"""
        if row < len(self.key_map) and col < len(self.key_map[row]):
            key = self.key_map[row][col]
            if key in self.special_keys:
                return self.special_keys[key]
            elif self.shift_pressed or self.caps_lock:
                return key.upper()
            else:
                return key
        return ""
    
    def process_key_press(self, key):
        """Process a key press and update current text"""
        if key == 'shift':
            self.shift_pressed = not self.shift_pressed
            return None
        elif key == 'caps':
            self.caps_lock = not self.caps_lock
            return None
        elif key == 'bksp':
            if self.current_text and self.cursor_position > 0:
                self.current_text = (self.current_text[:self.cursor_position-1] + 
                                   self.current_text[self.cursor_position:])
                self.cursor_position -= 1
            return 'BACKSPACE'
        elif key == 'enter':
            result = self.current_text
            self.clear_text()
            return result
        elif key == 'esc':
            self.clear_text()
            return 'ESCAPE'
        elif key == 'del':
            if self.current_text and self.cursor_position < len(self.current_text):
                self.current_text = (self.current_text[:self.cursor_position] + 
                                   self.current_text[self.cursor_position+1:])
            return 'DELETE'
        elif key == ' ':
            self.add_character(' ')
            return 'SPACE'
        else:
            # Regular character
            char = key.upper() if (self.shift_pressed or self.caps_lock) else key
            self.add_character(char)
            self.shift_pressed = False  # Reset shift after use
            return char
    
    def add_character(self, char):
        """Add a character at cursor position"""
        self.current_text = (self.current_text[:self.cursor_position] + 
                           char + 
                           self.current_text[self.cursor_position:])
        self.cursor_position += 1
    
    def clear_text(self):
        """Clear current text and reset cursor"""
        self.current_text = ""
        self.cursor_position = 0
    
    def get_current_text(self):
        """Get current text being typed"""
        return self.current_text
    
    def get_cursor_position(self):
        """Get current cursor position"""
        return self.cursor_position
    
    def move_cursor_left(self):
        """Move cursor left"""
        if self.cursor_position > 0:
            self.cursor_position -= 1
    
    def move_cursor_right(self):
        """Move cursor right"""
        if self.cursor_position < len(self.current_text):
            self.cursor_position += 1
    
    def display_keyboard(self):
        """Display current keyboard layout (for debugging/UI)"""
        print("\n=== QWERTY Keyboard ===")
        for row_idx, row in enumerate(self.key_map):
            row_display = []
            for col_idx, key in enumerate(row):
                display_key = self.get_key_display(row_idx, col_idx)
                row_display.append(f"[{display_key:^6}]")
            print(" ".join(row_display))
        
        print(f"\nCurrent text: '{self.current_text}'")
        print(f"Cursor position: {self.cursor_position}")
        print(f"Shift: {self.shift_pressed}, Caps: {self.caps_lock}")
    
    def simulate_typing(self, text):
        """Simulate typing text (for testing)"""
        self.clear_text()
        for char in text:
            if char.isupper():
                self.shift_pressed = True
            self.process_key_press(char.lower())
        return self.current_text
    
    def get_input_prompt(self, prompt="Enter text: "):
        """Get text input with prompt (simulation for testing)"""
        print(f"\n{prompt}")
        print("(This is a simulation - in real hardware, use physical keyboard)")
        print("Type 'DONE' when finished, 'CLEAR' to clear, 'SHOW' to show keyboard")
        
        while True:
            user_input = input("Keyboard input: ").strip()
            
            if user_input == 'DONE':
                result = self.current_text
                self.clear_text()
                return result
            elif user_input == 'CLEAR':
                self.clear_text()
                print("Text cleared")
            elif user_input == 'SHOW':
                self.display_keyboard()
            else:
                # Process each character
                for char in user_input:
                    self.process_key_press(char.lower())
                print(f"Current text: '{self.current_text}'")