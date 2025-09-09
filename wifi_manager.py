"""
WiFi Connection Module for Raspberry Pi Pico W
Handles WiFi connectivity and network operations
"""

import network
import time
import urequests as requests
from config import WIFI_SSID, WIFI_PASSWORD, MAX_RETRIES, DEBUG_MODE


class WiFiManager:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.is_connected = False
        
    def connect(self):
        """Connect to WiFi network"""
        if DEBUG_MODE:
            print(f"Connecting to WiFi: {WIFI_SSID}")
            
        self.wlan.active(True)
        self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection
        retry_count = 0
        while not self.wlan.isconnected() and retry_count < MAX_RETRIES:
            if DEBUG_MODE:
                print(f"Connection attempt {retry_count + 1}...")
            time.sleep(2)
            retry_count += 1
            
        if self.wlan.isconnected():
            self.is_connected = True
            if DEBUG_MODE:
                print(f"Connected! IP: {self.wlan.ifconfig()[0]}")
            return True
        else:
            self.is_connected = False
            if DEBUG_MODE:
                print("Failed to connect to WiFi")
            return False
    
    def disconnect(self):
        """Disconnect from WiFi"""
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.wlan.active(False)
        self.is_connected = False
        if DEBUG_MODE:
            print("WiFi disconnected")
    
    def get_status(self):
        """Get current WiFi connection status"""
        return {
            'connected': self.wlan.isconnected(),
            'ip': self.wlan.ifconfig()[0] if self.wlan.isconnected() else None,
            'strength': self.wlan.status() if self.wlan.isconnected() else None
        }
    
    def make_request(self, url, method='GET', headers=None, data=None):
        """Make HTTP request with error handling"""
        if not self.wlan.isconnected():
            raise Exception("Not connected to WiFi")
            
        try:
            if method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                response = requests.get(url, headers=headers)
            return response
        except Exception as e:
            if DEBUG_MODE:
                print(f"Request error: {e}")
            raise e