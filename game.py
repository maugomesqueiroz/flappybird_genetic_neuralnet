# -*- coding: utf-8 -*-
'''
    Game
    ====

    Provides
      * Definition of FlappyBirdGame class, which contains
        the main logic for the game.

    How to use
    ----------
    You can instanciate FlappyBirdGame, passing a list
    of Birds. It will run automatically.
'''


import os
import random
import time
import numpy as np
import pygame as pg

from classes import (Base, Bird, Pipe)

WIN_WIDTH = 500
WIN_HEIGHT = 800

BG_IMG = pg.transform.scale2x(pg.image.load('assets/background-day.png'))

pg.font.init()
STAT_FONT = pg.font.SysFont('comicsans', 40)

class FlappyBirdGame():
    ''' The core of the FlappyBird's game.

    Arguments
    ---------
    birds - a list of Bird
    '''

    def __init__(self, birds):

        self.title = 'Flappy Bird'
        self.base = Base(y=730)
        self.birds = birds
        self.pipes = [Pipe(x=550)]
        self.score = 0

        self.win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pg.time.Clock()

    def reset(self, birds, title='Flappy Bird'):
        ''' Resets the game with a new title and
        a new list of birds
        '''

        self.title = title
        self.birds = birds
        self.pipes = [Pipe(x=550)]
        self.score = 0

    def run(self, title='Flappy Bird'):
        ''' Given a list of Birds that were
        loaded into FlappyBirdGame during instantiation
        run the game until all of the birds die.

        Arguments
        ---------
        title - str, title of this run

        Returns
        -------
        Returns a list of each birds fitness.
        '''
        quit = False
        while True:
            self.clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit = True
            if quit:
                break

            add_pipe = False
            pipes_to_remove = []
            for pipe in self.pipes:
                is_pipe_outside_screen = pipe.x + pipe.PIPE_TOP.get_width() < 0
                is_pipe_behind_birds = not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < self.birds[0].x

                for bird in self.birds:
                    # Death by collision with pipe
                    if pipe.collide(bird) and not bird.dead:
                        bird.dead = True

                if is_pipe_outside_screen:
                    pipes_to_remove.append(pipe)

                if is_pipe_behind_birds:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()

            if add_pipe:
                self.score += 1
                self.pipes.append(Pipe(550))

            for pipe in pipes_to_remove:
                self.pipes.remove(pipe)

            pipes_ahead = [pipe for pipe in self.pipes
                            if pipe.passed == False]

            closest_pipe_idx = np.argmin([pipe.x for pipe in pipes_ahead])
            closest_pipe = pipes_ahead[closest_pipe_idx]

            for bird in self.birds:
                # Death by collision with ground
                bird_touched_ground = bird.y + bird.img.get_height() >= 730
                if bird_touched_ground and not bird.dead:
                    bird.dead = True

                if not bird.dead:
                    x_distance_to_closest_pipe = closest_pipe.x+ closest_pipe.PIPE_TOP.get_width() - bird.x
                    y_distance_to_pipe_gap = closest_pipe.height - bird.y
                    bird.flap_or_not(x_distance_to_closest_pipe/1000,y_distance_to_pipe_gap/1000)
                    bird.move()

            self.base.move()
            self.draw_window()

            exists_a_bird_alive = False in [bird.dead for bird in self.birds]
            if not exists_a_bird_alive:
                break

        birds_fitness = [bird.distance_traveled_alive-closest_pipe.x for bird in self.birds]
        return birds_fitness

    def draw_window(self):

        self.win.blit(BG_IMG, (0,0))

        self.base.draw(self.win)

        for pipe in self.pipes:
            pipe.draw(self.win)


        y_displacement = 1
        for bird in self.birds:
            if not bird.dead:
                bird.draw(self.win)

            bird_str = f'{bird.id}: {bird.distance_traveled_alive}'
            text = STAT_FONT.render(bird_str, 1, [255]*3)
            self.win.blit(text, (0,30*y_displacement))
            y_displacement += 1

        score_str = f'Score: {str(self.score)}'
        score_text = STAT_FONT.render(score_str, 1, [255]*3)
        title_text = STAT_FONT.render(str(self.title), 1, [255]*3)
        self.win.blit(title_text, (0,5))
        self.win.blit(score_text, (WIN_WIDTH/2,30))

        pg.display.update()

    @staticmethod
    def quit():
        pg.quit()
        quit()
