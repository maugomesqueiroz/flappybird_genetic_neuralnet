# -*- coding: utf-8 -*-
'''
    Brain
    =====

    Provides a Brain class, that simulates a bird's brain.
    This class should be callable, returning True or False
    depending on whether or not the bird should flap its wings.

    How to use
    ----------
    Brain is passed as an argument to Bird, which is defined in
    the classes module.

'''

import numpy as np

class Brain:
    ''' An abstraction of a flappy bird's brain.

    The brain is a Neural Network with two input nodes, one
    hidden layer with 6 nodes and one output node.

    Arguments
    ---------
    weights1 - weights mapping input to first hidden layer,
        has shape (6,2)
    weights2 - weights mapping first hidden layer to output,
        has shape (1,6)
    '''

    def __init__(self, weights1: np.array, weights2: np.array):
        self.weights1 = weights1
        self.weights2 = weights2
        self.activation = lambda x: 1 if x > 0.5 else 0

    def __call__(self, information: np.array):
        ''' Here should be defined the main logic for flapping.
        Arguments
        ---------
        information - Information is a np.array containing the inputs
            the bird will use to make an informed decision.

        Returns
        -------
        Returns a boolean corresponding to the decision of
        wing flapping.
        '''
        layer1_output = np.matmul(self.weights1, information)
        layer1_output = np.array([self.activation(value) for value in layer1_output])
        
        layer2_output = np.matmul(self.weights2, layer1_output)
        layer2_output = np.array([self.activation(value) for value in layer2_output])

        if layer2_output[0] == 1:
            return True
        return False


