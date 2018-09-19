#!/usr/bin/python3
"""Matrix screen saver."""

import os
from pygame import font
from kutils4pygame import Game, Animation
import random
from provision_py_proj.data_and_config_manager import create_data_dir_location
from screen_savers.pkg_utils import pkg_name

l = 1200
w = 1600
fps = 50
font.init()


class MatrixGame(Game):
    """Base class for MatrixGame."""

    @staticmethod
    def gen_coords(area_width, area_height):
        """Generate all pairs of coordinates."""
        return [(x, 0) for x in range(0, area_width, Cascade.get_width())]

    def __init__(self, screen_w, screen_h, fps, band_number=4):
        """Init MatrixGame."""
        self.cascades = []
        self.band_number = band_number
        super().__init__(screen_w, screen_h, fps)
        self.gen_cascade = self._gen_cascade(self.gen_coords(screen_w,
                                                             screen_h))

    def _gen_cascade(self, coord_list):
        """Generate the next cascade."""
        while True:
            random.shuffle(coord_list)
            for coord in coord_list:
                cascade = None
                while cascade is None:
                    cascade = Cascade(coord[0], coord[1], self.display)
                    yield cascade

    def run(self):
        """Run matrixgame, create and add cascades."""
        new_cascade = next(self.gen_cascade)
        if new_cascade:
            self.display.board[(new_cascade.x, new_cascade.y)] = new_cascade
        super().run()


class Cascade(Animation):
    """Cascade object."""

    frames_per_drip = 2
    frames_per_cascade = 1
    frames_since_new_cascade = frames_per_cascade
    keep_dripping_probability = 0.999

    @classmethod
    def get_frames_per_drip(cls):
        """Return static variable represent animation speed."""
        return cls.frames_per_drip

    @staticmethod   
    def get_height():
        """Return static variable char_height."""
        return Twitcher.char_height

    @staticmethod
    def get_width():
        """Return static variable char_height."""
        return Twitcher.char_width

    def __new__(cls, x, y, display):
        """Make new cascade if certain number of frames have passed."""
        if cls.frames_since_new_cascade >= cls.frames_per_cascade:
            cls.frames_since_new_cascade = 0
            return super().__new__(cls)
        cls.frames_since_new_cascade += 1
        return None

    def __init__(self, x, y, display):
        """Init cascade at initial x, y."""
        self.animations_till_death = random.randint(40, 60) * self.get_frames_per_drip()
        self.display = display
        super().__init__(x, y,
                         self.get_width(),
                         self.get_height(),
                         self.get_frames_per_drip())

    def leave_twitcher(self):
        """Create twitcher at current location."""
        new_twitcher = Twitcher(self.x,
                                self.y,
                                self.animations_till_death,
                                Twitcher.get_trailing_colour(),
                                self.fpi)
        self.display.board[(self.x, self.y)] = new_twitcher

    def move(self):
        """Move cascade downwards."""
        self.leave_twitcher()
        self.y += self.get_height()
        self.display.board[(self.x, self.y)] = self

    def get_image(self):
        """Get cascade image."""
        return Twitcher.render_random_char(Twitcher.get_initial_colour())

    def degrade(self):
        """Determine if cascade should die."""
        offscreen = self.y > self.display.screen_h
        roll_dice = random.random() > self.keep_dripping_probability
        if offscreen or roll_dice:
            self.is_dead = True

    def die(self, display):
        """Die leaves twitcher at current x,y."""
        self.leave_twitcher()


class Twitcher(Animation):
    """Changes character blitted at (x, y)."""

    char_height = 10
    char_width = 10
    font_name = "metlrebl.ttf"
    font_location = os.path.join(create_data_dir_location(pkg_name), font_name)
    font = font.Font(font_location, 7)
    font_val_min = 33
    font_val_max = 126
    initial_col = (255, 255, 255)
    green_range_min = 255
    green_range_max = 255

    @classmethod
    def get_random_char(cls):
        """Get random char in range of twitcher font."""
        return bytes([random.randint(cls.font_val_min, cls.font_val_max)])

    @classmethod
    def render_random_char(cls, colour):
        """Render random char in font's range."""
        char = cls.get_random_char()
        return cls.font.render(char, True, colour)

    @classmethod
    def render_current_char(cls, self):
        """Return random char in font's range."""
        return cls.font.render(self.char, True, self.colour)

    @classmethod
    def get_trailing_colour(cls):
        """Return initial colour."""
        g = random.randint(cls.green_range_min, cls.green_range_max)
        return (0, g, 0)

    @classmethod
    def get_initial_colour(cls):
        """Return trailing colour."""
        return cls.initial_col

    @classmethod
    def get_width(cls):
        """Return width."""
        return cls.char_width

    @classmethod
    def get_height(cls):
        """Return height."""
        return cls.char_height

    def __init__(self, x, y, frames_til_death, col=None, delay=0):
        """Calculate random frames per image and create Animation."""
        if col:
            self.colour = col
        else:
            self.colour = self.get_initial_colour()
        fpi = random.randint(10, 300)
        self.frames_til_death = frames_til_death
        super().__init__(x, y, self.get_width(), self.get_height(), fpi, delay)

    def set_random_char(self):
        """Set last character to fade out on."""
        self.char = Twitcher.get_random_char()

    def degrade(self):
        """Determine if twitcher dead."""
        rate = 1
        if self.dying:
            rate = 15
        self.frames_til_death -= rate

        if not self.dying and self.frames_til_death <= 0:
            self.fpi = 1
            self.set_random_char()
            self.dying = True
            self.frames_til_death = 200

        if self.dying:
            self.colour = (0, self.frames_til_death, 0)

        if self.frames_til_death <= 0:
            self.is_dead = True

    def get_image(self):
        """Randomly select character from font."""
        if not self.dying:
            return self.render_random_char(self.colour)
        return self.render_current_char(self)


def main():
    """Start matrix screen_saver."""
    game = MatrixGame(w, l, fps)
    game.start()

if __name__ == "__main__":
    main()


# TO DO:
# Make die less often
# Make auto full screen
# Set alternate tracer position
