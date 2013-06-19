#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
Mini-project #8 - RiceRocks (Asteroids) (June 19, 2013)

My solution (slightly retouched) of the mini-project #8 of the course
https://www.coursera.org/course/interactivepython (Coursera 2013).

Run on (maybe very slow on some browsers):
  - Chrome 27
  - Firefox 21
  - Safari 5.1.7 (without sounds)
  - Python 2 and 3 with SimpleGUICS2Pygame.

Piece of SimpleGUICS2Pygame.
https://bitbucket.org/OPiMedia/simpleguics2pygame

GPLv3 --- Copyright (C) 2013 Olivier Pirson
http://www.opimedia.be/
"""

import math
import random

try:
    from user16_Qpss15rD1ETZL7l import Loader

    import simplegui
except:
    from SimpleGUICS2Pygame.simplegui_lib import Loader

    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    simplegui.Frame._hide_status = True



#
# Global constants
###################
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



#
# Global variables
###################
frame = None

ricerock = None



#
# Helper functions
###################
def angle_to_vector(angle):
    """
    Return the vector corresponding to the angle expressed in radians.

    :param: int or float

    :return: (-1 <= float <= 1, -1 <= float <= 1)
    """
    #assert isinstance(angle, int) or isinstance(angle, float), type(angle)

    return (math.cos(angle), math.sin(angle))


def assert_position(position, non_negative = False, non_zero = False):
    """
    Assertions to check valid position: (int or float, int or float) or [int or float, int or float].

    If non_negative
    then each int or float must be >= 0.

    If non_zero
    then each int or float must be != 0.

    :param position: object
    :param non_negative: bool
    """
    assert isinstance(non_negative, bool), type(non_negative)
    assert isinstance(non_zero, bool), type(non_zero)

    assert isinstance(position, tuple) or isinstance(position, list), type(position)
    assert len(position) == 2, len(position)

    assert isinstance(position[0], int) or isinstance(position[0], float), type(position[0])
    assert isinstance(position[1], int) or isinstance(position[1], float), type(position[1])

    if non_negative:
        assert position[0] >= 0, position
        assert position[1] >= 0, position

    if non_zero:
        assert position[0] != 0, position
        assert position[1] != 0, position



#
# Classes
##########
class RiceRocks:
    """
    General class dealing the game.
    """
    def __init__(self):
        """
        Set elements of the game.
        """
        self.loaded = False

        self.keydown_left = False
        self.keydown_right = False
        self.lives = 3
        self.my_ship = None
        self.nb_bombs = None
        self.score = 0
        self.started = False
        self.time = 0.5

        self.explosions = []
        self.missiles = []
        self.rocks = []

        self.timer = simplegui.create_timer(1000, self.rock_spawner)


    def bomb_explode(self):
        """
        If it remains bomb
        then detonated a bomb that destroys all asteroids.
        """
        if self.nb_bombs:
            self.nb_bombs -= 1
            self.medias.get_sound('bomb_explode').rewind()
            self.medias.get_sound('bomb_explode').play()
            for rock in self.rocks:
                self.explosions.append(Sprite(rock.position, rock.velocity,
                                              0, rock.angle_velocity,
                                              'asteroid_explosion'))
            self.rocks = []


    def draw_and_update(self, canvas):
        """
        Draw and update all stuffs in each FPS cycle.

        :param canvas: simplegui.Canvas
        """
        self.time += 1

        # Draw static background
        canvas.draw_image(self.medias.get_image('nebula'),
                          self.img_infos['nebula'].get_center(), self.img_infos['nebula'].get_size(),
                          (SCREEN_WIDTH/2.0, SCREEN_HEIGHT/2.0), (SCREEN_WIDTH, SCREEN_HEIGHT))


        # Draw animated background
        center = self.img_infos['debris'].get_center()
        size = self.img_infos['debris'].get_size()

        y_offset = (self.time/8.0)%center[1]

        canvas.draw_image(self.medias.get_image('debris'),
                          (center[0], center[1] - y_offset), (size[0], size[1] - 2*y_offset),
                          (SCREEN_WIDTH/2.0, SCREEN_HEIGHT/2.0 + 1.25*y_offset), (SCREEN_WIDTH, SCREEN_HEIGHT - 2.5*y_offset))
        canvas.draw_image(self.medias.get_image('debris'),
                          (center[0], size[1] - y_offset), (size[0], 2*y_offset),
                          (SCREEN_WIDTH/2.0, 1.25*y_offset), (SCREEN_WIDTH, 2.5*y_offset))


        # Draw missiles, ship, asteroids and explosions
        for missile in self.missiles:
            missile.draw(canvas)

        if self.lives > 0:
            self.my_ship.draw(canvas)

        for rock in self.rocks:
            rock.draw(canvas)

        for i in range(len(self.explosions) - 1, -1, -1):
            explosion = self.explosions[i]

            explosion.draw(canvas)
            explosion.update()
            if explosion.lifespan <= 0:  # explosion finished
                del self.explosions[i]


        # Update ship
        self.my_ship.update()


        # Update missiles
        for i in range(len(self.missiles) - 1, -1, -1):
            missile = self.missiles[i]

            missile.update()
            if missile.lifespan <= 0:  # missile disappear
                del self.missiles[i]
            else:                      # active missile
                for j in range(len(self.rocks) - 1, -1, -1):  # check collide with asteroids
                    rock = self.rocks[j]

                    if missile.collide(rock):  # collide
                        del self.missiles[i]
                        del self.rocks[j]

                        self.score += 1
                        if self.score%10 == 0:
                            self.nb_bombs += 1
                            self.medias.get_sound('bomb_extra').rewind()
                            self.medias.get_sound('bomb_extra').play()

                        self.explosions.append(Sprite(rock.position, rock.velocity,
                                                      0, rock.angle_velocity,
                                                      'asteroid_explosion'))

                        break


        # Update asteroids
        for i in range(len(self.rocks) - 1, -1, -1):
            rock = self.rocks[i]

            rock.update()
            if self.my_ship.collide(rock):  # collide with ship
                del self.rocks[i]

                self.explosions.append(Sprite(rock.position, rock.velocity,
                                              0, rock.angle_velocity,
                                              'asteroid_collide_explosion'))

                self.lives = max(0, self.lives - 1)
                if self.lives <= 0:  # game over
                    self.stop()

                    self.explosions.append(Sprite(self.my_ship.position, self.my_ship.velocity,
                                                  0, self.my_ship.angle_velocity,
                                                  'ship_explosion'))

                    self.medias.get_sound('death').rewind()
                    self.medias.get_sound('death').play()

                    break


        # Display number of lives
        if self.started:
            info = self.img_infos['ship']
            for i in range(self.lives):
                canvas.draw_image(self.medias.get_image('ship'),
                                  info.get_center(), info.get_size(),
                                  (40 + i*40, 40), (40, 40),
                                  -math.pi/2)


        # Display number of bombs
        if self.started and self.nb_bombs:
            info = self.img_infos['bomb']
            for i in range(self.nb_bombs):
                canvas.draw_image(self.medias.get_image('bomb'),
                                  info.get_center(), info.get_size(),
                                  (40 + i*40, 80), (20, 40),
                                  -math.pi/2)


        # Display score
        size = 36
        font = 'sans-serif'

        s1 = 'Score'
        width1 = frame.get_canvas_textwidth(s1, size, font)
        s2 = str(self.score)
        width2 = frame.get_canvas_textwidth(s2, size, font)

        canvas.draw_text(s1, (SCREEN_WIDTH - 22 - width1, 22 + size*3.0/4), size, 'Gray', font)
        canvas.draw_text(s2, (SCREEN_WIDTH - 22 - width2, 22 + size*7.0/4), size, 'Gray', font)

        canvas.draw_text(s1, (SCREEN_WIDTH - 20 - width1, 20 + size*3.0/4), size, 'White', font)
        canvas.draw_text(s2, (SCREEN_WIDTH - 20 - width2, 20 + size*7.0/4), size, 'White', font)


        # Draw splash screen if game not started
        if not self.started:
            size = self.img_infos['splash'].get_size()
            canvas.draw_image(self.medias.get_image('splash'),
                              self.img_infos['splash'].get_center(), size,
                              (SCREEN_WIDTH/2.0, SCREEN_HEIGHT/2.0), size)



    def load_medias(self):
        """
        Load images and sounds and waiting all is loaded,
        the set the general draw handler.
        """
        self.img_infos = {'asteroid-1': ImageInfo((45, 45), (90, 90), 40),
                          'asteroid-2': ImageInfo((45, 45), (90, 90), 40),
                          'asteroid-3': ImageInfo((45, 45), (90, 90), 38),
                          'asteroid_explosion': ImageInfo((64, 64), (128, 128), 17, 24, True),
                          'asteroid_collide_explosion': ImageInfo((64, 64), (128, 128), 17, 24, True),
                          'bomb': ImageInfo((10, 10), (20, 20)),
                          'debris': ImageInfo((320, 240), (640, 480)),
                          'missile': ImageInfo((5, 5), (10, 10), 3, 50),
                          'nebula': ImageInfo((400, 300), (800, 600)),
                          'ship': ImageInfo((45, 45), (90, 90), 35),
                          'ship_explosion': ImageInfo((64, 64), (128, 128), 17, 24, True),
                          'splash': ImageInfo((200, 150), (400, 300))}


        self.medias = Loader()

        # Images by Kim Lathrop
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png',
                              'asteroid-1')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png',
                              'asteroid-2')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png',
                              'asteroid-3')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png',
                              'asteroid_explosion')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha2.png',
                              'asteroid_collide_explosion')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png',
                              'bomb')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png',
                              'debris')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png',
                              'missile')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png',
                              'nebula')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png',
                              'ship')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png',
                              'ship_explosion')
        self.medias.add_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png',
                              'splash')


        # Sounds from http://www.sounddogs.com/ (not free)
        self.medias.add_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg',
                              'asteroid_explosion')
        self.medias.add_sound('http://rpg.hamsterrepublic.com/wiki-images/f/f4/StormMagic.ogg',
                              'bomb_explode')
        self.medias.add_sound('http://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/extralife.ogg',
                              'bomb_extra')
        self.medias.add_sound('http://rpg.hamsterrepublic.com/wiki-images/5/58/Death.ogg',
                              'death')
        self.medias.add_sound('http://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/intromusic.ogg',
                              'intro')
        self.medias.add_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg',
                              'soundtrack')
        self.medias.add_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg',
                              'missile')
        self.medias.add_sound('http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg',
                              'ship_thrust')


        self.medias.load()


        def init():
            """
            Init the game after medias loaded.
            """
            self.medias.get_sound('missile').set_volume(.5)

            self.my_ship = Ship((SCREEN_WIDTH/2.0, SCREEN_HEIGHT/2.0), (0, 0), -math.pi/2, 'ship')

            frame.set_draw_handler(self.draw_and_update)

            frame.set_keydown_handler(keydown)
            frame.set_keyup_handler(keyup)

            frame.set_mouseclick_handler(click)

            self.medias.get_sound('intro').play()

            self.medias._sounds['asteroid_collide_explosion'] = self.medias._sounds['asteroid_explosion']

            self.loaded = True


        self.medias.wait_loaded(frame, SCREEN_WIDTH, init)


    def rock_spawner(self):
        """
        If the maximum is not reached
        then spawns a rock (not too close to the ship).
        """
        if len(self.rocks) < 12:
            too_close = True

            def random_vel():
                """
                :return: int or float
                """
                return min(10, (random.random()*0.3*(self.score/2 + 1)))*random.choice((-1, 1))

            while too_close:
                rock_pos = (random.randrange(0, SCREEN_WIDTH),
                            random.randrange(0, SCREEN_HEIGHT))
                rock_vel = (random_vel(),
                            random_vel())
                rock_ang_vel = random.random()*0.2 - 0.1

                rock = Sprite(rock_pos, rock_vel,
                              0, rock_ang_vel,
                              'asteroid-' + str(random.randint(1, 3)))
                too_close = self.my_ship.distance(rock) < (self.my_ship.radius + rock.radius)*1.5

            self.rocks.append(rock)


    def start(self):
        """
        Start the game.
        """
        self.medias.get_sound('intro').rewind()
        self.medias.get_sound('soundtrack').play()

        self.keydown_left = False
        self.keydown_right = False
        self.lives = 3
        self.nb_bombs = 0
        self.score = 0

        self.my_ship = Ship((SCREEN_WIDTH/2.0, SCREEN_HEIGHT/2.0), (0, 0), -math.pi/2, 'ship')

        self.explosions = []
        self.missiles = []
        self.rocks = []

        self.timer.start()
        self.rock_spawner()

        self.started = True


    def stop(self):
        """
        Stop the game.
        """
        self.timer.stop()

        self.nb_bombs = None

        self.missiles = []
        self.rocks = []

        self.started = False

        self.medias.get_sound('soundtrack').rewind()
        self.my_ship.stop()

        self.medias.get_sound('intro').play()



class ImageInfo:
    """
    Informations to use with Sprite.
    """
    def __init__(self, center, size, radius = None, lifespan = None, animated = False):
        """
        Set informations.

        If radius == None
        then use maximum of size components.

        :param center: (int or float, int or float) or [int or float, int or float]
        :param size: ((int or float) > 0, (int or float) > 0) or [(int or float) > 0, (int or float) > 0]
        :param radius: None or ((int or float) > 0)
        :param lifespan: None or ((int or float) > 0)
        :param animated: bool
        """
        #assert_position(center)
        #assert_position(size, True, True)
        #assert (radius == None) or ((isinstance(radius, int) or isinstance(radius, float)) and (radius > 0)), radius
        #assert (lifespan == None) or ((isinstance(lifespan, int) or isinstance(lifespan, float)) and (lifespan > 0)), lifespan
        #assert isinstance(animated, bool), type(animated)

        self._center = list(center)
        self._size = list(size)
        self._radius = (max(size) if radius == None
                        else radius)
        self._lifespan = (lifespan if lifespan
                          else float('inf'))
        self._animated = animated


    def get_animated(self):
        """
        If is a animated image
        then return True,
        else return False.

        :return: bool
        """
        return self._animated


    def get_center(self):
        """
        Return position of the center of image.

        :return: [int or float, int or float]
        """
        return list(self._center)


    def get_lifespan(self):
        """
        Return lifespan of image.

        :return: None or ((int or float) > 0)
        """
        return self._lifespan


    def get_radius(self):
        """
        Return radius of image.

        :return: (int or float) > 0
        """
        return self._radius


    def get_size(self):
        """
        Return size of image.

        :return: [(int or float) > 0, (int or float) > 0]
        """
        return list(self._size)



class Sprite:
    """
    Sprite class
    """
    def __init__(self, position, velocity, angle,
                 angle_velocity,
                 media_name):
        """
        Set sprite.

        :param position: (int or float, int or float) or [int or float, int or float]
        :param velocity: (int or float, int or float) or [int or float, int or float]
        :param angle: int or float
        :param media_name: str
        """
        #assert_position(position)
        #assert_position(velocity)
        #assert isinstance(angle, int) or isinstance(angle, float), type(angle)
        #assert isinstance(angle_velocity, int) or isinstance(angle_velocity, float), type(angle_velocity)
        #assert isinstance(media_name, str), type(media_name)

        if media_name in ricerocks.medias._sounds:
            sound = ricerocks.medias.get_sound(media_name)
            sound.rewind()
            sound.play()

        self.position = list(position)
        self.velocity = list(velocity)
        self.angle = angle
        self.angle_velocity = angle_velocity
        self.image = ricerocks.medias.get_image(media_name)

        img_info = ricerocks.img_infos[media_name]
        self.animated = img_info.get_animated()
        self.image_center = img_info.get_center()
        self.image_size = img_info.get_size()
        self.lifespan = img_info.get_lifespan()
        self.radius = img_info.get_radius()


    def collide(self, other_sprite):
        """
        If this sprite collide with other_sprite
        then return True,
        else return False

        :param other_sprite: Sprite

        :return: bool
        """
        #assert isinstance(other_sprite, Sprite), type(other_sprite)

        return ((self.position[0] - other_sprite.position[0])**2 + (self.position[1] - other_sprite.position[1])**2
                <= (self.radius + other_sprite.radius)**2)


    def distance(self, other_sprite):
        """
        Return the distance between this sprite and other_sprite.

        :param other_sprite: Sprite

        :return: float
        """
        #assert isinstance(other_sprite, Sprite), type(other_sprite)

        return math.sqrt((self.position[0] - other_sprite.position[0])**2 + (self.position[1] - other_sprite.position[1])**2)


    def draw(self, canvas):
        """
        Draw the sprite
        (if the associated image are not loaded, draw a red disc).

        :param canvas: simplegui.Canvas
        """
        if self.image.get_width() > 0:
            canvas.draw_image(self.image,
                              self.image_center, self.image_size,
                              self.position, self.image_size,
                              self.angle)
        else:
            # Useful to debug
            canvas.draw_circle(self.position, self.radius, 1, 'Red', 'Red')


    def update(self):
        """
        Update position adding velocity,
        angle adding angle_velocity,
        lifespan and current image if animated.
        """
        self.angle += self.angle_velocity

        self.position[0] = (self.position[0] + self.velocity[0])%SCREEN_WIDTH
        self.position[1] = (self.position[1] + self.velocity[1])%SCREEN_HEIGHT

        if self.lifespan != None:
            self.lifespan -= 1
            if self.animated:  # change the current image
                #assert self.image_center[0] < self.image.get_width()

                self.image_center[0] += self.image_size[0]



class Ship(Sprite):
    """
    Ship class
    """
    def __init__(self, position, velocity, angle,
                 media_name):
        """
        Set ship sprite.

        :param position: (int or float, int or float) or [int or float, int or float]
        :param velocity: (int or float, int or float) or [int or float, int or float]
        :param angle: int or float
        :param media_name: str
        """
        #assert_position(position)
        #assert_position(velocity)
        #assert isinstance(angle, int) or isinstance(angle, float), type(angle)
        #assert isinstance(media_name, str), type(media_name)

        Sprite.__init__(self, position, velocity, angle,
                        0,
                        media_name)

        self.thrust = False


    def flip(self):
        """
        Flip the ship.
        """
        self.angle += math.pi


    def shoot(self):
        """
        Launch a missile.
        """
        v = angle_to_vector(ricerocks.my_ship.angle)

        ricerocks.missiles.append(Sprite((ricerocks.my_ship.position[0] + ricerocks.my_ship.radius*v[0], ricerocks.my_ship.position[1] + ricerocks.my_ship.radius*v[1]),
                                         (ricerocks.my_ship.velocity[0] + v[0]*6, ricerocks.my_ship.velocity[1] + v[1]*6),
                                         self.angle, 0,
                                         'missile'))


    def stop(self):
        """
        Stop the ship.
        """
        self.turn(None)
        if self.thrust:
            self.thrust_on_off()


    def thrust_on_off(self):
        """
        Switch activation of thrust.
        """
        self.thrust = not self.thrust

        if self.thrust:
            ricerocks.medias.get_sound('ship_thrust').play()
            self.image_center[0] += self.image_size[0]  # sprite image with actif thrust
        else:
            ricerocks.medias.get_sound('ship_thrust').rewind()
            self.image_center[0] -= self.image_size[0]  # sprite image with inactif thrust


    def turn(self, right):
        """
        Turn the ship
        (in fact change angle_velocity).

        :param right: None or Bool
        """
        #assert (right == None) or isinstance(right, bool), type(right)

        ricerocks.my_ship.angle_velocity = {False: -0.075,
                                  None: 0,
                                  True: 0.075}[right]


    def update(self):
        """
        Update position adding velocity (and deal exit out of the canvas),
        decrease slightly velocity,
        and angle adding angle_velocity.

        Moreover if thrust is active then increase velocity.
        """
        # Update angle
        self.angle += self.angle_velocity

        # Update position
        self.position[0] = (self.position[0] + self.velocity[0])%SCREEN_WIDTH
        self.position[1] = (self.position[1] + self.velocity[1])%SCREEN_HEIGHT

        # Update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.velocity[0] += acc[0]*.1
            self.velocity[1] += acc[1]*.1

        self.velocity[0] *= .99
        self.velocity[1] *= .99



#
# Event handlers
#################
def click(pos):
    """
    If click on splash screen
    then start the game.
    """
    center = (SCREEN_WIDTH/2.0, SCREEN_HEIGHT/2.0)
    size = ricerocks.img_infos['splash'].get_size()

    if ((not ricerocks.started)
        and (center[0] - size[0]/2.0) < pos[0] < (center[0] + size[0]/2.0)
        and (center[1] - size[1]/2.0) < pos[1] < (center[1] + size[1]/2.0)):
        ricerocks.start()


def keydown(key):
    """
    Event handler to deal key down.
    """
    if ricerocks.started:
        if key == simplegui.KEY_MAP['left']:
            ricerocks.keydown_left = True
            ricerocks.my_ship.turn(False)
        elif key == simplegui.KEY_MAP['right']:
            ricerocks.keydown_right = True
            ricerocks.my_ship.turn(True)
        elif key == simplegui.KEY_MAP['up']:
            ricerocks.my_ship.thrust_on_off()
        elif key == simplegui.KEY_MAP['down']:
            ricerocks.my_ship.flip()
        elif key == simplegui.KEY_MAP['space']:
            ricerocks.my_ship.shoot()
        elif key == simplegui.KEY_MAP['Z']:
            ricerocks.bomb_explode()


def keyup(key):
    """
    Event handler to deal key up.
    """
    if ricerocks.started:
        if key == simplegui.KEY_MAP['left']:
            ricerocks.keydown_left = False
            ricerocks.my_ship.turn(True if ricerocks.keydown_right
                                   else None)
        elif key == simplegui.KEY_MAP['right']:
            ricerocks.keydown_right = False
            ricerocks.my_ship.turn(False if ricerocks.keydown_left
                                   else None)
        elif key == simplegui.KEY_MAP['up']:
            ricerocks.my_ship.thrust_on_off()


def quit():
    """
    Stop timer and quit.
    """
    if ricerocks.loaded:
        ricerocks.stop()
        frame.stop()


def stop():
    """
    Stop the game.
    """
    if ricerocks.loaded:
        ricerocks.stop()



#
# Main
#######
if __name__ == '__main__':
    frame = simplegui.create_frame('RiceRocks (Asteroids)', SCREEN_WIDTH, SCREEN_HEIGHT)


    ricerocks = RiceRocks()
    ricerocks.load_medias()


    frame.add_button('Stop this game', stop)
    frame.add_label('')
    frame.add_button('Quit', quit)
    frame.add_label('')
    frame.add_label('Turn: Left and Right')
    frame.add_label('Accelerate: Up')
    frame.add_label('Flip: Down')
    frame.add_label('Fire: Space')
    frame.add_label('Bomb: Z (or W)')


    frame.start()