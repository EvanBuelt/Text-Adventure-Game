__author__ = 'Evan'
import pygame
import GUIEngine.Engine as Engine
import GUIEngine.UI as UI
import GUIEngine.CustomUI as customUI


def button_press(button):
    print button.text
    return

dark_blue = (41, 86, 143)

# Initialize Graphics Engine
GUI_Engine = Engine.Engine
GUI_Engine.init(800, 600, dark_blue, "My text Adventure")

# Create a button
main_button = UI.Button(GUI_Engine, pygame.Rect(200, 200, 60, 30), 0, 'Start')
main_button.callbackFunction = button_press

# Create text
custom_text = customUI.MultiLineText(GUI_Engine, pygame.Rect(0, 0, 400, 200), 0,
                                     'This is a really, really, really, really, long text. If it is not, '
                                     'it will not show multiple lines.')

clock = pygame.time.Clock()

while True:
    GUI_Engine.update()
    GUI_Engine.render()
    clock.tick(30)
