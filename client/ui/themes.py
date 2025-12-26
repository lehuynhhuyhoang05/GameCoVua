"""
Theme management for chess board
Supports multiple visual themes
"""

class BoardTheme:
    """Chess board theme definition"""
    
    def __init__(self, name: str, light_square: str, dark_square: str, 
                 highlight: str, move_hint: str, last_move: str, check: str,
                 selected: str, bg_color: str):
        self.name = name
        self.light_square = light_square
        self.dark_square = dark_square
        self.highlight = highlight
        self.move_hint = move_hint
        self.last_move = last_move
        self.check = check
        self.selected = selected
        self.bg_color = bg_color


# Predefined themes
THEMES = {
    'classic': BoardTheme(
        name='Classic',
        light_square='#F0D9B5',
        dark_square='#B58863',
        highlight='#90EE90',
        move_hint='#7FA650',
        last_move='#CDD16A',
        check='#FF6B6B',
        selected='#F7EC90',
        bg_color='#312E2B'
    ),
    
    'modern': BoardTheme(
        name='Modern',
        light_square='#EEEED2',
        dark_square='#769656',
        highlight='#BBDB44',
        move_hint='#829769',
        last_move='#AAA23A',
        check='#E74C3C',
        selected='#F6F669',
        bg_color='#2C2C2C'
    ),
    
    'blue': BoardTheme(
        name='Blue Ocean',
        light_square='#DEE3E6',
        dark_square='#8CA2AD',
        highlight='#6FA8DC',
        move_hint='#7FA1B0',
        last_move='#A3C5D6',
        check='#FF4444',
        selected='#B4D7E8',
        bg_color='#1E3A4C'
    ),
    
    'wood': BoardTheme(
        name='Wooden',
        light_square='#F0D0A0',
        dark_square='#8B4513',
        highlight='#90CC90',
        move_hint='#6B8E23',
        last_move='#D4A574',
        check='#DC143C',
        selected='#FFE4B5',
        bg_color='#3E2723'
    ),
    
    'purple': BoardTheme(
        name='Purple Dream',
        light_square='#E8D5E8',
        dark_square='#9B59B6',
        highlight='#BB86FC',
        move_hint='#A374C8',
        last_move='#C5A3E0',
        check='#E91E63',
        selected='#D4B4E8',
        bg_color='#2D1B3D'
    ),
    
    'dark': BoardTheme(
        name='Dark Mode',
        light_square='#3E3E3E',
        dark_square='#1E1E1E',
        highlight='#4A90A4',
        move_hint='#3A7A8A',
        last_move='#5A6A5A',
        check='#FF5555',
        selected='#5E6E7E',
        bg_color='#121212'
    ),
    
    'neon': BoardTheme(
        name='Neon',
        light_square='#1A1A2E',
        dark_square='#0F0F1E',
        highlight='#00FF88',
        move_hint='#00CC77',
        last_move='#16213E',
        check='#FF0055',
        selected='#0F4C75',
        bg_color='#0A0A0A'
    ),
    
    'lichess_brown': BoardTheme(
        name='Lichess Brown',
        light_square='#F0D9B5',
        dark_square='#B58863',
        highlight='#A0C060',
        move_hint='#809050',
        last_move='#C5C084',
        check='#E74C3C',
        selected='#E8E18E',
        bg_color='#2B2724'
    ),
    
    'chess_com': BoardTheme(
        name='Chess.com',
        light_square='#EBECD0',
        dark_square='#739552',
        highlight='#C0D860',
        move_hint='#8FA861',
        last_move='#B8C568',
        check='#E74C3C',
        selected='#F5F682',
        bg_color='#312E2B'
    ),
    
    'coral': BoardTheme(
        name='Coral',
        light_square='#FFE4E1',
        dark_square='#FF7F50',
        highlight='#90EE90',
        move_hint='#FFA07A',
        last_move='#FFB6A3',
        check='#DC143C',
        selected='#FFDAB9',
        bg_color='#2B1B17'
    )
}


class ThemeManager:
    """Manages board themes"""
    
    def __init__(self):
        self.current_theme_name = 'classic'
        self.themes = THEMES
    
    def get_current_theme(self) -> BoardTheme:
        """Get current active theme"""
        return self.themes[self.current_theme_name]
    
    def set_theme(self, theme_name: str):
        """Set active theme"""
        if theme_name in self.themes:
            self.current_theme_name = theme_name
            return True
        return False
    
    def get_theme_names(self):
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def get_theme(self, theme_name: str) -> BoardTheme:
        """Get specific theme by name"""
        return self.themes.get(theme_name, self.themes['classic'])


# Global theme manager
_theme_manager = None

def get_theme_manager() -> ThemeManager:
    """Get global theme manager instance"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
