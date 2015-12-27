__author__ = 'Evan'
import pygame
import GUIEngine.Engine as Engine
import GUIEngine.UI as UI


def button_press(button):
    print button.text
    return


class TextDisplay:
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height
        return


# Initialize Graphics Engine
GUI_Engine = Engine.Engine
GUI_Engine.init(800, 600, "My text Adventure")

# Create a button
main_button = UI.Button(GUI_Engine, pygame.Rect(200, 200, 60, 30), 0, 'Start')
main_button.callbackFunction = button_press


main_text = UI.Text(GUI_Engine, pygame.Rect(400, 400, 200, 200), 0,
                    'This is text.\nThis should be another line')

while True:
    GUI_Engine.update()
    GUI_Engine.render()
