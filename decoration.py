from enum import Enum
import pygame
import os
from material import Material
import numpy as np
import random

# A dictionary containing the config settings for decorations
config_dict = {'deep-water': {'None': 100}, 'shallow-water': {'None': 100},
               'sand': {'None': 100}, 'shrub': {'None': 100}, 'grass': {'None': 100},
               'hill': {'None': 100}, 'mountain': {'None': 100}, 'snow': {'None': 100}}

# A speed modifier that controls how fast plants grow. Higher numbers mean they grow faster
aging_speed = 1.0


# Called when config file is parsed to update generation settings
def update_decoration_config(new_dict):
    global config_dict
    config_dict = new_dict


""" An Enum representing the different decorations that can be found in the "world"

 Each decoration can be placed on tiles under specific circumstances
 This contains things such as trees and flowers
"""


class DecorationType(Enum):
    TREE = ("tree", [os.path.join("Images", "Tree01.png"),
                     os.path.join("Images", "Tree02.png"),
                     os.path.join("Images", "Tree03.png"),
                     os.path.join("Images", "Tree04.png")], 16, True)
    PALM = ("palm", [os.path.join("Images", "Palm01.png"),
                     os.path.join("Images", "Palm02.png"),
                     os.path.join("Images", "Palm03.png")], 16, True)
    PINE = ("pine", [os.path.join("Images", "Pine01.png"),
                     os.path.join("Images", "Pine02.png"),
                     os.path.join("Images", "Pine03.png"),
                     os.path.join("Images", "Pine04.png")], 16, True)
    RED_ROSE = ("red-rose", [os.path.join("Images", "RedRose.png")], 8, False)
    PINK_ROSE = ("pink-rose", [os.path.join("Images", "PinkRose.png")], 8, False)
    BLUE_ROSE = ("blue-rose", [os.path.join("Images", "BlueRose.png")], 8, False)
    EDELWEISS = ("edelweiss", [os.path.join("Images", "Edelweiss.png")], 8, False)

    def __init__(self, name, images, res, does_age):
        self.id_name = name
        self.images = [pygame.image.load(image) for image in images]
        self.res = res  # Resolution
        self.does_age = does_age

    @classmethod
    def convert_images(cls):
        for deco in DecorationType:
            deco.images = [image.convert_alpha() for image in deco.images]

    # Checks the config data for what decorations can be placed on the material
    # And chooses one using a weighted average
    @classmethod
    def get_decoration_for_material(cls, mat):
        decos = []
        weights = []
        decos_for_material = config_dict[mat.id_name]
        for deco in decos_for_material:
            decos.append(deco)
            weights.append(decos_for_material[deco])

        chosen = random.choices(decos, weights=weights, k=1)

        if chosen[0] == "None":
            return None
        else:
            return chosen[0]


""" A class that can be instantiated, representing a single ingame decoration

 For instance, it can hold data on the age and state of the decoration
"""


class Decoration:

    def __init__(self, decoration_type):
        self.decoration_type = decoration_type
        self.age = int(random.randint(0, 400)) // aging_speed
        self.img_index = 0
        self.res = 8

    def update(self):
        if self.decoration_type.does_age:
            self.age += 1
            if self.age == 520 // aging_speed:
                self.res = 16
                self.img_index = 1
            if self.age == 1000 // aging_speed:
                self.img_index = 2
            if self.age == (1700 // aging_speed) and len(self.decoration_type.images) > 3:
                self.img_index = 3

    def get_img(self):
        return self.decoration_type.images[self.img_index]

