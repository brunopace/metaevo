#!/usr/bin/python

import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random as rndm
import numpy
import time
from Constants import Constants
from copy import deepcopy

class Environment():
    def __init__(self, descriptivestring):
        self.actual = Constants.env_dict[descriptivestring][0]

    def change_environment(index):
        self.actual = Constants.env_dict[descriptivestring][index]

