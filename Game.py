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

# Create initial screen.  Transitions will be taken care of from initial screen
initial_screen = customUI.InitialScreen(GUI_Engine)
screen_machine = customUI.ScreenStateMachine(initial_screen)

clock = pygame.time.Clock()

while True:
    GUI_Engine.update()
    GUI_Engine.render()
    screen_machine.update()
    clock.tick(30)
