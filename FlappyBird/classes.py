# -*- coding: utf-8 -*-
'''
    Classes
    =======

    Provides
      * Definitions for the Pipe, Bird and Base classes

    How to use
    ----------
    The heart of each of the games assests is defined here
    Specifics of the movementation and behaviour of each
    asset can be found in the docstring for each class.
'''

import pygame as pg
import os
import random
import numpy as np

from FlappyBird.brain import Brain

BIRD_IMGS = [
    pg.transform.scale2x(pg.image.load(os.path.join('assets', 'yellowbird.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('assets', 'bluebird.png'))),
    pg.transform.scale2x(pg.image.load(os.path.join('assets', 'redbird.png')))
]

BASE_IMG = pg.transform.scale2x(pg.image.load('assets/base.png'))
PIPE_IMG = pg.transform.scale2x(pg.image.load('assets/pipe-green.png'))

class Bird:
    ''' The Bird defines a FlappyBird's bird.

    Arguments
    ---------
    x - starting x position on the screen
    y - statting y position on the screen
    brain - a Brain instance, defined on
        the brain module
    '''

    IMGS = BIRD_IMGS
    BIRD_ID = 0

    def __init__(self, x, y, brain):
        self.x = x
        self.y = y
        self.vel = 0
        self.id = self.BIRD_ID
        self.step_count = 0
        self.img = random.choice(self.IMGS)
        self.distance_traveled_alive = 0
        self.dead = False
        self.brain = brain
        Bird.BIRD_ID += 1

    def __add__(self, other):
        ''' This add method defines the creation of a offspring
        of self and other. The offspring has a mixture of the
        weights of each instance of Bird, with a random variation

        Returns
        -------
        A Bird instance
        '''

        # Create a new weights matrix as mean of self and other
        new_weights1 = (self.brain.weights1 + other.brain.weights1)/2
        new_weights2 = (self.brain.weights2 + other.brain.weights2)/2

        # Create a noise matrix with size and shape as weights matrix
        noise_weights1 = np.random.normal(0,0.5,new_weights1.size).reshape(*new_weights1.shape)
        noise_weights2 = np.random.normal(0,0.5,new_weights2.size).reshape(*new_weights2.shape)

        new_weights1 = new_weights1 + noise_weights1
        new_weights2 = new_weights2 + noise_weights2

        return Bird(230,350, Brain(new_weights1, new_weights2))

    def jump(self):
        self.vel = -10.5
        self.step_count = 0

    def move(self):
        self.step_count += 1

        if not self.dead:
            self.distance_traveled_alive += 1

        move_distance = self.vel*self.step_count + 1.5*self.step_count**2

        if move_distance > 16: #terminal velocity
            move_distance = 16

        self.y += move_distance

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pg.mask.from_surface(self.img)

    def flap_or_not(self, distance_to_pipe, y):
        ''' Main process for deciding if the bird
        should flap its wings.

        Arguments
        ---------
        distance_to_pipe - bird to closest pipe ahead distance
        y - y distance from pipe gap

        '''
        brain_output = self.brain(np.array([distance_to_pipe,y]))
        if brain_output:
            self.jump()


class Pipe:
    ''' The Pipe defines a FlappyBird's obstacle.

    Arguments
    ---------
    x - starting x position on the screen
    '''
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        # TOP PIPE img needs to be flipped
        self.PIPE_TOP = pg.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()

        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

class Base:
    ''' The Base defines a FlappyBird's ground.

    Arguments
    ---------
    y - y position on the screen
    '''

    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
