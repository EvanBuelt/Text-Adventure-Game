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


class LongestJokeTeller:
    def __init__(self):
        joke_file = open('Longest Joke Ever.txt', 'r')
        self.joke = joke_file.read()
        self.joke = self.joke.split('\n')

        # Set time between displaying lines to 1s (1000 ms), time per word as 0.4s (400 ms), and minimum
        # line time to 3s (3000 ms)
        self.line_delay = 1000
        self.time_per_word = 250
        self.minimum_line_time = 500

        # Get current time
        self.previous_time = pygame.time.get_ticks()

        # Get first line
        self.current_line = ""
        self.current_line_time = self.minimum_line_time

        self.state = "Start"
        return

    def update(self):
        if self.state == "Start":
            self.previous_time = pygame.time.get_ticks()
            self.state = "Fade in"

        elif self.state == "Fade in":
            if pygame.time.get_ticks() - self.previous_time > (self.line_delay / 2):
                self.current_line = self.joke.pop(0)
                self.current_line_time = self.get_line_time(self.current_line)
                self.previous_time = pygame.time.get_ticks()
                self.state = "Display"
            else:
                self.current_line = ""

        elif self.state == "Fade out":
            if pygame.time.get_ticks() - self.previous_time > (self.line_delay / 2):
                self.previous_time = pygame.time.get_ticks()
                self.state = "Fade in"
            else:
                self.current_line = ""

        elif self.state == "Display":
            if pygame.time.get_ticks() - self.previous_time > self.current_line_time:
                self.previous_time = pygame.time.get_ticks()
                self.state = "Fade out"

        if len(self.joke) > 0:
            return self.current_line
        else:
            return None

    def get_line_time(self, line):
        # Get words in line
        words = line.split(' ')

        # Get time to read line, plus the minimum time to read the line
        time = len(words) * self.time_per_word
        time += self.minimum_line_time
        return time


class ScreenStateMachine:
    def __init__(self, initial_screen):
        self._states = []
        self._active_state = initial_screen
        self._active_state.enter()
        self._next_state = None

    def add_screen(self, screen):
        if screen not in self._states:
            self._states.append(screen)
        return

    def remove_screen(self, screen):
        if screen in self._states:
            self._states.remove(screen)
        return

    def update(self):
        self._next_state = self._active_state.update()
        if self._next_state is not None:
            self._active_state.exit()
            self._active_state = self._next_state
            self._active_state.enter()
        return


class Screen:
    def __init__(self, engine, ui_element_list=None):
        if ui_element_list is None:
            self.ui_element_list = []
        else:
            self.ui_element_list = ui_element_list
        self.engine = engine
        return

    def update(self):
        return None

    def enter(self):
        for ui_element in self.ui_element_list:
            self.engine.add_ui_element(ui_element)
        return

    def exit(self):
        for ui_element in self.ui_element_list:
            self.engine.remove_ui_element(ui_element)
        return


class InitialScreen(Screen):
    def __init__(self, engine):
        button = UI.Button(None, pygame.Rect(int(engine.width/2) - 30, int(engine.height/2) - 15, 60, 30), 0, 'Start')
        button.callbackFunction = self.handle_button_event
        self.button_return = None
        self.start_time = pygame.time.get_ticks()
        self.current_time = self.start_time
        Screen.__init__(self, engine, [button])

    def handle_button_event(self, button):
        self.button_return = LongestJokeScreen(self.engine)
        return

    def update(self):
        if (pygame.time.get_ticks() - self.start_time) > 6000:
            return LongestJokeScreen(self.engine)
        else:
            Screen.update(self)
            return self.button_return


class LongestJokeScreen(Screen):
    def __init__(self, engine):
        self.story_teller = LongestJokeTeller()
        self.text = MultiLineText(None, pygame.Rect(200, 200, 400, 200), 0, "")
        self.text_return = None
        Screen.__init__(self, engine, [self.text])

    def update(self):
        text = self.story_teller.update()
        if text is None:
            self.text_return = None
        else:
            self.text.text = text
        Screen.update(self)
        return self.text_return


class GameScreen(Screen):
    def __init__(self, engine):
        text = MultiLineText(None, pygame.Rect(10, 10, 100, 100), 0, "This is a game")
        self.text_return = None
        Screen.__init__(self, engine, [text])

    def update(self):
        Screen.update(self)
        return self.text_return


class EndScreen(Screen):
    def __init__(self, engine):
        text = MultiLineText(None, pygame.Rect(10, 10, 100, 100), 0, "This is a game")
        Screen.__init__(self, engine, [text])

    def update(self):
        Screen.update()
        return None
