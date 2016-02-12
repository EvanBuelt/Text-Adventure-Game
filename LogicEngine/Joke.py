__author__ = 'Evan'
import pygame


class LongestJokeTeller:
    def __init__(self):
        joke_file = open('Longest Joke Ever.txt', 'r')
        self.joke = joke_file.read()
        self.joke = self.joke.split('\n')

        # Set up timing for telling the joke, in milliseconds.  Minimum Line Time should be set so short texts
        # are on the screen long enough.  ~1200 ms seems to be a good starting point.
        # Average words per second is 5, so Time Per Word is set to 200 ms.
        # Line Delay is time between displaying different lines.  100 ms seems to be a good starting point.
        self.fade_delay = 300
        self.wait_delay = 500
        self.time_per_word = 200
        self.minimum_line_time = 1200

        # Get current time
        self.previous_time = pygame.time.get_ticks()

        # Get first line
        self.current_line = ""
        self.current_line_time = self.minimum_line_time

        self.state = "Start"
        return

    def update(self):
        if self.state == "Start":
            if pygame.time.get_ticks() - self.previous_time > 2000:
                self.previous_time = pygame.time.get_ticks()
                print self.state, pygame.time.get_ticks(), 2000
                self.state = "Fade in"

        elif self.state == "Fade out":
            if pygame.time.get_ticks() - self.previous_time > self.fade_delay:
                self.previous_time = pygame.time.get_ticks()
                print self.state, pygame.time.get_ticks(), self.fade_delay
                self.state = "Wait"
            else:
                self.current_line = ""

        elif self.state == "Wait":
            if pygame.time.get_ticks() - self.previous_time > self.wait_delay:
                self.previous_time = pygame.time.get_ticks()
                print self.state, pygame.time.get_ticks(), self.wait_delay
                self.state = "Fade in"
            else:
                self.current_line = ""

        elif self.state == "Fade in":
            if pygame.time.get_ticks() - self.previous_time > self.fade_delay:
                self.current_line = self.joke.pop(0)
                self.current_line_time = self.get_line_time(self.current_line)
                self.previous_time = pygame.time.get_ticks()
                print self.state, pygame.time.get_ticks(), self.fade_delay
                self.state = "Display"
            else:
                self.current_line = ""

        elif self.state == "Display":
            if pygame.time.get_ticks() - self.previous_time > self.current_line_time:
                self.previous_time = pygame.time.get_ticks()
                print self.state, pygame.time.get_ticks(), self.current_line_time
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