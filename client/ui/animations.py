"""
Animation utilities for smooth UI transitions
"""

import tkinter as tk
from typing import Callable, Optional
import math


class Animator:
    """Handles smooth animations in tkinter"""
    
    def __init__(self, widget: tk.Widget):
        self.widget = widget
        self.animations = []
        self.animation_id = None
    
    def animate_move(self, canvas: tk.Canvas, item_id: int, 
                     from_x: int, from_y: int, to_x: int, to_y: int,
                     duration: int = 200, callback: Optional[Callable] = None):
        """
        Animate moving a canvas item
        
        Args:
            canvas: Canvas widget
            item_id: Canvas item ID
            from_x, from_y: Starting position
            to_x, to_y: Ending position
            duration: Animation duration in milliseconds
            callback: Function to call when animation completes
        """
        start_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
        total_dx = to_x - from_x
        total_dy = to_y - from_y
        
        def step():
            current_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
            elapsed = current_time - start_time
            
            if elapsed >= duration:
                # Animation complete
                canvas.coords(item_id, to_x, to_y)
                if callback:
                    callback()
                return
            
            # Easing function (ease-out cubic)
            progress = elapsed / duration
            eased = 1 - math.pow(1 - progress, 3)
            
            # Calculate new position
            new_x = from_x + (total_dx * eased)
            new_y = from_y + (total_dy * eased)
            
            # Move item
            current_coords = canvas.coords(item_id)
            if current_coords:
                dx = new_x - current_coords[0]
                dy = new_y - current_coords[1]
                canvas.move(item_id, dx, dy)
            
            # Schedule next frame
            self.widget.after(16, step)  # ~60 FPS
        
        step()
    
    def fade_in(self, widget: tk.Widget, duration: int = 300):
        """Fade in a widget"""
        try:
            start_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
            
            def step():
                current_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
                elapsed = current_time - start_time
                
                if elapsed >= duration:
                    widget.config(state=tk.NORMAL)
                    return
                
                progress = elapsed / duration
                # Update widget appearance based on progress
                self.widget.after(16, step)
            
            step()
        except:
            pass
    
    def pulse(self, canvas: tk.Canvas, item_id: int, duration: int = 500, 
              scale_factor: float = 1.1):
        """Create a pulsing effect"""
        start_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
        original_coords = canvas.coords(item_id)
        
        if not original_coords or len(original_coords) < 4:
            return
        
        center_x = (original_coords[0] + original_coords[2]) / 2
        center_y = (original_coords[1] + original_coords[3]) / 2
        
        def step():
            current_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
            elapsed = current_time - start_time
            
            if elapsed >= duration:
                canvas.coords(item_id, *original_coords)
                return
            
            # Sine wave for smooth pulse
            progress = (elapsed / duration) * 2 * math.pi
            scale = 1 + ((scale_factor - 1) * math.sin(progress))
            
            # Calculate scaled coordinates
            x1, y1, x2, y2 = original_coords[:4]
            width = x2 - x1
            height = y2 - y1
            
            new_x1 = center_x - (width * scale / 2)
            new_y1 = center_y - (height * scale / 2)
            new_x2 = center_x + (width * scale / 2)
            new_y2 = center_y + (height * scale / 2)
            
            canvas.coords(item_id, new_x1, new_y1, new_x2, new_y2)
            
            self.widget.after(16, step)
        
        step()
    
    def shake(self, widget: tk.Widget, intensity: int = 5, duration: int = 300):
        """Shake a widget (for invalid moves)"""
        start_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
        original_x = widget.winfo_x()
        
        def step():
            current_time = self.widget.winfo_toplevel().tk.call('clock', 'milliseconds')
            elapsed = current_time - start_time
            
            if elapsed >= duration:
                widget.place(x=original_x)
                return
            
            # Oscillating offset
            progress = (elapsed / duration) * 4 * math.pi
            offset = intensity * math.sin(progress) * (1 - elapsed / duration)
            
            widget.place(x=original_x + offset)
            
            self.widget.after(16, step)
        
        step()


class LoadingSpinner:
    """Animated loading spinner"""
    
    def __init__(self, canvas: tk.Canvas, x: int, y: int, radius: int = 20):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.running = False
        self.angle = 0
        self.arc = None
    
    def start(self):
        """Start the spinner animation"""
        if self.arc is None:
            self.arc = self.canvas.create_arc(
                self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius,
                start=0, extent=90, style=tk.ARC, width=3,
                outline='#4A90E2'
            )
        
        self.running = True
        self._animate()
    
    def stop(self):
        """Stop the spinner animation"""
        self.running = False
        if self.arc:
            self.canvas.delete(self.arc)
            self.arc = None
    
    def _animate(self):
        """Animation loop"""
        if not self.running:
            return
        
        self.angle = (self.angle + 10) % 360
        
        if self.arc:
            self.canvas.itemconfig(self.arc, start=self.angle)
        
        self.canvas.after(16, self._animate)


def smooth_scroll(text_widget: tk.Text, target_line: int, duration: int = 300):
    """Smoothly scroll text widget to a line"""
    start_pos = float(text_widget.yview()[0])
    total_lines = int(text_widget.index('end-1c').split('.')[0])
    target_pos = max(0, min(1, (target_line - 1) / total_lines))
    
    start_time = text_widget.winfo_toplevel().tk.call('clock', 'milliseconds')
    
    def step():
        current_time = text_widget.winfo_toplevel().tk.call('clock', 'milliseconds')
        elapsed = current_time - start_time
        
        if elapsed >= duration:
            text_widget.yview_moveto(target_pos)
            return
        
        progress = elapsed / duration
        eased = 1 - math.pow(1 - progress, 3)
        
        new_pos = start_pos + ((target_pos - start_pos) * eased)
        text_widget.yview_moveto(new_pos)
        
        text_widget.after(16, step)
    
    step()
