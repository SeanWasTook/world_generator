from material import Material

""" Tile Class

 A tile represents a single square on the map
 The entirety of the map can be represented as a grid of tiles
 Created with one of the enums of Material
 Currently has limited functionality that will be expanded later
"""


class Tile:

    def __init__(self, material, decorations):
        self.material = material
        self.decorations = decorations

    def __str__(self):
        return self.material.txt

    def lower(self):
        if self.material == Material.DEEP_WATER:
            return
        elif self.material == Material.SHALLOW_WATER:
            self.material = Material.DEEP_WATER
        elif self.material == Material.SAND:
            self.material = Material.SHALLOW_WATER
            self.decorations = (None, None)
        elif self.material == Material.SHRUB:
            self.material = Material.SAND
        elif self.material == Material.GRASS:
            self.material = Material.SHRUB
            self.decorations = (None, None)
        elif self.material == Material.HILL:
            self.material = Material.GRASS
        elif self.material == Material.MOUNTAIN:
            self.material = Material.HILL
            self.decorations = (None, None)
        elif self.material == Material.SNOW:
            self.material = Material.MOUNTAIN
            self.decorations = (None, None)

    def increase(self):
        if self.material == Material.DEEP_WATER:
            self.material = Material.SHALLOW_WATER
        elif self.material == Material.SHALLOW_WATER:
            self.material = Material.SAND
        elif self.material == Material.SAND:
            self.material = Material.SHRUB
            self.decorations = (None, None)
        elif self.material == Material.SHRUB:
            self.material = Material.GRASS
        elif self.material == Material.GRASS:
            self.material = Material.HILL
        elif self.material == Material.HILL:
            self.material = Material.MOUNTAIN
            self.decorations = (None, None)
        elif self.material == Material.MOUNTAIN:
            self.material = Material.SNOW
            self.decorations = (None, None)
        elif self.material == Material.SNOW:
            return
