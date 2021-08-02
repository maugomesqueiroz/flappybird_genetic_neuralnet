# -*- coding: utf-8 -*-
'''
    Run
    ===

    Provides
      * Orchestrates the game execution and the evolution logic
'''

import numpy as np

from brain import Brain
from classes import Bird
from game import FlappyBirdGame

def create_birds(n=10):
    ''' Creates a list of n Birds with random weights

    Arguments
    ---------
    n - int, number of birds to create

    Returns
    -------
    Returns a list of Birds
    '''

    birds = []
    for count in range(n):
        birds.append(Bird(230,350, brain = Brain(np.random.rand(2,3), np.random.rand(3,1))))
    return birds

def evolve(birds, fitness):

    birds_and_fitness = list(zip(birds, fitness))
    #sort by fitness
    birds_and_fitness = sorted(birds_and_fitness, key=lambda x: x[1],reverse=True)
    sorted_birds = [bird for bird,_ in birds_and_fitness]

    new_birds = []

    #pass on the winners
    for bird in sorted_birds[:4]:
        bird_replica = Bird(230,350,Brain(bird.brain.weights1, bird.brain.weights2))
        new_birds.append(bird_replica)

    #Breed the winners
    new_birds.append(sorted_birds[0]+sorted_birds[1])
    new_birds.append(sorted_birds[0]+sorted_birds[2])
    new_birds.append(sorted_birds[1]+sorted_birds[2])

    #add mutate winners
    new_birds.append(sorted_birds[0]+sorted_birds[0])
    new_birds.append(sorted_birds[1]+sorted_birds[1])
    new_birds.append(sorted_birds[2]+sorted_birds[2])

    return new_birds

birds = create_birds()
fb = FlappyBirdGame(birds)

for generation in range(500):

    birds_fitness = fb.run()
    birds = evolve(birds, birds_fitness)
    fb.reset(birds,title=f'GEN {generation}')

fb.quit()
