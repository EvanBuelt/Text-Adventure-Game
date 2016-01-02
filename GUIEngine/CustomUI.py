__author__ = 'Evan'
import pygame
import UI


class _BaseMultiLineText(UI.UIElement):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=UI.TRANSPARENT, text_color=UI.BLACK, font=None):

        UI.UIElement.__init__(self, engine, rect, z)

        # Set color of background and text color
        self._bgColor = background_color
        self._textColor = text_color

        if text is '':
            self._text = 'Text'
        else:
            self._text = text

        if font is None:
            self._font = UI.UI_FONT
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

        # Update surface to fit size of rect
        self._surfaceNormal = pygame.Surface(self._rect.size).convert_alpha()
        self._surfaceNormal.fill(self._bgColor)

        # Draw text on surface
        split_text = self._text.split(' ')
        line = ''
        offset = self.font.get_height()
        h_offset = 0

        # Fit as many words into one line as possible and print it
        for word in split_text:
            if self.font.size((line + ' ' + word).strip(' '))[0] < w:
                line = (line + ' ' + word).strip(' ')
            else:
                text_surf = self.font.render(line, True, self._textColor)
                text_rect = text_surf.get_rect()
                text_rect.top = int(h_offset)
                self._surfaceNormal.blit(text_surf, text_rect)
                line = word
                h_offset = h_offset + offset

        # Print last line, as the for loop won't
        text_surf = self.font.render(line, True, self._textColor)
        text_rect = text_surf.get_rect()
        text_rect.top = int(h_offset)
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


class MultiLineText(_BaseMultiLineText):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=UI.TRANSPARENT, text_color=UI.BLACK, font=None):
        # Let base handle most of initialization.  Base class should call _update.
        _BaseMultiLineText.__init__(self, engine, rect, z, text,
                                    background_color, text_color, font)

        # Update just in case.
        self._update()


class PyMultiLineText(_BaseMultiLineText):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=UI.TRANSPARENT, text_color=UI.BLACK, font=None):
        # Let base handle most of initialization.  Base class should call _update.
        _BaseMultiLineText.__init__(self, engine, rect, z, text,
                                    background_color, text_color, font)

        self._mouseOverText = False
        self._lastMouseDownOverText = False
        self._isSelected = False

        # Update just in case.
        self._update()

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


class Screen:
    def __init__(self, ui_element_list=None):
        if ui_element_list is None:
            self.ui_element_list = []
        return

    def handle_event(self, event):
        for ui_element in self.ui_element_list:
            ui_element.handle_event(event)
        return

    def enter(self):
        for ui_element in self.ui_element_list:
            ui_element.visible = True
        return

    def exit(self):
        for ui_element in self.ui_element_list:
            ui_element.visible = False
        return


class ScreenStateMachine:
    def __init__(self, initial_screen):
        self._states = []
        self._active_state = initial_screen
        self._next_state = self._active_state

    def add_screen(self, screen):
        if screen not in self._states:
            self._states.append(screen)
        return

    def remove_screen(self, screen):
        if screen in self._states:
            self._states.remove(screen)
        return

    def transition_state(self, x):
        return