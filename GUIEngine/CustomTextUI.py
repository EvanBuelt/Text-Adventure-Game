__author__ = 'Evan'
import pygame
import UI


class _BaseMultiLineText(UI.UIElement):
    def __init__(self, engine, rect=None, z=0, text='',
                 background_color=UI.TRANSPARENT, text_color=UI.BLACK, font=None):

        UI.UIElement.__init__(self, engine)

        # Set location for text
        if rect is None:
            self._rect = pygame.Rect(0, 0, 60, 30)
        else:
            self._rect = pygame.Rect(rect)
        self._z = z

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

        self._visible = True

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

    def set_location(self, x, y, z):
        self._rect.topleft = (x, y)
        self._z = z
        self._update()

    def handle_event(self, event):
        pass

    def _prop_get_text(self):
        return self._text

    def _prop_set_text(self, new_text):
        self._text = new_text
        self._update()
        return

    def _prop_get_rect(self):
        return self._rect

    def _prop_set_rect(self, new_rect):
        self._rect = pygame.Rect(new_rect)
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

    def _prop_get_visible(self):
        return self._visible

    def _prop_set_visible(self, visible):
        self._visible = visible
        self._update()
        return

    def _prop_get_z(self):
        return self.z

    def _prop_set_z(self, new_z):
        self._z = new_z
        self._update()
        return

    rect = property(_prop_get_rect, _prop_set_rect)
    z = property(_prop_get_z, _prop_set_z)
    text = property(_prop_get_text, _prop_set_text)
    text_color = property(_prop_get_text_color, _prop_set_text_color)
    font = property(_prop_get_font, _prop_set_font)
    background_color = property(_prop_get_background_color, _prop_set_background_color)
    visible = property(_prop_get_visible, _prop_set_visible)
