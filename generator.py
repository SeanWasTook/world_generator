import numpy as np
from noise import pnoise2
from material import Material
from decoration import DecorationType, Decoration
from tile import Tile


""" The world generator, that creates a grid of tiles using random noise

 The random noise is based on the perlin noise generator from the noise
 library, and allows for values that vary slowly as inputs change
"""


class Generator:
    """ Create a generator

     Size is the number of tiles on one side of the map (map will be a size x size square)
     Seed is an arbitrary number that randomizes how the map generates. Two
     different seeds will give two completely different maps, but the same
     seed will always give you the same map
    """
    def __init__(self, config_data, seed=0):
        self.x_height = config_data["world"]["width"]
        self.y_height = config_data["world"]["width"]
        self.scale = (1 + np.pi / 4) / config_data["world"]["continent-size"]
        if seed == 0:
            self.seed = np.random.rand()
        else:
            self.seed = (seed % 100000) / 100000

        #  Noise map is like a raw height map, random numbers with no meaning assigned to them
        self.noise_map = np.zeros((self.x_height, self.y_height))

        self.generate_noise_map()

        #  The tile map is what will actually be used, it represents the actual materials at each point
        self.tile_map = self.generate_tile_map()

    # Creates as 2D array of floats [0, 1) that represent the height at each point
    def generate_noise_map(self):

        for i in range(self.x_height):
            for j in range(self.y_height):
                x = self.scale * (i + 0.5) / 4.0
                y = self.scale * (j + 0.5) / 4.0
                x += self.seed*100000
                y += self.seed*100000
                self.noise_map[i][j] = pnoise2(x, y, octaves=3, persistence=0.3, lacunarity=3,) / 2.0 + .5  # Math normalizes the value to within [0, 1)

    # Uses the generator's noise map to create a 2D array of tiles
    def generate_tile_map(self):
        tile_map = np.empty(shape=(self.x_height, self.y_height), dtype=object)
        for i in range(self.x_height):
            for j in range(self.y_height):
                mat = Material.get_material_at_height(self.noise_map[i][j])
                dec1 = DecorationType.get_decoration_for_material(mat)
                if dec1 is not None:
                    dec1 = Decoration(dec1)
                dec2 = DecorationType.get_decoration_for_material(mat)
                if dec2 is not None:
                    dec2 = Decoration(dec2)
                decs = (dec1,
                        dec2)
                tile_map[i][j] = Tile(mat, decs)
        return tile_map
