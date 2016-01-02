__author__ = 'Evan'
import pygame

pygame.font.init()
UI_FONT = gentiumBookBasic = pygame.font.Font(pygame.font.match_font('gentiumbookbasic'), 20)

BLACK = (0, 0, 0, 255)
DARKGRAY = (64, 64, 64, 255)
GRAY = (128, 128, 128, 255)
LIGHTGRAY = (140, 140, 140, 255)
LIGHTGRAY2 = (212, 208, 200, 255)
WHITE = (255, 255, 255, 255)
TRANSPARENT = (255, 255, 255, 0)
GREEN = (24, 119, 24, 255)


# InheritanceError is used to ensure certain class methods are inherited.  Used for UIElement.
class InheritanceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Base UI Element to be used with an engine.  This should be inherited by every UI Element, as the engine
# will expect to use the methods below.
class UIElement(object):
    def __init__(self, engine, rect, z):
        if engine is not None:
            engine.add_ui_element(self)

        # Every UI element will need an x, y, and z coordinate (in the form of a rect and z).
        # Every UI element will also need to know if it is visible or not.
        # Set location for text
        if rect is None:
            self._rect = pygame.Rect(0, 0, 60, 30)
        else:
            self._rect = pygame.Rect(rect)
        self._z = z
        self._visible = True

    # Used to render an image to the screen.
    def render(self, surface):
        raise InheritanceError('Function not defined')

    # Used to update the internal state of the UI Element.
    def _update(self):
        raise InheritanceError('Function not defined')

    # Used to set the location of the UI Element.
    def set_location(self, x, y, z):
        self._rect.topleft = (x, y)
        self._z = z
        self._update()

    # Used to handle a pygame event.
    def handle_event(self, event):
        raise InheritanceError('Function not defined')

    def collide(self, x, y):
        return self._rect.collidepoint(x, y)

    # Properties to access variables
    def _prop_get_rect(self):
        return self._rect

    def _prop_set_rect(self, new_rect):
        self._rect = pygame.Rect(new_rect)
        self._update()
        return

    def _prop_get_z(self):
        return self._z

    def _prop_set_z(self, new_z):
        self._z = new_z
        self._update()
        return

    def _prop_get_visible(self):
        return self._visible

    def _prop_set_visible(self, visible):
        self._visible = visible
        self._update()
        return

    rect = property(_prop_get_rect, _prop_set_rect)
    z = property(_prop_get_z, _prop_set_z)
    visible = property(_prop_get_visible, _prop_set_visible)


# The following classes are used as a base for common UI Elements.  The first way to handle UI Elements is to
# use a callback function, which will be triggered internally in reaction to pygame events.  The second way is to
# use inheritance to override several methods in the UI Element class.  These methods are called in the handle_event
# method that will call the overridden methods.

# As both classes share several commonalities, a base class is used.
# This base class is internal to the UI module, and cannot handle events,
# so it should not be referenced outside this module.

# Standard UI Elements:
# Text (Output)
# TextBox (Input)
# CheckBox (Input)
# Button (Input)

class _BaseText(UIElement):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=TRANSPARENT, text_color=BLACK, font=None):

        UIElement.__init__(self, engine, rect, z)

        # Set color of background and text color
        self._bgColor = background_color
        self._textColor = text_color

        if text is '':
            self._text = 'Text'
        else:
            self._text = text

        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # Create standard surface for text
        self._surfaceNormal = pygame.Surface(self._rect.size).convert_alpha()
        self._update()

    def render(self, surface):
        if self._visible:
            surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Make syntax pretty
        w = self._rect.width
        h = self._rect.height

        # Update surface to fit size of rect
        self._surfaceNormal = pygame.Surface(self._rect.size).convert_alpha()
        self._surfaceNormal.fill(self._bgColor)

        # Draw text on surface
        text_surf = self.font.render(self._text, True, self._textColor)
        text_rect = text_surf.get_rect()
        text_rect.center = int(w / 2), int(h / 2)
        self._surfaceNormal.blit(text_surf, text_rect)

    def handle_event(self, event):
        pass

    def _prop_get_text(self):
        return self._text

    def _prop_set_text(self, new_text):
        self._text = new_text
        self._update()
        return

    def _prop_get_font(self):
        return self._font

    def _prop_set_font(self, new_font):
        self._font = new_font
        self._update()
        return

    def _prop_get_background_color(self):
        return self._bgColor

    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()
        return

    def _prop_get_text_color(self):
        return self._textColor

    def _prop_set_text_color(self, new_text_color):
        self._textColor = new_text_color
        self._update()
        return

    text = property(_prop_get_text, _prop_set_text)
    text_color = property(_prop_get_text_color, _prop_set_text_color)
    font = property(_prop_get_font, _prop_set_font)
    background_color = property(_prop_get_background_color, _prop_set_background_color)


class _BaseTextBox(UIElement):
    def __init__(self, engine, rect=None, z=0, background_text=None, background_color=WHITE,
                 input_text_color=BLACK, background_text_color=LIGHTGRAY, font=None):

        UIElement.__init__(self, engine, rect, z)

        # Set values for surface display
        self._bgColor = background_color
        self._inputTextColor = input_text_color
        self._bgTextColor = background_text_color

        # Input text uses a list that is converted to a string (which is immutable)
        self._inputText = ''
        self._listInputText = []

        # Background text
        if background_text is None:
            self._bgText = 'Input'
        else:
            self._bgText = background_text

        # If no font is given, use gentium book, font size 12
        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # Track mouse click events and keyboard inputs
        self._isSelected = False
        self._lastMouseDownOverTextBox = False
        self._keydown = False

        # Create Surface
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceInput = pygame.Surface(self._rect.size)

        self._update()

    def render(self, surface):
        if self._visible:
            if self._inputText is not '':
                surface.blit(self._surfaceInput, self._rect)
            else:
                surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Syntactic sugar for height and width for text
        w = self._rect.width
        h = self._rect.height

        # Start with a clean slate for the surfaces with background color
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceInput = pygame.Surface(self._rect.size)

        self._surfaceNormal.fill(self._bgColor)
        self._surfaceInput.fill(self._bgColor)

        # Create background text
        bg_text_surf = self._font.render(self._bgText, True, self._bgTextColor, self._bgColor)
        bg_text_rect = bg_text_surf.get_rect()
        bg_text_rect.left = 5
        bg_text_rect.centery = int(h / 2)
        self._surfaceNormal.blit(bg_text_surf, bg_text_rect)

        # Create input text
        self._listInputText = [y for y in self._listInputText if y != '']
        self._inputText = str(''.join(self._listInputText))
        input_text_surf = self._font.render(self._inputText, True, self._inputTextColor, self._bgColor)
        input_text_rect = input_text_surf.get_rect()
        input_text_rect.left = 5
        input_text_rect.centery = int(h / 2)
        self._surfaceInput.blit(input_text_surf, input_text_rect)

        # Update normal surface used not selected and no input
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (1, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 1), (w - 2, h - 2))

        # Update input surface used for when selected or there is input
        pygame.draw.rect(self._surfaceInput, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self._surfaceInput, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceInput, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceInput, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceInput, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (1, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 1), (w - 2, h - 2))

    def handle_event(self, event):
        pass

    def _prop_set_background_text(self, new_background_text):
        self._bgText = new_background_text
        self._update()

    def _prop_get_background_text(self):
        return self._bgText

    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_background_color(self):
        return self._bgColor

    def _prop_set_input_text(self, new_input_text):
        self._listInputText = []
        for char in new_input_text:
            self._listInputText.append(char)

    def _prop_get_input_text(self):
        return self._inputText

    def _prop_set_input_text_color(self, new_input_text_color):
        self._inputTextColor = new_input_text_color
        self._update()

    def _prop_get_input_text_color(self):
        return self._inputTextColor

    def _prop_set_background_text_color(self, new_background_text_color):
        self._bgTextColor = new_background_text_color
        self._update()

    def _prop_get_background_text_color(self):
        return self._bgTextColor

    def _prop_set_font(self, new_font):
        self._font = new_font
        self._update()

    def _prop_get_font(self):
        return self._font

    backgroundText = property(_prop_get_background_text, _prop_set_background_text)
    backgroundTextColor = property(_prop_get_background_text_color, _prop_set_background_text_color)
    backgroundColor = property(_prop_get_background_color, _prop_set_background_color)
    inputText = property(_prop_get_input_text, _prop_set_input_text)
    inputTextColor = property(_prop_get_input_text_color, _prop_set_input_text_color)
    font = property(_prop_get_font, _prop_set_font)


class _BaseCheckBox(UIElement):
    def __init__(self, engine, rect=None, z=0, background_color=WHITE):
        # Set position of element

        UIElement.__init__(self, engine, rect, z)

        self._bgColor = background_color

        # Variables to track internal state in reaction to events
        self._isChecked = False
        self._lastMouseDownOverCheckBox = False

        # Images to be displayed on screen
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceChecked = pygame.Surface(self._rect.size)

        self._update()

    def render(self, surface):
        if self._visible:
            if self._isChecked:
                surface.blit(self._surfaceChecked, self._rect)
            else:
                surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Create blank surfaces to be drawn upon
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceChecked = pygame.Surface(self._rect.size)

        # Syntactic sugar
        w = self._rect.width
        h = self._rect.height

        # Create unchecked surface
        self._surfaceNormal.fill(self._bgColor)
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((1, 1, w - 2, h - 2)), 1)

        # Create checked surface
        self._surfaceChecked.fill(self._bgColor)
        pygame.draw.rect(self._surfaceChecked, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.rect(self._surfaceChecked, BLACK, pygame.Rect((1, 1, w - 2, h - 2)), 1)
        pygame.draw.line(self._surfaceChecked, GREEN, (3, int(h / 2)), (int(w / 2), h - 5), 3)
        pygame.draw.line(self._surfaceChecked, GREEN, (int(w / 2), h - 5), (w - 5, 4), 3)

    def handle_event(self, event):
        pass

    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_background_color(self):
        return self._bgColor

    def _prop_set_is_checked(self, is_checked):
        self._isChecked = is_checked
        self._update()

    def _prop_get_is_checked(self):
        return self._isChecked

    backgroundColor = property(_prop_get_background_color, _prop_set_background_color)
    checked = property(_prop_get_is_checked, _prop_set_is_checked)


class _BaseButton(UIElement):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=LIGHTGRAY, foreground_color=BLACK, font=None):

        UIElement.__init__(self, engine, rect, z)

        # set text and color to be applied to blank surfaces
        self._text = text
        self._bgColor = background_color
        self._fgColor = foreground_color

        # set font for text
        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # create blank surfaces to be created in update
        pygame.Surface((200, 300))
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceDown = pygame.Surface(self._rect.size)
        self._surfaceHighlight = pygame.Surface(self._rect.size)

        # tracks the state of the button
        self._buttonDown = False  # is the button currently pushed down?
        self._mouseOverButton = False  # is the mouse currently hovering over the button?
        self._lastMouseDownOverButton = False  # was the last mouse down event over the mouse button? (Tracks clicks.)

        # update graphics for the button
        self._update()

    def render(self, surface):
        if self._visible:
            if self._buttonDown:
                surface.blit(self._surfaceDown, self._rect)
            elif self._mouseOverButton:
                surface.blit(self._surfaceHighlight, self._rect)
            else:
                surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceDown = pygame.Surface(self._rect.size)
        self._surfaceHighlight = pygame.Surface(self._rect.size)

        # syntactic sugar
        w = self._rect.width
        h = self._rect.height

        # fill background color for all buttons
        self._surfaceNormal.fill(self._bgColor)
        self._surfaceDown.fill(self._bgColor)
        self._surfaceHighlight.fill(self._bgColor)

        # draw caption text for all buttons
        caption_surf = self._font.render(self._text, True, self._fgColor, self._bgColor)
        caption_rect = caption_surf.get_rect()
        caption_rect.center = int(w / 2), int(h / 2)
        self._surfaceNormal.blit(caption_surf, caption_rect)
        self._surfaceDown.blit(caption_surf, caption_rect)

        # draw border for normal button
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self._surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self._surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self._surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self._surfaceDown, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        self._surfaceHighlight = self._surfaceNormal

    def get_text(self):
        return self._text

    def set_text(self, new_text):
        self._text = new_text

    def handle_event(self, event):
        pass

    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_background_color(self):
        return self._bgColor

    def _prop_set_foreground_color(self, new_foreground_color):
        self._fgColor = new_foreground_color
        self._update()

    def _prop_get_foreground_color(self):
        return self._fgColor

    def _prop_set_font(self, new_font):
        self._visible = new_font
        self._update()

    def _prop_get_font(self):
        return self._font

    def _prop_set_text(self, new_text):
        self._text = new_text
        self._update()

    def _prop_get_text(self):
        return self._text

    foregroundColor = property(_prop_get_foreground_color, _prop_set_foreground_color)
    backgroundColor = property(_prop_get_background_color, _prop_set_background_color)
    font = property(_prop_get_font, _prop_set_font)
    text = property(_prop_get_text, _prop_set_text)


# The following UI Elements use a callback function
class Text(_BaseText):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=TRANSPARENT, text_color=BLACK, font=None):
        # Let base handle most of initialization.  Base class should call _update.
        _BaseText.__init__(self, engine, rect, z, text,
                           background_color, text_color, font)


class TextBox(_BaseTextBox):
    def __init__(self, engine, rect=None, z=0, background_text=None, background_color=WHITE,
                 input_text_color=BLACK, background_text_color=LIGHTGRAY,
                 font=None, callback_function=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseTextBox.__init__(self, engine, rect, z, background_text, background_color,
                              input_text_color, background_text_color, font)

        # Set callback function.
        self._callbackFunction = callback_function

    def set_callback(self, new_callback_function):
        # Set the callback function to be called upon user hitting the enter key
        self._callbackFunction = new_callback_function

    def handle_event(self, event):
        # Track only mouse presses and key presses
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if self._rect.collidepoint(event.pos):
                # clicking and releasing inside textbox selects textbox
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverTextBox = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverTextBox:
                        self._isSelected = True
                    self._lastMouseDownOverTextBox = False
            else:
                # releasing mouse outside textbox deselects textbox
                self._lastMouseDownOverTextBox = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self._isSelected = False

        if event.type is pygame.KEYDOWN and self._isSelected:
            if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                if len(self._listInputText) > 0:
                    self._listInputText.pop()

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                pass  # Future update.  Allow user to move cursor location

            elif event.key in (pygame.K_TAB, pygame.K_ESCAPE):
                pass  # Events to ignore

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self._callbackFunction is not None:
                    self._callbackFunction(self)

            else:
                self._listInputText.append(event.unicode)

        self._update()

    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)


class CheckBox(_BaseCheckBox):
    def __init__(self, engine, rect=None, z=0, background_color=WHITE, callback_function=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseCheckBox.__init__(self, engine, rect, z, background_color)

        # Set function to be called when checked or unchecked
        self._callbackFunction = callback_function

    def set_callback(self, new_callback_function):
        # Set the callback function to be called upon checkbox changing checked state
        self._callbackFunction = new_callback_function

    def handle_event(self, event):
        # Track only mouse presses and key presses
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self._visible:
            return

        if self._rect.collidepoint(event.pos):
            # clicking and releasing inside checkbox toggles check
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._lastMouseDownOverCheckBox = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._lastMouseDownOverCheckBox and self._isChecked:
                    self._isChecked = False
                    if self._callbackFunction is not None:
                        self._callbackFunction(self)
                elif self._lastMouseDownOverCheckBox and not self._isChecked:
                    self._isChecked = True
                    if self._callbackFunction is not None:
                        self._callbackFunction(self)
                self._lastMouseDownOverCheckBox = False
        else:
            self._lastMouseDownOverCheckBox = False

        self._update()

    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)


class Button(_BaseButton):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=LIGHTGRAY, foreground_color=BLACK, font=None,
                 callback_function=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseButton.__init__(self, engine, rect, z, text,
                             background_color, foreground_color, font)

        # Set callback if provided
        self._callbackFunction = callback_function

    def set_callback(self, new_callback_function):
        # Set the callback function to be called upon checkbox changing checked state
        self._callbackFunction = new_callback_function

    def handle_event(self, event):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self._visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return

        if not self._mouseOverButton and self._rect.collidepoint(event.pos):
            # if mouse has entered the button:
            self._mouseOverButton = True
        elif self._mouseOverButton and not self._rect.collidepoint(event.pos):
            # if mouse has exited the button:
            self._mouseOverButton = False

        if self._rect.collidepoint(event.pos):
            # if mouse event happened over the button:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._buttonDown = True
                self._lastMouseDownOverButton = True
        else:
            if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self._lastMouseDownOverButton = False

        # mouse up is handled whether or not it was over the button
        do_mouse_click = False
        if event.type == pygame.MOUSEBUTTONUP:
            if self._lastMouseDownOverButton:
                do_mouse_click = True
                self._lastMouseDownOverButton = False

            if self._buttonDown:
                self._buttonDown = False

            if do_mouse_click:
                self._buttonDown = False
                if self._callbackFunction is not None:
                    self._callbackFunction(self)

        self._update()

    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)


# UI Elements below, denoted with a prefix of Py-, are intended to be inherited.
# Several methods have been set up, but not defined.  These methods are to be handled by the programmer.

# The following methods are to be overwritten as necessary:
#   -mouse_click: called when mouse clicked.
#   -mouse_enter: called when mouse entered UI Element
#   -mouse_exit: called when mouse no longer over UI Element
#   -mouse_down: called when mouse pressed
#   -mouse_up: called when mouse released
#   -keyboard_down: called when key pressed
#   -keyboard_up: called when key released


class PyText(_BaseText):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=TRANSPARENT, text_color=BLACK, font=None):
        # Let base handle most of initialization.  Base class should call _update.
        _BaseText.__init__(self, engine, rect, z, text,
                           background_color, text_color, font)

        self._mouseOverText = False
        self._lastMouseDownOverText = False
        self._isSelected = False

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        do_mouse_click = False

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverText and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverText = True
                self.mouse_enter(event)
            elif self._mouseOverText and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverText = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self._rect.collidepoint(event.pos):
                # if mouse event happened over the check box:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)

                # clicking and releasing inside textbox selects it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverText = True
                    self.mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverText:
                        self._isSelected = True
                        do_mouse_click = True
                    self._lastMouseDownOverText = False
                    self.mouse_up(event)
            else:
                # releasing mouse click outside textbox deselects it
                self._lastMouseDownOverText = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self._isSelected = False

            if do_mouse_click:
                self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)

        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass


class PyTextBox(_BaseTextBox):
    def __init__(self, engine, rect=None, z=0, background_text=None, background_color=WHITE,
                 input_text_color=BLACK, background_text_color=LIGHTGRAY, font=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseTextBox.__init__(self, engine, rect, z, background_text, background_color,
                              input_text_color, background_text_color, font)

        self._mouseOverTextBox = False

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        do_mouse_click = False

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverTextBox and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverTextBox = True
                self.mouse_enter(event)
            elif self._mouseOverTextBox and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverTextBox = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self._rect.collidepoint(event.pos):
                # if mouse event happened over the check box:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)

                # clicking and releasing inside textbox selects it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverTextBox = True
                    self.mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverTextBox:
                        self._isSelected = True
                        do_mouse_click = True
                    self._lastMouseDownOverTextBox = False
                    self.mouse_up(event)
            else:
                # releasing mouse click outside textbox deselects it
                self._lastMouseDownOverTextBox = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self._isSelected = False

            if do_mouse_click:
                self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)

        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass


class PyCheckBox(_BaseCheckBox):
    def __init__(self, engine, rect=None, z=0, background_color=WHITE):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseCheckBox.__init__(self, engine, rect, z, background_color)

        # Variables to be used in handling events
        self._mouseOverCheckBox = False

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        do_mouse_click = False

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverCheckBox and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverCheckBox = True
                self.mouse_enter(event)
            elif self._mouseOverCheckBox and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverCheckBox = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self._rect.collidepoint(event.pos):
                # if mouse event happened over the check box:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)

                # clicking and releasing inside checkbox toggles check
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverCheckBox = True
                    self.mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverCheckBox and self._isChecked:
                        self._isChecked = False
                        do_mouse_click = True
                    elif self._lastMouseDownOverCheckBox and not self._isChecked:
                        self._isChecked = True
                        do_mouse_click = True
                    self._lastMouseDownOverCheckBox = False
                    self.mouse_up(event)
            else:
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    self._lastMouseDownOverCheckBox = False

            if do_mouse_click:
                self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)

        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass


class PyButton(_BaseButton):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=LIGHTGRAY, foreground_color=BLACK, font=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseButton.__init__(self, engine, rect, z, text,
                             background_color, foreground_color, font)

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverButton and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverButton = True
                self.mouse_enter(event)
            elif self._mouseOverButton and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverButton = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self.rect.collidepoint(event.pos):
                # if mouse event happened over the button:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._buttonDown = True
                    self._lastMouseDownOverButton = True
                    self.mouse_down(event)
            else:
                if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                    # if an up/down happens off the button, then the next up won't cause mouseClick()
                    self._lastMouseDownOverButton = False

            # mouse up is handled whether or not it was over the button
            do_mouse_click = False
            if event.type == pygame.MOUSEBUTTONUP:
                if self._lastMouseDownOverButton:
                    do_mouse_click = True
                self._lastMouseDownOverButton = False

                if self._buttonDown:
                    self._buttonDown = False
                    self.mouse_up(event)

                if do_mouse_click:
                    self._buttonDown = False
                    self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)
        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass
