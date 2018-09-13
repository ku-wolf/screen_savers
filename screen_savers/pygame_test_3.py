#!/usr/bin/python3
"""Pygame test."""

from pygame import *
import sys
import random


def main():
    """Fill screen with text of random colour."""
    font.init()
    l = 800
    w = 600
    n = 20
    m = 20
    max_col_value = 255
    screen = display.set_mode((l, w))
    random_pixel = Surface((n, m))
    clock = time.Clock()
    f = font.Font("metlrebl.ttf", n)

    while True:
        for e in event.get():
            print("type: " + str(e.type))
            if e.type == QUIT:
                quit()
                sys.exit()

        for x in range_by_n(l, n):
            for y in range_by_n(w, m):

                r = random.randint(0, max_col_value)
                g = random.randint(0, max_col_value)
                b = random.randint(0, max_col_value)

                i = random.randint(33, 126)
                c = bytes([i])
                c = f.render(c, True, (r, g, b))

                screen.blit(c, (x, y))

        display.update()
        clock.tick(2)


def range_by_n(upper_limit, by_n=1):
    """Generate 0 to upper_limit, increasing by by_n at each step."""
    i = 0
    while True:
        yield i
        i += by_n
        if i > upper_limit:
            raise StopIteration


if __name__ == "__main__":
    main()
