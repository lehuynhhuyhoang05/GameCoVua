"""
Desktop notification system for chess game
Cross-platform notifications using plyer
"""

try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("plyer not available - desktop notifications disabled")


class NotificationManager:
    """Manages desktop notifications"""
    
    def __init__(self):
        self.enabled = NOTIFICATIONS_AVAILABLE
        self.app_name = "Chess Online"
        self.app_icon = None  # Path to icon file
    
    def notify(self, title: str, message: str, timeout: int = 5):
        """
        Show a desktop notification
        
        Args:
            title: Notification title
            message: Notification message
            timeout: Duration in seconds
        """
        if not self.enabled:
            return
        
        try:
            notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                app_icon=self.app_icon,
                timeout=timeout
            )
        except Exception as e:
            print(f"Notification error: {e}")
    
    def notify_game_start(self, opponent: str):
        """Notify when game starts"""
        self.notify(
            "Game Started!",
            f"Your game with {opponent} has begun. Good luck!",
            timeout=3
        )
    
    def notify_your_turn(self):
        """Notify when it's player's turn"""
        self.notify(
            "Your Turn!",
            "It's your move in the chess game.",
            timeout=2
        )
    
    def notify_game_over(self, result: str):
        """Notify when game ends"""
        self.notify(
            "Game Over",
            result,
            timeout=5
        )
    
    def notify_opponent_joined(self, opponent: str):
        """Notify when opponent joins"""
        self.notify(
            "Opponent Joined!",
            f"{opponent} has joined your game.",
            timeout=3
        )
    
    def notify_check(self):
        """Notify when in check"""
        self.notify(
            "Check!",
            "You are in check! Protect your king.",
            timeout=3
        )
    
    def notify_chat_message(self, sender: str):
        """Notify new chat message"""
        self.notify(
            "New Message",
            f"Message from {sender}",
            timeout=2
        )
    
    def toggle_notifications(self):
        """Toggle notifications on/off"""
        if NOTIFICATIONS_AVAILABLE:
            self.enabled = not self.enabled
        return self.enabled


# Global notification manager
_notification_manager = None

def get_notification_manager() -> NotificationManager:
    """Get global notification manager instance"""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager
