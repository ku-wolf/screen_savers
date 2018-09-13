#!/usr/bin/python3
"""Tracer Game."""

from kutils4pygame import Game, Animation
from pygame import Surface
import random

l = 1200
w = 1200
fps = 100


class TracerGame(Game):
    """Base class for TracerGame."""

    def __init__(self, screen_w, screen_h, fps, band_number=4):
        """Init TracerGame."""
        super().__init__(screen_w, screen_h, fps)
        self.gen_tracer = self._gen_tracer(self.gen_edge_coords())
        self.current_tracer = next(self.gen_tracer)

    def gen_edge_coords(self):
        """Generate all coordinates along the edge of the screen."""
        point_list = []
        for x in range(self.screen_w):
            point_list.append((x, 0))
            point_list.append((x, self.screen_h))

        for y in range(self.screen_h):
            point_list.append((0, y))
            point_list.append((self.screen_w, y))

        return point_list

    def _gen_tracer(self, coord_list):
        """Generate the next tracer."""
        while True:
            random.shuffle(coord_list)
            for coord in coord_list:
                new_tracer = Tracer(coord[0], coord[1], self.screen_w, self.screen_h)
                self.display.board[(coord[0], coord[1])] = new_tracer
                yield new_tracer

    def run(self):
        """Run tracer game create new tracer once gone offscreen."""
        if self.current_tracer.dead():
            self.current_tracer = next(self.gen_tracer)

        super().run()


class Tracer(Animation):
    """Tracer object."""

    change_direction_probability = 0.01

    def __init__(self, x, y, max_x, max_y, w=1, h=1):
        """Init tracer at initial x, y."""
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.surface = Surface((w, h))
        self.surface.fill((255, 255, 255))
        self.ver_direction_functions = [self.up, self.down]
        self.hor_direction_functions = [self.left, self.right]
        self.direction_x = None
        self.direction_y = None
        self.set_initial_direction()
        super().__init__(x, y, w, h)

    def set_initial_direction(self):
        """Set initial direction based on starting edge."""
        if self.x == 0:
            self.direction_x = self.right
            for i in range(5):
                self.hor_direction_functions.append(self.direction_x)
        if self.x == self.max_x:
            self.direction_x = self.left
            for i in range(5):
                self.hor_direction_functions.append(self.direction_x)
        if self.y == 0:
            self.direction_y = self.down
            for i in range(5):
                self.ver_direction_functions.append(self.direction_y)
        if self.y == self.max_y:
            self.direction_y = self.up
            for i in range(5):
                self.ver_direction_functions.append(self.direction_y)

    def up(self):
        """Move tracer up."""
        self.y -= self.h

    def down(self):
        """Move tracer down."""
        self.y += self.h

    def left(self):
        """Move tracer left."""
        self.x -= self.w

    def right(self):
        """Move tracer right."""
        self.x += self.w

    def switch_direction(self):
        """Switch direction with certain probability."""
        if random.random() < Tracer.change_direction_probability:
            index = random.randint(0, len(self.hor_direction_functions) - 1)
            self.direction_x = self.hor_direction_functions[index]
            index = random.randint(0, len(self.ver_direction_functions) - 1)
            self.direction_y = self.ver_direction_functions[index]

    def move(self):
        """Move cascade downwards."""
        self.switch_direction()
        if self.direction_x:
            self.direction_x()
        if self.direction_y:
            self.direction_y()

    def get_image(self):
        """Get cascade image."""
        return self.surface

    def degrade(self):
        """Determine if cascade should die."""
        offscreen = self.y > self.max_y or self.x > self.max_x or self.x < 0 or self.y < 0
        if offscreen:
            self.is_dead = True

    def die(self, display):
        """Dummy."""
        pass


def main():
    """Run tracer game."""
    game = TracerGame(w, l, fps)
    game.start()

if __name__ == "__main__":
    main()
