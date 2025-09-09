"""
Main Application for Raspberry Pi Pico W - Gemini AI Integration
Provides translator, quiz, and chat functionality with QWERTY keyboard interface
"""

import time
import gc
from machine import Pin, reset
from config import DEBUG_MODE
from wifi_manager import WiFiManager
from gemini_client import GeminiClient
from qwerty_keyboard import QWERTYKeyboard
from translator import Translator
from quiz_module import QuizModule
from chat_module import ChatModule


class GeminiPicoApp:
    def __init__(self):
        self.version = "1.0.0"
        self.start_time = time.time()
        
        # Initialize components
        self.wifi_manager = None
        self.gemini_client = None
        self.keyboard = None
        self.translator = None
        self.quiz_module = None
        self.chat_module = None
        
        # Status LED (built-in LED on Pico W)
        self.status_led = Pin("LED", Pin.OUT)
        self.status_led.off()
        
        if DEBUG_MODE:
            print(f"Gemini Pico App v{self.version} initializing...")
    
    def blink_status_led(self, times=3, delay=0.5):
        """Blink status LED"""
        for _ in range(times):
            self.status_led.on()
            time.sleep(delay)
            self.status_led.off()
            time.sleep(delay)
    
    def initialize_components(self):
        """Initialize all application components"""
        try:
            print("Initializing components...")
            
            # Initialize keyboard
            self.keyboard = QWERTYKeyboard()
            print("✓ Keyboard initialized")
            
            # Initialize WiFi manager
            self.wifi_manager = WiFiManager()
            print("✓ WiFi manager initialized")
            
            # Initialize Gemini client
            self.gemini_client = GeminiClient(self.wifi_manager)
            print("✓ Gemini client initialized")
            
            # Initialize modules
            self.translator = Translator(self.gemini_client, self.keyboard)
            print("✓ Translator module initialized")
            
            self.quiz_module = QuizModule(self.gemini_client, self.keyboard)
            print("✓ Quiz module initialized")
            
            self.chat_module = ChatModule(self.gemini_client, self.keyboard)
            print("✓ Chat module initialized")
            
            self.blink_status_led(2, 0.3)
            return True
            
        except Exception as e:
            print(f"Component initialization error: {e}")
            self.blink_status_led(5, 0.1)  # Error indication
            return False
    
    def connect_wifi(self):
        """Connect to WiFi network"""
        print("\nConnecting to WiFi...")
        
        if self.wifi_manager.connect():
            print("✓ WiFi connected successfully")
            self.status_led.on()  # Keep LED on when connected
            return True
        else:
            print("✗ WiFi connection failed")
            print("Please check your WiFi credentials in config.py")
            self.blink_status_led(10, 0.1)  # Error indication
            return False
    
    def test_gemini_connection(self):
        """Test connection to Gemini API"""
        print("\nTesting Gemini API connection...")
        
        try:
            success, message = self.gemini_client.check_api_status()
            if success:
                print("✓ Gemini API is accessible")
                return True
            else:
                print(f"✗ Gemini API test failed: {message}")
                return False
        except Exception as e:
            print(f"✗ Gemini API test error: {e}")
            return False
    
    def display_main_menu(self):
        """Display main application menu"""
        print("\n" + "="*50)
        print(f"  Raspberry Pi Pico W - Gemini AI Assistant v{self.version}")
        print("="*50)
        print("1. Translator")
        print("2. Personalized Quiz")
        print("3. Chat with Gemini")
        print("4. System Status")
        print("5. Settings")
        print("9. Restart System")
        print("0. Exit")
        print("="*50)
    
    def display_system_status(self):
        """Display system status information"""
        print("\n=== System Status ===")
        
        # WiFi status
        wifi_status = self.wifi_manager.get_status()
        print(f"WiFi: {'Connected' if wifi_status['connected'] else 'Disconnected'}")
        if wifi_status['connected']:
            print(f"IP Address: {wifi_status['ip']}")
        
        # System uptime
        uptime = time.time() - self.start_time
        hours = int(uptime // 3600)
        minutes = int((uptime % 3600) // 60)
        seconds = int(uptime % 60)
        print(f"Uptime: {hours}h {minutes}m {seconds}s")
        
        # Memory usage (approximate)
        try:
            gc.collect()
            print(f"Free memory: {gc.mem_free()} bytes")
        except:
            print("Memory info unavailable")
        
        # Component status
        print(f"Translator: {'Ready' if self.translator else 'Not initialized'}")
        print(f"Quiz: {'Ready' if self.quiz_module else 'Not initialized'}")
        print(f"Chat: {'Ready' if self.chat_module else 'Not initialized'}")
        
        # Test API connection
        try:
            api_test = self.gemini_client.check_api_status()
            print(f"Gemini API: {'Connected' if api_test[0] else 'Error'}")
        except:
            print("Gemini API: Error")
    
    def display_settings(self):
        """Display and manage settings"""
        while True:
            print("\n=== Settings ===")
            print("1. WiFi Information")
            print("2. Reconnect WiFi")
            print("3. Test Gemini API")
            print("4. System Information")
            print("5. Debug Mode Toggle")
            print("6. Keyboard Test")
            print("0. Back to main menu")
            
            choice = self.keyboard.get_input_prompt("Select option: ")
            
            if choice == '0':
                break
            elif choice == '1':
                wifi_status = self.wifi_manager.get_status()
                print(f"\nWiFi Status: {'Connected' if wifi_status['connected'] else 'Disconnected'}")
                if wifi_status['connected']:
                    print(f"IP Address: {wifi_status['ip']}")
                    print(f"Signal Strength: {wifi_status['strength']}")
            elif choice == '2':
                self.wifi_manager.disconnect()
                time.sleep(1)
                self.connect_wifi()
            elif choice == '3':
                self.test_gemini_connection()
            elif choice == '4':
                self.display_system_status()
            elif choice == '5':
                global DEBUG_MODE
                DEBUG_MODE = not DEBUG_MODE
                print(f"Debug mode: {'ON' if DEBUG_MODE else 'OFF'}")
            elif choice == '6':
                self.keyboard.display_keyboard()
                test_text = self.keyboard.get_input_prompt("Test keyboard input: ")
                print(f"You typed: '{test_text}'")
            else:
                print("Invalid option.")
    
    def handle_memory_cleanup(self):
        """Perform memory cleanup"""
        if DEBUG_MODE:
            print("Performing memory cleanup...")
        gc.collect()
    
    def run(self):
        """Main application loop"""
        print(f"\nStarting Gemini Pico App v{self.version}...")
        
        # Initialize components
        if not self.initialize_components():
            print("Failed to initialize components. Exiting.")
            return
        
        # Connect to WiFi
        if not self.connect_wifi():
            print("WiFi connection required. Please check configuration.")
            return
        
        # Test Gemini API
        if not self.test_gemini_connection():
            print("Warning: Gemini API not accessible. Some features may not work.")
            proceed = self.keyboard.get_input_prompt("Continue anyway? (y/n): ").lower()
            if proceed != 'y':
                return
        
        print("\n✓ System ready!")
        self.blink_status_led(3, 0.2)
        
        # Main application loop
        while True:
            try:
                self.display_main_menu()
                choice = self.keyboard.get_input_prompt("Select option: ")
                
                if choice == '0':
                    print("Goodbye!")
                    break
                elif choice == '1':
                    if self.translator:
                        self.translator.run()
                    else:
                        print("Translator not available")
                elif choice == '2':
                    if self.quiz_module:
                        self.quiz_module.run()
                    else:
                        print("Quiz module not available")
                elif choice == '3':
                    if self.chat_module:
                        self.chat_module.run()
                    else:
                        print("Chat module not available")
                elif choice == '4':
                    self.display_system_status()
                elif choice == '5':
                    self.display_settings()
                elif choice == '9':
                    confirm = self.keyboard.get_input_prompt(
                        "Restart system? (y/n): "
                    ).lower()
                    if confirm == 'y':
                        print("Restarting system...")
                        time.sleep(1)
                        reset()
                else:
                    print("Invalid option. Please try again.")
                
                # Periodic memory cleanup
                self.handle_memory_cleanup()
                
            except KeyboardInterrupt:
                print("\nShutdown requested by user")
                break
            except Exception as e:
                print(f"Application error: {e}")
                if DEBUG_MODE:
                    import sys
                    sys.print_exception(e)
                
                # Try to recover
                print("Attempting to recover...")
                self.handle_memory_cleanup()
                time.sleep(2)
        
        # Cleanup
        print("Shutting down...")
        if self.wifi_manager:
            self.wifi_manager.disconnect()
        self.status_led.off()
        print("System shutdown complete.")


def main():
    """Main entry point"""
    try:
        app = GeminiPicoApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        if DEBUG_MODE:
            import sys
            sys.print_exception(e)
    finally:
        # Ensure LED is off
        try:
            status_led = Pin("LED", Pin.OUT)
            status_led.off()
        except:
            pass


if __name__ == "__main__":
    main()