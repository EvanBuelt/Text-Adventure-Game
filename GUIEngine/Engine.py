__author__ = 'Evan'
import sys
import pygame
import random


class MouseButton:
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


class EventHandler:
    def __init__(self):
        self.functions = []

    def __iadd__(self, function):
        if function not in self.functions:
            self.functions.append(function)
        return self

    def __isub__(self, function):
        if function in self.functions:
            self.functions.remove(function)
        return self

    def notify(self, *args):
        for function in self.functions:
            function(*args)


class Engine:
    # Pygame Display
    DISPLAYSURFACE = None
    width = 0
    height = 0

    # Event handlers for various events, to be linked internally and externally
    mouseClick = EventHandler()
    cardClick = EventHandler()
    mouseMovement = EventHandler()
    keyPress = EventHandler()
    gameQuit = EventHandler()

    # List of UI Elements
    _UIElements = []

    def __init__(self):
        raise NotImplementedError("Engine cannot be instantiated.")

    @classmethod
    def init(cls, width=800, height=600, display_caption='UI Engine'):
        # Setup the pygame display for use in the Engine
        pygame.init()
        cls.width = width
        cls.height = height
        cls.DISPLAYSURFACE = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption(display_caption)

        cls._UIElements = []

        # Event handlers for various events to be linked externally
        cls.mouseClick = EventHandler()
        cls.cardClick = EventHandler()
        cls.mouseMovement = EventHandler()
        cls.keyPress = EventHandler()
        cls.gameQuit = EventHandler()

    @classmethod
    def update(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Notify other parts before closing the window and exiting program.
                cls.gameQuit.notify()
                pygame.quit()
                sys.exit()

            else:
                for ui_element in cls._UIElements:
                    ui_element.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    cls.mouseClick.notify(event)

                elif event.type == pygame.MOUSEBUTTONUP:
                    cls.mouseClick.notify(event)

                elif event.type == pygame.MOUSEMOTION:
                    cls.mouseMovement.notify(event)

                elif event.type == pygame.KEYDOWN:
                    cls.keyPress.notify(event)

                elif event.type == pygame.KEYUP:
                    cls.keyPress.notify(event)

    @classmethod
    def render(cls):
        cls.DISPLAYSURFACE.fill((70, 200, 70))
        cls._sort_ui_elements()
        for card in cls._UIElements:
            card.render(cls.DISPLAYSURFACE)
        pygame.display.update()

    # Methods below are used to handle the ui elements on screen.
    @classmethod
    def _sort_ui_elements(cls):
        for i in range(1, len(cls._UIElements)):
            j = i
            while (j > 0) and (cls._UIElements[j - 1].z > cls._UIElements[j].z):
                temp = cls._UIElements[j]
                cls._UIElements[j] = cls._UIElements[j - 1]
                cls._UIElements[j - 1] = temp
                j -= 1

    @classmethod
    def add_ui_element(cls, ui_element):
        if ui_element not in cls._UIElements:
            cls._UIElements.append(ui_element)

    @classmethod
    def remove_ui_element(cls, ui_element):
        if ui_element in cls._UIElements:
            cls._UIElements.remove(ui_element)

    @classmethod
    def remove_all_ui_elements(cls):
        del cls._UIElements[:]
