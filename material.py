from enum import Enum
import pygame
import os

# The config settings for material choice
deep_shallow_water_border = 0.4
shallow_water_sand_border = 0.45
sand_shrub_border = 0.5
shrub_grass_border = 0.55
grass_hill_border = 0.6
hill_mountain_border = 0.65
mountain_snow_border = 0.7


# Called when the config file is parsed to set generation values
def set_values(material_heights):
    global deep_shallow_water_border, shallow_water_sand_border, sand_shrub_border, shrub_grass_border,\
        grass_hill_border, hill_mountain_border, mountain_snow_border
    deep_shallow_water_border = material_heights["deep-shallow-water-border"]
    shallow_water_sand_border = material_heights["shallow-water-sand-border"]
    sand_shrub_border = material_heights["sand-shrub-border"]
    shrub_grass_border = material_heights["shrub-grass-border"]
    grass_hill_border = material_heights["grass-hill-border"]
    hill_mountain_border = material_heights["hill-mountain-border"]
    mountain_snow_border = material_heights["mountain-snow-border"]


""" An Enum representing the different materials that can make up the "world"

 Each material represents what the world is made of at a certain height
 For instance, "Sea level" is at 0.3, below which is water
 Height ranges on [0, 1)
"""


class Material(Enum):
    DEEP_WATER = ("deep-water", 'W', os.path.join("Images", "DeepWater.png"))
    SHALLOW_WATER = ("shallow-water", 'w', os.path.join("Images", "ShallowWater.png"))
    SAND = ("sand", '_', os.path.join("Images", "Sand.png"))
    SHRUB = ("shrub", '/', os.path.join("Images", "Shrub.png"))
    GRASS = ("grass", '|', os.path.join("Images", "Grass.png"))
    HILL = ("hill", '^', os.path.join("Images", "Hill.png"))
    MOUNTAIN = ("mountain", 'M', os.path.join("Images", "Mountain.png"))
    SNOW = ("snow", '■', os.path.join("Images", "Snow.png"))

    def __init__(self, name, txt, img):
        self.id_name = name
        self.txt = txt  # A simple unicode representation, used for debugging
        self.img = pygame.image.load(img)

    @classmethod
    def convert_images(cls):
        for mat in Material:
            mat.img = mat.img.convert()

    @classmethod
    def get_material_at_height(cls, height):
        if height < deep_shallow_water_border:
            return Material.DEEP_WATER
        elif height < shallow_water_sand_border:
            return Material.SHALLOW_WATER
        elif height < sand_shrub_border:
            return Material.SAND
        elif height < shrub_grass_border:
            return Material.SHRUB
        elif height < grass_hill_border:
            return Material.GRASS
        elif height < hill_mountain_border:
            return Material.HILL
        elif height < mountain_snow_border:
            return Material.MOUNTAIN
        else:
            return Material.SNOW

