#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
Test colors HTML. (October 4, 2013)

Piece of SimpleGUICS2Pygame.
https://bitbucket.org/OPiMedia/simpleguics2pygame

GPLv3 --- Copyright (C) 2013, 2014 Olivier Pirson
http://www.opimedia.be/
"""

try:
    from user38_ZmhOVHGm2lhVRhk import hex2, hex_fig

    import simplegui

    SIMPLEGUICS2PYGAME = False
except ImportError:
    from SimpleGUICS2Pygame.codeskulptor_lib import hex2, hex_fig

    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    SIMPLEGUICS2PYGAME = True

    simplegui.Frame._hide_status = True


if SIMPLEGUICS2PYGAME:
    from sys import version as python_version
    from pygame.version import ver as pygame_version
    from SimpleGUICS2Pygame import _VERSION as GUI_VERSION

    PYTHON_VERSION = 'Python ' + python_version.split()[0]
    PYGAME_VERSION = 'Pygame ' + pygame_version
    GUI_VERSION = 'SimpleGUICS2Pygame ' + GUI_VERSION
else:
    PYTHON_VERSION = 'CodeSkulptor'  # http://www.codeskulptor.org/
    PYGAME_VERSION = ''
    GUI_VERSION = 'simplegui'


TEST = 'test colors HTML'

WIDTH = 512
HEIGHT = 180


def draw(canvas):
    """
    Draw (with draw_line()) range of colors in #rgb and #rrggbb formats.

    :param canvas: simpleguics2pygame.Canvas or simplegui.Canvas
    """
    for i in range(16):  # Format #rgb
        canvas.draw_line((i*32, 10), ((i + 1)*32, 10), 10,
                         '#' + hex_fig(i)*3)
        canvas.draw_line((i*32, 30), ((i + 1)*32, 30), 10,
                         '#' + hex_fig(i) + '00')
        canvas.draw_line((i*32, 50), ((i + 1)*32, 50), 10,
                         '#0' + hex_fig(i) + '0')
        canvas.draw_line((i*32, 70), ((i + 1)*32, 70), 10,
                         '#00' + hex_fig(i))

    for i in range(256):  # Format #rrggbb
        canvas.draw_line((i*2, 110), ((i + 1)*2, 110), 10,
                         '#' + hex2(i)*3)
        canvas.draw_line((i*2, 130), ((i + 1)*2, 130), 10,
                         '#' + hex2(i) + '0000')
        canvas.draw_line((i*2, 150), ((i + 1)*2, 150), 10,
                         '#00' + hex2(i) + '00')
        canvas.draw_line((i*2, 170), ((i + 1)*2, 170), 10,
                         '#0000' + hex2(i))


# Main
frame = simplegui.create_frame(TEST, WIDTH, HEIGHT)

frame.add_label(TEST)
frame.add_label('')
frame.add_label(PYTHON_VERSION)
frame.add_label(GUI_VERSION)
frame.add_label(PYGAME_VERSION)
frame.add_label('')
frame.add_button('Quit', frame.stop)

frame.set_draw_handler(draw)

if SIMPLEGUICS2PYGAME:
    from sys import argv

    if len(argv) == 2:
        frame._save_canvas_and_stop(argv[1])


frame.start()
