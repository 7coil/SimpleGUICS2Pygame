#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
simpleguics2pygame/canvas (January 29 29, 2020)

Class Canvas.

Piece of SimpleGUICS2Pygame.
https://bitbucket.org/OPiMedia/simpleguics2pygame

GPLv3 --- Copyright (C) 2015, 2016, 2020 Olivier Pirson
http://www.opimedia.be/
"""

from __future__ import division
from __future__ import print_function


__all__ = ['Canvas',
           'create_invisible_canvas']


try:
    import pygame

    _PYGAME_AVAILABLE = True
except ImportError:
    _PYGAME_AVAILABLE = False

from SimpleGUICS2Pygame.simpleguics2pygame._colors \
    import _SIMPLEGUICOLOR_TO_PYGAMECOLOR, \
    _simpleguicolor_to_pygamecolor


#
# Private global constants
##########################
from math import pi

_RADIAN_TO_DEGREE = 180.0/pi
"""
Multiplicative constant to convert radian to degree.
"""


from re import compile as re_compile

_RE_UNPRINTABLE_WHITESPACE_CHAR = re_compile('[\t\n\r\f\v]')
"""
Regular expression pattern to unprintable whitespace character.
"""


#
# "Private" function
####################
def _pos_round(position):
    """
    Returns the rounded `position`.

    **Don't require Pygame.**

    **(Not available in SimpleGUI of CodeSkulptor.)**

    :param position: (int or float, int or float)
                     or [int or float, int or float]

    :return: (int, int)
    """
    assert isinstance(position, tuple) or isinstance(position, list), \
        type(position)
    assert len(position) == 2, len(position)
    assert isinstance(position[0], int) or isinstance(position[0], float), \
        type(position[0])
    assert isinstance(position[1], int) or isinstance(position[1], float), \
        type(position[1])

    return (int(round(position[0])), int(round(position[1])))


#
# Class
#######
class Canvas:
    """
    Canvas similar to SimpleGUI `Canvas` of CodeSkulptor.
    """

    _background_pygame_color = (_SIMPLEGUICOLOR_TO_PYGAMECOLOR['black']
                                if _PYGAME_AVAILABLE
                                else None)
    """
    Default `pygame.Color` of the background of the canvas.
    """

    _background_pygame_surface_image = None
    """
    `pygame.Surface` default background image
    replaces `_background_pygame_color`.
    """

    def __init__(self,
                 frame,
                 canvas_width, canvas_height):
        """
        Set the canvas.

        **Don't use directly**, a canvas is created by `Frame()`
        and reachable by handler defined by `Frame.set_draw_handler()`.

        :param frame: Frame (or None)
        :param canvas_width: int >= 0
        :param canvas_height: int >= 0
        """
        assert _PYGAME_AVAILABLE, """Pygame not available!
See https://simpleguics2pygame.readthedocs.io/en/latest/#installation"""

        from SimpleGUICS2Pygame.simpleguics2pygame.frame import Frame

        assert (frame is None) or isinstance(frame, Frame), type(frame)

        assert isinstance(canvas_width, int), type(canvas_width)
        assert canvas_width >= 0, canvas_width

        assert isinstance(canvas_height, int), type(canvas_height)
        assert canvas_height >= 0, canvas_height

        self._frame_parent = frame

        self._width = canvas_width
        self._height = canvas_height

        self._background_pygame_color = Canvas._background_pygame_color

        self._draw_handler = None

        self._pygame_surface = pygame.Surface((canvas_width, canvas_height))

    def __repr__(self):
        """
        Return `'<Canvas object>'`.

        :return: str
        """
        return '<Canvas object>'

    def _draw(self):
        """
        If `self._draw_handler` != `None`
        then call it and update display of the canvas.

        **(Not available in SimpleGUI of CodeSkulptor.)**
        """
        if ((self._draw_handler is not None)
                and (self._frame_parent is not None)):
            if self._background_pygame_surface_image is None:
                if self._background_pygame_color.a == 255:
                    # Without alpha
                    self._pygame_surface.fill(self._background_pygame_color)
                elif self._background_pygame_color.a > 0:
                    # With alpha (not null)
                    s_alpha = pygame.Surface((self._width, self._height),
                                             pygame.SRCALPHA)
                    s_alpha.fill(self._background_pygame_color)
                    self._pygame_surface.blit(s_alpha, (0, 0))
            else:
                self._pygame_surface.blit(
                    self._background_pygame_surface_image, (0, 0))

            self._draw_handler(self)

            if self._frame_parent._display_fps_average:
                from SimpleGUICS2Pygame.simpleguics2pygame._fonts \
                    import _simpleguifontface_to_pygamefont

                self._pygame_surface.blit(
                    _simpleguifontface_to_pygamefont(None, 40)
                    .render(str(int(round(self._frame_parent._fps_average))),
                            True,
                            _SIMPLEGUICOLOR_TO_PYGAMECOLOR['red']),
                    (10, self._height - 40))

            self._frame_parent._pygame_surface.blit(
                self._pygame_surface,
                (self._frame_parent._canvas_x_offset,
                 self._frame_parent._canvas_y_offset))

            pygame.display.update((self._frame_parent._canvas_x_offset,
                                   self._frame_parent._canvas_y_offset,
                                   self._width,
                                   self._height))

    def _save(self, filename):
        """
        Save the canvas in `filename`.

        Supported formats are supported formats by Pygame to save:
        TGA, PNG, JPEG or BMP
        (see https://www.pygame.org/docs/ref/image.html#pygame.image.save ).

        If `filename` extension is not recognized
        then TGA format is used.

        **(Not available in SimpleGUI of CodeSkulptor.)**

        :param filename: str
        """
        assert isinstance(filename, str), type(filename)

        pygame.image.save(self._pygame_surface, filename)

    def draw_circle(self,
                    center_point, radius,
                    line_width, line_color,
                    fill_color=None):
        """
        Draw a circle.

        If `fill_color` != `None`
        then fill with this color.

        :param center_point: (int or float, int or float)
                             or [int or float, int or float]
        :param radius: (int or float) > 0
        :param line_width: (int or float) > 0
        :param line_color: str
        :param fill_color: None or str
        """
        assert (isinstance(center_point, tuple)
                or isinstance(center_point, list)), type(center_point)
        assert len(center_point) == 2, len(center_point)
        assert (isinstance(center_point[0], int)
                or isinstance(center_point[0], float)), type(center_point[0])
        assert (isinstance(center_point[1], int)
                or isinstance(center_point[1], float)), type(center_point[1])

        assert isinstance(radius, int) or isinstance(radius, float), \
            type(radius)
        assert radius > 0, radius

        assert isinstance(line_width, int) or isinstance(line_width, float), \
            type(line_width)
        assert line_width > 0, line_width

        assert isinstance(line_color, str), type(line_color)
        assert (fill_color is None) or isinstance(fill_color, str), \
            type(fill_color)

        line_width = (1 if line_width <= 1
                      else int(round(line_width)))

        radius = int(round(radius)) + int(round(line_width//2))

        if radius > 1:
            line_color = _simpleguicolor_to_pygamecolor(line_color)
            if fill_color is not None:
                fill_color = _simpleguicolor_to_pygamecolor(fill_color)

            if ((line_color.a == 255)
                    and ((fill_color is None) or (fill_color.a == 255))):
                # Without alpha
                if fill_color is not None:
                    pygame.draw.circle(self._pygame_surface, fill_color,
                                       _pos_round(center_point), radius, 0)
                if line_color != fill_color:
                    pygame.draw.circle(self._pygame_surface, line_color,
                                       _pos_round(center_point),
                                       radius, min(line_width, radius))
            elif ((line_color.a > 0)
                  or ((fill_color is not None) and (fill_color.a > 0))):
                # With one or two alpha (not null)
                s_alpha = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

                if (fill_color is not None) and (fill_color.a > 0):
                    pygame.draw.circle(s_alpha, fill_color,
                                       (radius, radius), radius, 0)
                if (line_color != fill_color) and (line_color.a > 0):
                    pygame.draw.circle(s_alpha, line_color,
                                       (radius, radius),
                                       radius, min(line_width, radius))

                self._pygame_surface.blit(
                    s_alpha,
                    (int(round(center_point[0])) - radius,
                     int(round(center_point[1])) - radius))
        elif radius > 0:  # == 1
            self.draw_point(center_point, line_color)

    def draw_image(self, image,
                   center_source, width_height_source,
                   center_dest, width_height_dest,
                   rotation=0):
        """
        Draw `image` on the canvas.

        Specify center position and size of the source (`image`)
        and center position and size of the destination (the canvas).

        Size of the source allow get a piece of `image`.
        If `width_height_source` is bigger than `image`
        then draw nothing.

        Size of the destination allow rescale the drawed image.

        `rotation` specify a clockwise rotation in radians.

        Each new Pygame surface used
        is added to `image._pygamesurfaces_cached`.
        See `Image._pygamesurfaces_cached_clear()`_ .

        .. _`Image._pygamesurfaces_cached_clear()`: image.html#SimpleGUICS2Pygame.simpleguics2pygame.image.Image._pygamesurfaces_cached_clear

        If number of surfaces in this caches
        is greater than `image._pygamesurfaces_cache_max_size`
        then remove the oldest surface.

        :param image: Image
        :param center_source: (int or float, int or float)
                              or [int or float, int or float]
        :param width_height_source: ((int or float) >= 0, (int or float) >= 0)
                                 or [(int or float) >= 0, (int or float) >= 0]
        :param center_dest: (int or float, int or float)
                            or [int or float, int or float]
        :param width_height_dest: ((int or float) >= 0, (int or float) >= 0)
                                  or [(int or float) >= 0, (int or float) >= 0]
        :param rotation: int or float
        """
        from SimpleGUICS2Pygame.simpleguics2pygame.image import Image

        assert isinstance(image, Image), type(image)

        assert (isinstance(center_source, tuple)
                or isinstance(center_source, list)), type(center_source)
        assert len(center_source) == 2, len(center_source)
        assert (isinstance(center_source[0], int)
                or isinstance(center_source[0], float)), type(center_source[0])
        assert (isinstance(center_source[1], int)
                or isinstance(center_source[1], float)), type(center_source[1])

        assert (isinstance(width_height_source, tuple)
                or isinstance(width_height_source, list)), \
            type(width_height_source)
        assert len(width_height_source) == 2, len(width_height_source)
        assert (isinstance(width_height_source[0], int)
                or isinstance(width_height_source[0], float)), \
            type(width_height_source[0])
        assert width_height_source[0] >= 0, width_height_source[0]
        assert (isinstance(width_height_source[1], int)
                or isinstance(width_height_source[1], float)), \
            type(width_height_source[1])
        assert width_height_source[1] >= 0, width_height_source[1]

        assert (isinstance(center_dest, tuple)
                or isinstance(center_dest, list)), type(center_dest)
        assert len(center_dest) == 2, len(center_dest)
        assert (isinstance(center_dest[0], int)
                or isinstance(center_dest[0], float)), type(center_dest[0])
        assert (isinstance(center_dest[1], int)
                or isinstance(center_dest[1], float)), type(center_dest[1])

        assert (isinstance(width_height_dest, tuple)
                or isinstance(width_height_dest, list)), \
            type(width_height_dest)
        assert len(width_height_dest) == 2, len(width_height_dest)
        assert (isinstance(width_height_dest[0], int)
                or isinstance(width_height_dest[0], float)), \
            type(width_height_dest[0])
        assert width_height_dest[0] >= 0, width_height_dest[0]
        assert (isinstance(width_height_dest[1], int)
                or isinstance(width_height_dest[1], float)), \
            type(width_height_dest[1])
        assert width_height_dest[1] >= 0, width_height_dest[1]

        assert isinstance(rotation, int) or isinstance(rotation, float), \
            type(rotation)

        if image._pygame_surface is None:
            return

        # Calculate parameters
        width_source, height_source = width_height_source

        x0_source = center_source[0] - width_source/2
        y0_source = center_source[1] - height_source/2

        if x0_source >= 0:
            x0_source = int(round(x0_source))
        elif -1 < x0_source:  # rounding error correcting
            width_source -= x0_source
            x0_source = 0
        else:                 # outside of source image
            return

        if y0_source >= 0:
            y0_source = int(round(y0_source))
        elif -1 < y0_source:  # rounding error correcting
            height_source -= y0_source
            y0_source = 0
        else:                 # outside of source image
            return

        width_source = int(round(width_source))
        height_source = int(round(height_source))

        if ((x0_source + width_source > image.get_width() + 1)
                or (y0_source + height_source > image.get_height() + 1)):
            # Bigger than source image
            return

        if x0_source + width_source > image.get_width():
            # Keep this image (seem too big, maybe rounding error)
            width_source -= 1

        if y0_source + height_source > image.get_height():
            # Keep this image (seem too big, maybe rounding error)
            height_source -= 1

        width_height_dest = _pos_round(width_height_dest)

        rotation = int(round(-rotation*_RADIAN_TO_DEGREE)) % 360

        # Get in cache or build Pygame surface
        from sys import version_info

        if version_info[:2] >= (3, 2):
            move_to_end = image._pygamesurfaces_cached.move_to_end
        else:
            def move_to_end(key):
                """
                Move the `key` item to the newest place of the surfaces cache.

                :param key: tuple of 7 (int >= 0)
                """
                del image._pygamesurfaces_cached[key]

                image._pygamesurfaces_cached[key] = pygame_surface_image

        key = (x0_source, y0_source, width_source, height_source,
               width_height_dest[0], width_height_dest[1],
               rotation)
        pygame_surface_image = image._pygamesurfaces_cached.get(key)

        if pygame_surface_image is not None:  # Result available
            move_to_end(key)
            if __debug__:
                image._pygamesurfaces_cached_counts[0] += 1
        else:                                 # Build result
            from SimpleGUICS2Pygame.simpleguics2pygame.frame import Frame

            key_0 = key[:-1] + (0, )
            if rotation != 0:  # Get not rotated surface in cache
                pygame_surface_image = image._pygamesurfaces_cached.get(key_0)

            if pygame_surface_image is not None:  # Not rotated available
                move_to_end(key_0)
                if __debug__:
                    image._pygamesurfaces_cached_counts[1] += 1
            else:                                 # Build piece and/or resize
                if ((x0_source == 0) and (y0_source == 0)
                        and (width_source == image.get_width())
                        and (height_source == image.get_height())):
                    pygame_surface_image = image._pygame_surface
                else:  # Get a piece in source
                    pygame_surface_image = image._pygame_surface.subsurface(
                        (x0_source, y0_source,
                         width_source, height_source))

                if ((width_height_dest[0] != width_source)
                        or (width_height_dest[1] != height_source)):
                    # Resize to destination dimensions
                    pygame_surface_image = pygame.transform.scale(
                        pygame_surface_image, width_height_dest)

                image._pygamesurfaces_cached[key_0] = pygame_surface_image

                if (Frame._print_stats_cache
                    and (len(image._pygamesurfaces_cached)
                         == image._pygamesurfaces_cache_max_size)):
                    image._print_stats_cache(
                        'Surfaces full cache              ')
                elif (len(image._pygamesurfaces_cached)
                      > image._pygamesurfaces_cache_max_size):
                    image._pygamesurfaces_cached.popitem(False)

            if rotation != 0:  # Rotate
                pygame_surface_image = pygame.transform.rotate(
                    pygame_surface_image, rotation)

                image._pygamesurfaces_cached[key] = pygame_surface_image

                if (Frame._print_stats_cache
                    and (len(image._pygamesurfaces_cached)
                         == image._pygamesurfaces_cache_max_size)):
                    image._print_stats_cache(
                        'Surfaces full cache with rotated ')
                elif (len(image._pygamesurfaces_cached)
                      > image._pygamesurfaces_cache_max_size):
                    image._pygamesurfaces_cached.popitem(False)

        # Draw the result
        self._pygame_surface.blit(
            pygame_surface_image,
            (int(round(center_dest[0] - pygame_surface_image.get_width()/2)),
             int(round(center_dest[1] - pygame_surface_image.get_height()/2))))
        if __debug__:
            image._draw_count += 1

    def draw_line(self,
                  point1, point2,
                  line_width, line_color):
        """
        Draw a line segment from point1 to point2.

        :param point1: (int or float, int or float)
                       or [int or float, int or float]
        :param point2: (int or float, int or float)
                       or [int or float, int or float]
        :param line_width: (int or float) > 0
        :param line_color: str
        """
        assert isinstance(point1, tuple) or isinstance(point1, list), \
            type(point1)
        assert len(point1) == 2, len(point1)
        assert isinstance(point1[0], int) or isinstance(point1[0], float), \
            type(point1[0])
        assert isinstance(point1[1], int) or isinstance(point1[1], float), \
            type(point1[1])

        assert isinstance(point2, tuple) or isinstance(point2, list), \
            type(point2)
        assert len(point2) == 2, len(point2)
        assert isinstance(point2[0], int) or isinstance(point2[0], float), \
            type(point2[0])
        assert isinstance(point2[1], int) or isinstance(point2[1], float), \
            type(point2[1])

        assert isinstance(line_width, int) or isinstance(line_width, float), \
            type(line_width)
        assert line_width > 0, line_width

        assert isinstance(line_color, str), type(line_color)

        line_color = _simpleguicolor_to_pygamecolor(line_color)

        if line_color.a == 255:  # without alpha
            pygame.draw.line(self._pygame_surface, line_color,
                             _pos_round(point1), _pos_round(point2),
                             int(round(line_width)))
        elif line_color.a > 0:   # with alpha (not null)
            x1, y1 = _pos_round(point1)
            x2, y2 = _pos_round(point2)

            width = abs(x2 - x1) + line_width*2
            height = abs(y2 - y1) + line_width*2

            x_min = min(x1, x2)
            y_min = min(y1, y2)

            s_alpha = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.line(s_alpha, line_color,
                             (x1 - x_min + line_width,
                              y1 - y_min + line_width),
                             (x2 - x_min + line_width,
                              y2 - y_min + line_width),
                             int(round(line_width)))
            self._pygame_surface.blit(s_alpha,
                                      (x_min - line_width, y_min - line_width))

    def draw_point(self, position, color):
        """
        Draw a point.

        :param position: (int or float, int or float)
                         or [int or float, int or float]
        :param color: str
        """
        assert isinstance(position, tuple) or isinstance(position, list), \
            type(position)
        assert len(position) == 2, len(position)
        assert isinstance(position[0], int) or isinstance(position[0], float),\
            type(position[0])
        assert isinstance(position[1], int) or isinstance(position[1], float),\
            type(position[1])

        assert isinstance(color, str), type(color)

        color = _simpleguicolor_to_pygamecolor(color)

        if color.a == 255:  # without alpha
            self._pygame_surface.set_at(_pos_round(position), color)
        elif color.a > 0:   # with alpha (not null)
            s_alpha = pygame.Surface((1, 1), pygame.SRCALPHA)
            s_alpha.set_at((0, 0), color)
            self._pygame_surface.blit(s_alpha, _pos_round(position))

    def draw_polygon(self,
                     point_list,
                     line_width, line_color,
                     fill_color=None):
        """
        Draw a polygon from a list of points.
        A segment is automatically drawed
        between the last point and the first point.

        If `fill color` is not None
        then fill with this color.

        If `line_width` > 1, ends are poorly made!

        :param point_list: not empty (tuple or list)
                           of ((int or float, int or float)
                           or [int or float, int or float])
        :param line_width: (int or float) > 0
        :param line_color: str
        :param fill_color: None or str
        """
        assert isinstance(point_list, tuple) or isinstance(point_list, list), \
            type(point_list)
        assert len(point_list) > 0, len(point_list)

        if __debug__:
            for point in point_list:
                assert isinstance(point, tuple) or isinstance(point, list), \
                    type(point)
                assert len(point) == 2, len(point)
                assert (isinstance(point[0], int)
                        or isinstance(point[0], float)), type(point[0])
                assert (isinstance(point[1], int)
                        or isinstance(point[1], float)), type(point[1])

        assert isinstance(line_width, int) or isinstance(line_width, float), \
            type(line_width)
        assert line_width >= 0, line_width

        assert isinstance(line_color, str), type(line_color)
        assert (fill_color is None) or isinstance(fill_color, str), \
            type(fill_color)

        if len(point_list) == 1:
            return

        line_color = _simpleguicolor_to_pygamecolor(line_color)
        if fill_color is not None:
            fill_color = _simpleguicolor_to_pygamecolor(fill_color)

        point_list = [_pos_round(point) for point in point_list]

        if ((line_color.a == 255)
                and ((fill_color is None) or (fill_color.a == 255))):
            # Without alpha
            if fill_color is not None:
                pygame.draw.polygon(self._pygame_surface, fill_color,
                                    point_list, 0)
            if line_color != fill_color:
                pygame.draw.lines(self._pygame_surface, line_color, True,
                                  point_list, line_width)
        elif ((line_color.a > 0)
              or ((fill_color is not None) and (fill_color.a > 0))):
            # With one or two alpha (not null)
            s_alpha = pygame.Surface((self._width, self._height),
                                     pygame.SRCALPHA)

            if (fill_color is not None) and (fill_color.a > 0):
                pygame.draw.polygon(s_alpha, fill_color,
                                    point_list, 0)
            if (line_color != fill_color) and (line_color.a > 0):
                pygame.draw.lines(s_alpha, line_color, True,
                                  point_list, line_width)

            self._pygame_surface.blit(s_alpha, (0, 0))

    def draw_polyline(self,
                      point_list,
                      line_width, line_color):
        """
        Draw line segments between a list of points.

        If `line_width` > 1, ends are poorly made!

        :param point_list: not empty (tuple or list)
                           of ((int or float, int or float)
                           or [int or float, int or float])
        :param line_width: (int or float) > 0
        :param line_color: str
        """
        assert isinstance(point_list, tuple) or isinstance(point_list, list), \
            type(point_list)
        assert len(point_list) > 0, len(point_list)

        if __debug__:
            for point in point_list:
                assert isinstance(point, tuple) or isinstance(point, list), \
                    type(point)
                assert len(point) == 2, len(point)
                assert (isinstance(point[0], int)
                        or isinstance(point[0], float)), type(point[0])
                assert (isinstance(point[1], int)
                        or isinstance(point[1], float)), type(point[1])

        assert isinstance(line_width, int) or isinstance(line_width, float), \
            type(line_width)
        assert line_width > 0, line_width

        assert isinstance(line_color, str), type(line_color)

        if len(point_list) == 1:
            return

        line_color = _simpleguicolor_to_pygamecolor(line_color)

        point_list = [_pos_round(point) for point in point_list]

        if line_color.a == 255:  # without alpha
            pygame.draw.lines(self._pygame_surface, line_color, False,
                              point_list, line_width)
        elif line_color.a > 0:   # with alpha (not null)
            s_alpha = pygame.Surface((self._width, self._height),
                                     pygame.SRCALPHA)

            pygame.draw.lines(s_alpha, line_color, False,
                              point_list, line_width)

            self._pygame_surface.blit(s_alpha, (0, 0))

    def draw_text(self,
                  text, point,
                  font_size, font_color,
                  font_face='serif',
                  _font_size_coef=3/4):
        """
        Draw the `text` string at the position `point`.

        (`point[0]` is the left of the text,
        `point[1]` is the bottom of the text.)

        If correponding font in Pygame is not founded,
        then use the default `pygame.font.Font`.

        `_font_size_coef` is used to adjust the vertical positioning.
        **(This paramater is not available in SimpleGUI of CodeSkulptor.)**

        :warning: This method can't draw multiline text.

        To draw multiline text, see `simplegui_lib_draw.draw_text_multi()`_ .

        .. _`simplegui_lib_draw.draw_text_multi()`: ../simplegui_lib_draw.html#SimpleGUICS2Pygame.simplegui_lib_draw.draw_text_multi

        :param text: str
        :param point: (int or float, int or float)
                      or [int or float, int or float]
        :param font_size: (int or float) >= 0
        :param font_color: str
        :param font_face: str == 'monospace', 'sans-serif', 'serif'
        :param _font_size_coef: int or float

        :raise: ValueError if text contains unprintable whitespace character

        **(Alpha color channel don't work!!!)**
        """
        assert isinstance(text, str), type(text)

        assert isinstance(point, tuple) or isinstance(point, list), type(point)
        assert len(point) == 2, len(point)
        assert isinstance(point[0], int) or isinstance(point[0], float), \
            type(point[0])
        assert isinstance(point[1], int) or isinstance(point[1], float), \
            type(point[1])

        assert isinstance(font_size, int) or isinstance(font_size, float), \
            type(font_size)
        assert font_size >= 0, font_size

        assert isinstance(font_color, str), type(font_color)

        from SimpleGUICS2Pygame.simpleguics2pygame._fonts \
            import _SIMPLEGUIFONTFACE_TO_PYGAMEFONTNAME, \
            _simpleguifontface_to_pygamefont

        assert isinstance(font_face, str), type(font_face)
        assert font_face in _SIMPLEGUIFONTFACE_TO_PYGAMEFONTNAME, font_face

        assert (isinstance(_font_size_coef, int)
                or isinstance(_font_size_coef, float)), type(_font_size_coef)

        if text == '':
            return

        if _RE_UNPRINTABLE_WHITESPACE_CHAR.search(text):
            raise ValueError('text may not contain non-printing characters')

        font_color = _simpleguicolor_to_pygamecolor(font_color)
        font_size = int(round(font_size))

        if (font_color.a > 0) and (font_size > 0):
            pygame_surface_text = _simpleguifontface_to_pygamefont(
                font_face, font_size).render(text, True, font_color)

            #if font_color.a == 255:  # without alpha
            self._pygame_surface.blit(
                pygame_surface_text,
                (point[0],
                 point[1] - pygame_surface_text.get_height()*_font_size_coef))
            #else:                    # with alpha (not null)
            #    # Don't work!!!
            #    s_alpha = pygame.Surface((pygame_surface_text.get_width(),
            #                              pygame_surface_text.get_height()),
            #                             pygame.SRCALPHA)
            #    s_alpha.blit(pygame_surface_text, (0, 0))
            #    self._pygame_surface.blit(
            #        s_alpha,
            #        (point[0],
            #         point[1]
            #         - pygame_surface_text.get_height()*_font_size_coef))


#
# SimpleGUI function
####################
def create_invisible_canvas(width, height):
    """
    NOT IMPLEMENTED!
    (Return a "weak" `Canvas`.)

    (Available in SimpleGUI of CodeSkulptor
    but *not in CodeSkulptor documentation*!)

    :param width: int >= 0
    :param height: int >= 0

    :return: Canvas
    """
    assert isinstance(width, int), type(width)
    assert width >= 0, width

    assert isinstance(height, int), type(height)
    assert height >= 0, height

    return Canvas(None, width, height)
