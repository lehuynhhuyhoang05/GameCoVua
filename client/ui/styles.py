"""
UI Styles and Colors for Chess Client - Enhanced
"""

# Color Scheme - Modern & Vibrant
COLORS = {
    # Board Colors - Premium Look
    'light_square': '#EEEED2',
    'dark_square': '#769656',
    'highlight': '#BACA44',
    'selected': '#F6F669',
    'legal_move': '#829769',
    'last_move': '#CDD26A',
    'check': '#FF5252',
    'premove': '#40C4FF',
    
    # UI Colors - Material Design 2.0
    'primary': '#1976D2',
    'primary_dark': '#1565C0',
    'primary_light': '#42A5F5',
    'success': '#43A047',
    'success_dark': '#388E3C',
    'warning': '#FB8C00',
    'warning_dark': '#F57C00',
    'danger': '#E53935',
    'danger_dark': '#D32F2F',
    'info': '#00ACC1',
    'dark': '#263238',
    'light': '#ECEFF1',
    
    # Text Colors
    'text_dark': '#212121',
    'text_light': '#FFFFFF',
    'text_gray': '#757575',
    'text_muted': '#9E9E9E',
    
    # Background - Layered Design
    'bg_primary': '#FAFAFA',
    'bg_secondary': '#F5F5F5',
    'bg_card': '#FFFFFF',
    'bg_dark': '#37474F',
    'bg_darker': '#263238',
    
    # Shadows & Effects (Tkinter doesn't support alpha, use gray tones)
    'shadow_sm': '#E0E0E0',
    'shadow_md': '#BDBDBD',
    'shadow_lg': '#9E9E9E',
    
    # Gradients (as tuples of colors)
    'gradient_primary': ('#1976D2', '#42A5F5'),
    'gradient_success': ('#43A047', '#66BB6A'),
    'gradient_danger': ('#E53935', '#EF5350'),
}

# Fonts - Better Hierarchy
FONTS = {
    'title': ('Segoe UI', 28, 'bold'),
    'heading': ('Segoe UI', 20, 'bold'),
    'subheading': ('Segoe UI', 16, 'bold'),
    'body': ('Segoe UI', 12),
    'body_bold': ('Segoe UI', 12, 'bold'),
    'small': ('Segoe UI', 10),
    'tiny': ('Segoe UI', 9),
    'button': ('Segoe UI', 12, 'bold'),
    'button_large': ('Segoe UI', 14, 'bold'),
    'chess_piece': ('Arial Unicode MS', 56, 'bold'),
    'board_coord': ('Segoe UI', 9),
    'timer': ('Consolas', 36, 'bold'),
    'timer_small': ('Consolas', 18, 'bold'),
}

# Sizes - Better Proportions
SIZES = {
    'board': 600,  # Larger board
    'square': 75,
    'button_width': 20,
    'button_height': 2,
    'entry_width': 30,
    'chat_height': 15,
    'padding': 15,
    'padding_small': 8,
    'padding_large': 20,
    'border_radius': 8,  # For visual reference (tkinter doesn't support, but good for planning)
}

# Unicode Chess Pieces (Better looking)
PIECES_UNICODE = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

# Button Styles - Enhanced with Hover Effects
def get_button_style(style='primary', size='normal'):
    """Get button style configuration with hover support"""
    
    base_styles = {
        'primary': {
            'bg': COLORS['primary'],
            'fg': COLORS['text_light'],
            'activebackground': COLORS['primary_dark'],
            'activeforeground': COLORS['text_light'],
        },
        'success': {
            'bg': COLORS['success'],
            'fg': COLORS['text_light'],
            'activebackground': COLORS['success_dark'],
            'activeforeground': COLORS['text_light'],
        },
        'warning': {
            'bg': COLORS['warning'],
            'fg': COLORS['text_light'],
            'activebackground': COLORS['warning_dark'],
            'activeforeground': COLORS['text_light'],
        },
        'danger': {
            'bg': COLORS['danger'],
            'fg': COLORS['text_light'],
            'activebackground': COLORS['danger_dark'],
            'activeforeground': COLORS['text_light'],
        },
        'dark': {
            'bg': COLORS['dark'],
            'fg': COLORS['text_light'],
            'activebackground': COLORS['bg_darker'],
            'activeforeground': COLORS['text_light'],
        },
        'light': {
            'bg': COLORS['bg_card'],
            'fg': COLORS['text_dark'],
            'activebackground': COLORS['bg_secondary'],
            'activeforeground': COLORS['text_dark'],
        },
    }
    
    # Get base style
    btn_style = base_styles.get(style, base_styles['primary']).copy()
    
    # Add common properties
    btn_style.update({
        'relief': 'flat',
        'cursor': 'hand2',
        'borderwidth': 0,
    })
    
    # Adjust font based on size
    if size == 'large':
        btn_style['font'] = FONTS['button_large']
    elif size == 'small':
        btn_style['font'] = FONTS['body']
    else:
        btn_style['font'] = FONTS['button']
    
    return btn_style

# Frame Styles - Enhanced with Borders
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
            'bg': COLORS['bg_card'],
            'relief': 'solid',
            'borderwidth': 1,
            'highlightthickness': 0,
        },
        'elevated': {
            'bg': COLORS['bg_card'],
            'relief': 'raised',
            'borderwidth': 2,
        },
    }
    return styles.get(style, styles['default'])


# Label Styles
def get_label_style(style='default'):
    """Get label style configuration"""
    styles = {
        'title': {
            'font': FONTS['title'],
            'bg': COLORS['bg_primary'],
            'fg': COLORS['primary'],
        },
        'heading': {
            'font': FONTS['heading'],
            'bg': COLORS['bg_primary'],
            'fg': COLORS['text_dark'],
        },
        'body': {
            'font': FONTS['body'],
            'bg': COLORS['bg_primary'],
            'fg': COLORS['text_dark'],
        },
        'muted': {
            'font': FONTS['small'],
            'bg': COLORS['bg_primary'],
            'fg': COLORS['text_muted'],
        },
    }
    return styles.get(style, styles['body'])


# Entry/Input Styles
def get_entry_style():
    """Get entry widget style"""
    return {
        'font': FONTS['body'],
        'relief': 'solid',
        'borderwidth': 2,
        'highlightthickness': 0,
    }


# Utility Functions
def add_hover_effect(widget, color_normal, color_hover):
    """Add hover effect to widget"""
    def on_enter(e):
        widget.config(bg=color_hover)
    
    def on_leave(e):
        widget.config(bg=color_normal)
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)


def create_separator(parent, orient='horizontal'):
    """Create a visual separator"""
    import tkinter as tk
    from tkinter import ttk
    
    if orient == 'horizontal':
        sep = ttk.Separator(parent, orient='horizontal')
    else:
        sep = ttk.Separator(parent, orient='vertical')
    
    return sep
