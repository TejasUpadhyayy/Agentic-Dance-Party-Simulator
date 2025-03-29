"""
Control Panel Module for Artificial Dance Party Simulation
Provides interactive controls for adjusting simulation parameters
"""
import pygame
import pygame_gui
from typing import Dict, Any, Callable

class ControlPanel:
    """Handles UI controls for adjusting simulation parameters"""
    
    def __init__(self, screen, position, size):
        self.screen = screen
        self.position = position
        self.size = size
        self.visible = False
        self.panel_color = (30, 30, 50, 200)
        
        # Initialize pygame_gui
        self.ui_manager = pygame_gui.UIManager(screen.get_size())
        
        # Create the panel container
        self.panel_rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.panel_rect,
            manager=self.ui_manager
        )
        
        # Track all controls
        self.controls = {}
        self.callbacks = {}
        
        # Create controls with default values
        self._create_controls()
    
    def _create_controls(self):
        """Create all the UI controls"""
        # Panel title
        title_rect = pygame.Rect(10, 10, 180, 30)
        self.controls['title'] = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="Simulation Controls",
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset = 50
        
        # Music tempo slider
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['tempo_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Music Tempo (BPM)",
            manager=self.ui_manager,
            container=self.panel
        )
        
        slider_rect = pygame.Rect(10, y_offset + 25, 180, 20)
        self.controls['tempo_slider'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=slider_rect,
            start_value=120,
            value_range=(80, 160),
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 60
        
        # Creativity distribution slider
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['creativity_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Dancer Creativity",
            manager=self.ui_manager,
            container=self.panel
        )
        
        slider_rect = pygame.Rect(10, y_offset + 25, 180, 20)
        self.controls['creativity_slider'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=slider_rect,
            start_value=0.5,
            value_range=(0.1, 0.9),
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 60
        
        # Extroversion distribution slider
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['social_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Dancer Sociability",
            manager=self.ui_manager,
            container=self.panel
        )
        
        slider_rect = pygame.Rect(10, y_offset + 25, 180, 20)
        self.controls['social_slider'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=slider_rect,
            start_value=0.5,
            value_range=(0.1, 0.9),
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 60
        
        # Dance Floor Size slider (NEW)
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['floor_size_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Dance Floor Size",
            manager=self.ui_manager,
            container=self.panel
        )
        
        slider_rect = pygame.Rect(10, y_offset + 25, 180, 20)
        self.controls['floor_size_slider'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=slider_rect,
            start_value=1.0,
            value_range=(0.5, 1.5),
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 60
        
        # Group Formation Threshold slider (NEW)
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['group_threshold_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Group Formation Ease",
            manager=self.ui_manager,
            container=self.panel
        )
        
        slider_rect = pygame.Rect(10, y_offset + 25, 180, 20)
        self.controls['group_threshold_slider'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=slider_rect,
            start_value=0.1,
            value_range=(0.01, 0.3),
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 60
        
        # Floor mood dropdown
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['mood_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Dance Floor Mood",
            manager=self.ui_manager,
            container=self.panel
        )
        
        dropdown_rect = pygame.Rect(10, y_offset + 25, 180, 30)
        self.controls['mood_dropdown'] = pygame_gui.elements.UIDropDownMenu(
            options_list=['Normal', 'Energetic', 'Relaxed', 'Experimental'],
            starting_option='Normal',
            relative_rect=dropdown_rect,
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 70
        
        # Color Theme dropdown (NEW)
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['theme_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Color Theme",
            manager=self.ui_manager,
            container=self.panel
        )
        
        dropdown_rect = pygame.Rect(10, y_offset + 25, 180, 30)
        self.controls['theme_dropdown'] = pygame_gui.elements.UIDropDownMenu(
            options_list=['Default', 'Neon', 'Pastel', 'Monochrome'],
            starting_option='Default',
            relative_rect=dropdown_rect,
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 70
        
        # Camera Controls (NEW)
        label_rect = pygame.Rect(10, y_offset, 180, 20)
        self.controls['camera_label'] = pygame_gui.elements.UILabel(
            relative_rect=label_rect,
            text="Camera Controls",
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 25
        # Zoom buttons
        zoom_in_rect = pygame.Rect(10, y_offset, 85, 30)
        self.controls['zoom_in_button'] = pygame_gui.elements.UIButton(
            relative_rect=zoom_in_rect,
            text="Zoom In",
            manager=self.ui_manager,
            container=self.panel
        )
        
        zoom_out_rect = pygame.Rect(105, y_offset, 85, 30)
        self.controls['zoom_out_button'] = pygame_gui.elements.UIButton(
            relative_rect=zoom_out_rect,
            text="Zoom Out",
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 40
        # Focus and reset camera buttons
        focus_rect = pygame.Rect(10, y_offset, 85, 30)
        self.controls['focus_button'] = pygame_gui.elements.UIButton(
            relative_rect=focus_rect,
            text="Focus Dancer",
            manager=self.ui_manager,
            container=self.panel
        )
        
        reset_cam_rect = pygame.Rect(105, y_offset, 85, 30)
        self.controls['reset_cam_button'] = pygame_gui.elements.UIButton(
            relative_rect=reset_cam_rect,
            text="Reset View",
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 70
        
        # Add celebrity button
        button_rect = pygame.Rect(10, y_offset, 180, 40)
        self.controls['celebrity_button'] = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="Add Celebrity Dancer",
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 60
        
        # Change Music button
        button_rect = pygame.Rect(10, y_offset, 180, 40)
        self.controls['music_button'] = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="Change Music",
            manager=self.ui_manager,
            container=self.panel
        )
        
        y_offset += 60
        
        # Reset button
        button_rect = pygame.Rect(10, y_offset, 180, 40)
        self.controls['reset_button'] = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="Reset Simulation",
            manager=self.ui_manager,
            container=self.panel
        )
    
    def toggle_visibility(self):
        """Toggle the control panel visibility"""
        self.visible = not self.visible
        if self.visible:
            self.panel.show()
        else:
            self.panel.hide()
    
    def register_callback(self, control_id: str, callback: Callable):
        """Register a callback function for a control"""
        self.callbacks[control_id] = callback
    
    def get_value(self, control_id: str) -> Any:
        """Get the current value of a control"""
        if control_id in self.controls:
            control = self.controls[control_id]
            
            # Different controls have different methods to get values
            if isinstance(control, pygame_gui.elements.UIHorizontalSlider):
                return control.get_current_value()
            elif isinstance(control, pygame_gui.elements.UIDropDownMenu):
                return control.selected_option
            
        return None
    
    def process_events(self, event):
        """Process UI events"""
        if not self.visible:
            return False
        
        # Let the UI manager process the event
        self.ui_manager.process_events(event)
        
        # Handle UI events
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            for control_id, control in self.controls.items():
                if event.ui_element == control and control_id in self.callbacks:
                    self.callbacks[control_id](self.get_value(control_id))
                    return True
        
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            for control_id, control in self.controls.items():
                if event.ui_element == control and control_id in self.callbacks:
                    self.callbacks[control_id](self.get_value(control_id))
                    return True
        
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            for control_id, control in self.controls.items():
                if event.ui_element == control and control_id in self.callbacks:
                    self.callbacks[control_id]()
                    return True
        
        return False
    
    def update(self, time_delta):
        """Update the UI"""
        if self.visible:
            self.ui_manager.update(time_delta)
    
    def draw(self):
        """Draw the control panel"""
        if self.visible:
            self.ui_manager.draw_ui(self.screen)