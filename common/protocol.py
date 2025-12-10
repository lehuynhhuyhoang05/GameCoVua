"""
Message protocol for client-server communication
"""

import json
from datetime import datetime
from typing import Dict, Any


def create_message(msg_type: str, data: Dict[str, Any] = None) -> str:
    """
    Create a JSON message with standard format
    
    Args:
        msg_type: Type of message
        data: Message data payload
    
    Returns:
        JSON string message
    """
    message = {
        "type": msg_type,
        "timestamp": datetime.now().isoformat(),
        "data": data or {}
    }
    return json.dumps(message)


def parse_message(message: str) -> Dict[str, Any]:
    """
    Parse JSON message string
    
    Args:
        message: JSON string message
    
    Returns:
        Parsed message dictionary
    """
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        return {
            "type": "ERROR",
            "data": {"error": "Invalid message format"}
        }


def send_message(socket, msg_type: str, data: Dict[str, Any] = None):
    """
    Send message through socket
    
    Args:
        socket: Socket object
        msg_type: Type of message
        data: Message data payload
    """
    message = create_message(msg_type, data)
    socket.sendall(message.encode('utf-8'))


def receive_message(socket, buffer_size: int = 4096) -> Dict[str, Any]:
    """
    Receive and parse message from socket
    
    Args:
        socket: Socket object
        buffer_size: Buffer size for receiving
    
    Returns:
        Parsed message dictionary
    """
    try:
        data = socket.recv(buffer_size).decode('utf-8')
        if not data:
            return None
        return parse_message(data)
    except Exception as e:
        return {
            "type": "ERROR",
            "data": {"error": str(e)}
        }
