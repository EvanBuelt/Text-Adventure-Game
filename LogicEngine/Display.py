__author__ = 'Evan'
import pygame
import GUIEngine.UI as UI
import GUIEngine.CustomUI as CustomUI
import Joke


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
        self.button_return = GameScreen(self.engine)
        return

    def update(self):
        if (pygame.time.get_ticks() - self.start_time) > 6000:
            return LongestJokeScreen(self.engine)
        else:
            Screen.update(self)
            return self.button_return


class LongestJokeScreen(Screen):
    def __init__(self, engine):
        self.story_teller = Joke.LongestJokeTeller()
        self.text = CustomUI.MultiLineText(None, pygame.Rect(200, 200, 400, 200), 0, "")
        self.text_return = None
        Screen.__init__(self, engine, [self.text])

    def update(self):
        text = self.story_teller.update()
        if text is None:
            self.text_return = EndScreen(self.engine)
        else:
            self.text_return = None
            self.text.text = text
        Screen.update(self)
        return self.text_return


class GameScreen(Screen):
    def __init__(self, engine):
        text = CustomUI.MultiLineText(None, pygame.Rect(10, 10, 100, 100), 0, "This is a game.")
        self.text_return = None
        Screen.__init__(self, engine, [text])

    def update(self):
        Screen.update(self)
        return self.text_return


class EndScreen(Screen):
    def __init__(self, engine):
        text = CustomUI.MultiLineText(None, pygame.Rect(10, 10, 100, 100), 0, "This is the end.")
        Screen.__init__(self, engine, [text])

    def update(self):
        Screen.update(self)
        return None
