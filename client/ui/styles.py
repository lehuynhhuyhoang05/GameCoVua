"""
UI Styles and Colors for Chess Client
"""

# Color Scheme
COLORS = {
    # Board Colors
    'light_square': '#F0D9B5',
    'dark_square': '#B58863',
    'highlight': '#BACA44',
    'selected': '#7CB342',
    'legal_move': '#829769',
    'last_move': '#CDD26A',
    'check': '#FF6B6B',
    
    # UI Colors
    'primary': '#2196F3',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'info': '#00BCD4',
    'dark': '#263238',
    'light': '#ECEFF1',
    
    # Text Colors
    'text_dark': '#212121',
    'text_light': '#FFFFFF',
    'text_gray': '#757575',
    
    # Background
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F5F5F5',
    'bg_dark': '#37474F',
}

# Fonts
FONTS = {
    'title': ('Segoe UI', 24, 'bold'),
    'heading': ('Segoe UI', 18, 'bold'),
    'subheading': ('Segoe UI', 14, 'bold'),
    'body': ('Segoe UI', 12),
    'small': ('Segoe UI', 10),
    'button': ('Segoe UI', 11, 'bold'),
    'chess_piece': ('Arial', 48, 'bold'),
    'board_coord': ('Arial', 10),
}

# Sizes
SIZES = {
    'board': 560,
    'square': 70,
    'button_width': 20,
    'button_height': 2,
    'entry_width': 25,
    'chat_height': 15,
    'padding': 10,
}

# Unicode Chess Pieces (Better looking)
PIECES_UNICODE = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

# Button Styles
def get_button_style(style='primary'):
    """Get button style configuration"""
    styles = {
        'primary': {
            'bg': COLORS['primary'],
            'fg': COLORS['text_light'],
            'activebackground': '#1976D2',
            'activeforeground': COLORS['text_light'],
            'relief': 'flat',
            'cursor': 'hand2',
            'font': FONTS['button'],
        },
        'success': {
            'bg': COLORS['success'],
            'fg': COLORS['text_light'],
            'activebackground': '#388E3C',
            'activeforeground': COLORS['text_light'],
            'relief': 'flat',
            'cursor': 'hand2',
            'font': FONTS['button'],
        },
        'warning': {
            'bg': COLORS['warning'],
            'fg': COLORS['text_light'],
            'activebackground': '#F57C00',
            'activeforeground': COLORS['text_light'],
            'relief': 'flat',
            'cursor': 'hand2',
            'font': FONTS['button'],
        },
        'danger': {
            'bg': COLORS['danger'],
            'fg': COLORS['text_light'],
            'activebackground': '#D32F2F',
            'activeforeground': COLORS['text_light'],
            'relief': 'flat',
            'cursor': 'hand2',
            'font': FONTS['button'],
        },
        'dark': {
            'bg': COLORS['dark'],
            'fg': COLORS['text_light'],
            'activebackground': '#1C2833',
            'activeforeground': COLORS['text_light'],
            'relief': 'flat',
            'cursor': 'hand2',
            'font': FONTS['button'],
        },
    }
    return styles.get(style, styles['primary'])

# Frame Styles
def get_frame_style(style='default'):
    """Get frame style configuration"""
    styles = {
        'default': {
            'bg': COLORS['bg_primary'],
            'relief': 'flat',
        },
        'secondary': {
            'bg': COLORS['bg_secondary'],
            'relief': 'flat',
        },
        'dark': {
            'bg': COLORS['bg_dark'],
            'relief': 'flat',
        },
        'card': {
            'bg': COLORS['bg_primary'],
            'relief': 'solid',
            'borderwidth': 1,
        },
    }
    return styles.get(style, styles['default'])
