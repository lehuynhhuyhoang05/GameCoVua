"""
Keyboard shortcuts manager for chess game
"""

class ShortcutManager:
    """Manages keyboard shortcuts"""
    
    SHORTCUTS = {
        # Game controls
        '<Escape>': 'Deselect piece',
        '<Control-n>': 'New game / Create room',
        '<Control-r>': 'Refresh rooms',
        '<Control-q>': 'Quit / Logout',
        
        # In-game actions
        '<Control-z>': 'Undo move (if allowed)',
        '<Control-y>': 'Redo move (if allowed)',
        '<Control-s>': 'Offer draw',
        '<Control-x>': 'Resign',
        
        # UI controls
        '<F11>': 'Toggle fullscreen',
        '<Control-t>': 'Change theme',
        '<Control-m>': 'Toggle sound',
        '<Control-h>': 'Show help',
        
        # Chat
        '<Return>': 'Send chat message (when in chat)',
        '<Control-slash>': 'Focus chat',
        
        # Navigation
        '<Tab>': 'Switch focus',
        '<Up>': 'Scroll up (in chat/history)',
        '<Down>': 'Scroll down (in chat/history)',
    }
    
    @staticmethod
    def get_all_shortcuts():
        """Get all available shortcuts"""
        return ShortcutManager.SHORTCUTS
    
    @staticmethod
    def get_shortcuts_text():
        """Get formatted shortcuts text for display"""
        text = "⌨️ KEYBOARD SHORTCUTS\n\n"
        
        categories = {
            'Game Controls': ['<Escape>', '<Control-n>', '<Control-r>', '<Control-q>'],
            'In-Game Actions': ['<Control-z>', '<Control-y>', '<Control-s>', '<Control-x>'],
            'UI Controls': ['<F11>', '<Control-t>', '<Control-m>', '<Control-h>'],
            'Chat': ['<Return>', '<Control-slash>'],
            'Navigation': ['<Tab>', '<Up>', '<Down>']
        }
        
        for category, keys in categories.items():
            text += f"═══ {category} ═══\n"
            for key in keys:
                if key in ShortcutManager.SHORTCUTS:
                    # Format key name
                    key_display = key.replace('<', '').replace('>', '').replace('-', '+')
                    text += f"  {key_display:20} → {ShortcutManager.SHORTCUTS[key]}\n"
            text += "\n"
        
        return text


def bind_shortcuts(widget, callbacks: dict):
    """
    Bind keyboard shortcuts to a widget
    
    Args:
        widget: Tkinter widget to bind to
        callbacks: Dictionary mapping shortcut keys to callback functions
    """
    for key, callback in callbacks.items():
        if callable(callback):
            widget.bind(key, callback)
