"""
Test script for Gemini Pico App
Tests basic functionality of individual modules
"""

import sys
import time

# Mock MicroPython modules for testing on desktop
class MockPin:
    def __init__(self, pin, mode):
        self.pin = pin
        self.mode = mode
        self.state = False
    
    def on(self):
        self.state = True
        print(f"LED ON")
    
    def off(self):
        self.state = False
        print(f"LED OFF")

class MockNetwork:
    STA_IF = 1
    
    class WLAN:
        def __init__(self, mode):
            self.mode = mode
            self.connected = False
            
        def active(self, state):
            print(f"WiFi active: {state}")
        
        def connect(self, ssid, password):
            print(f"Connecting to {ssid}...")
            self.connected = True
        
        def isconnected(self):
            return self.connected
        
        def ifconfig(self):
            return ['192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8']
        
        def status(self):
            return 3  # Connected
        
        def disconnect(self):
            self.connected = False

# Mock machine module
class MockMachine:
    Pin = MockPin
    
    @staticmethod
    def reset():
        print("System reset requested")

# Install mocks
sys.modules['machine'] = MockMachine()
sys.modules['network'] = MockNetwork()

# Mock urequests
class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = str(json_data) if json_data else ""
    
    def json(self):
        return self._json_data
    
    def close(self):
        pass

class MockRequests:
    @staticmethod
    def post(url, headers=None, json=None):
        print(f"Mock POST to {url}")
        # Mock Gemini API response
        mock_response = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": "This is a mock response from Gemini API for testing purposes."
                    }]
                }
            }]
        }
        return MockResponse(200, mock_response)
    
    @staticmethod
    def get(url, headers=None):
        print(f"Mock GET to {url}")
        return MockResponse(200, {"status": "ok"})

sys.modules['urequests'] = MockRequests()

# Now import our modules
from qwerty_keyboard import QWERTYKeyboard
from wifi_manager import WiFiManager
from gemini_client import GeminiClient


def test_keyboard():
    """Test QWERTY keyboard functionality"""
    print("\n=== Testing QWERTY Keyboard ===")
    
    keyboard = QWERTYKeyboard()
    
    # Test typing simulation
    test_text = "Hello World"
    result = keyboard.simulate_typing(test_text)
    print(f"Simulated typing '{test_text}': {result}")
    
    # Test special keys
    keyboard.clear_text()
    keyboard.process_key_press('h')
    keyboard.process_key_press('i')
    keyboard.process_key_press('bksp')
    keyboard.process_key_press('e')
    keyboard.process_key_press('l')
    keyboard.process_key_press('l')
    keyboard.process_key_press('o')
    
    print(f"After typing 'hi' then backspace then 'ello': '{keyboard.get_current_text()}'")
    
    # Test shift
    keyboard.clear_text()
    keyboard.process_key_press('shift')
    keyboard.process_key_press('h')
    keyboard.process_key_press('e')
    keyboard.process_key_press('l')
    keyboard.process_key_press('l')
    keyboard.process_key_press('o')
    
    print(f"With shift: '{keyboard.get_current_text()}'")
    
    return True


def test_wifi_manager():
    """Test WiFi manager functionality"""
    print("\n=== Testing WiFi Manager ===")
    
    wifi = WiFiManager()
    
    # Test connection
    success = wifi.connect()
    print(f"WiFi connection: {'Success' if success else 'Failed'}")
    
    # Test status
    status = wifi.get_status()
    print(f"WiFi status: {status}")
    
    # Test request (mocked)
    try:
        response = wifi.make_request("https://api.example.com/test")
        print(f"Mock request status: {response.status_code}")
    except Exception as e:
        print(f"Request error: {e}")
    
    return True


def test_gemini_client():
    """Test Gemini client functionality"""
    print("\n=== Testing Gemini Client ===")
    
    wifi = WiFiManager()
    wifi.connect()
    
    client = GeminiClient(wifi)
    
    # Test basic content generation
    try:
        response = client.generate_content("Hello, how are you?")
        print(f"Generated response: {response[:100]}...")
    except Exception as e:
        print(f"Content generation error: {e}")
    
    # Test translation
    try:
        translation = client.translate_text("Hello", "Spanish")
        print(f"Translation result: {translation}")
    except Exception as e:
        print(f"Translation error: {e}")
    
    # Test quiz generation
    try:
        quiz = client.generate_quiz_question("Science", "easy")
        print(f"Quiz question: {quiz.get('question', 'No question generated')[:50]}...")
    except Exception as e:
        print(f"Quiz generation error: {e}")
    
    # Test API status
    try:
        status, message = client.check_api_status()
        print(f"API status: {status}, Message: {message}")
    except Exception as e:
        print(f"API status check error: {e}")
    
    return True


def run_all_tests():
    """Run all test functions"""
    print("Starting Gemini Pico App Tests")
    print("=" * 50)
    
    tests = [
        ("Keyboard", test_keyboard),
        ("WiFi Manager", test_wifi_manager),
        ("Gemini Client", test_gemini_client)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning {test_name} test...")
            success = test_func()
            results.append((test_name, success, None))
            print(f"✓ {test_name} test completed")
        except Exception as e:
            results.append((test_name, False, str(e)))
            print(f"✗ {test_name} test failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, success, error in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
        if error:
            print(f"  Error: {error}")
        if success:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(tests)} tests")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)