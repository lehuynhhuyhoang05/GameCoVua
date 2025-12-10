"""
Network handler for client-server communication
"""

import socket
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.constants import *
from common.protocol import send_message, receive_message


class NetworkHandler:
    """Handles network communication with server"""
    
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.running = False
        self.message_callback = None
        
    def connect(self) -> bool:
        """Connect to server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.running = True
            
            # Start receive thread
            receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            receive_thread.start()
            
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def send(self, msg_type: str, data: dict = None):
        """Send message to server"""
        if self.connected and self.socket:
            try:
                send_message(self.socket, msg_type, data)
            except Exception as e:
                print(f"Send error: {e}")
                self.connected = False
    
    def _receive_loop(self):
        """Receive messages from server"""
        while self.running and self.connected:
            try:
                message = receive_message(self.socket, BUFFER_SIZE)
                if message and self.message_callback:
                    self.message_callback(message)
                elif not message:
                    self.connected = False
                    break
            except Exception as e:
                if self.running:
                    print(f"Receive error: {e}")
                self.connected = False
                break
    
    def set_message_callback(self, callback):
        """Set callback for received messages"""
        self.message_callback = callback
