import unittest
import material
from material import Material
import decoration
from decoration import DecorationType
from tile import Tile
from generator import Generator
from config_parser import parse_config


class TestMaterials(unittest.TestCase):

    def test_deep_water(self):
        self.assertEqual(Material.get_material_at_height(0.1), Material.DEEP_WATER)

    def test_shallow_water(self):
        self.assertEqual(Material.get_material_at_height(0.44), Material.SHALLOW_WATER)

    def test_sand(self):
        self.assertEqual(Material.get_material_at_height(0.46), Material.SAND)

    def test_shrub(self):
        self.assertEqual(Material.get_material_at_height(0.51), Material.SHRUB)

    def test_grass(self):
        self.assertEqual(Material.get_material_at_height(0.56), Material.GRASS)

    def test_hill(self):
        self.assertEqual(Material.get_material_at_height(0.63), Material.HILL)

    def test_mountain(self):
        self.assertEqual(Material.get_material_at_height(0.67), Material.MOUNTAIN)

    def test_snow(self):
        self.assertEqual(Material.get_material_at_height(0.9), Material.SNOW)


class TestDecoration(unittest.TestCase):

    def setUp(self):
        parse_config("config/default-config.yaml")

    def test_decoration(self):
        self.assertEqual(DecorationType.get_decoration_for_material(Material.SHRUB), None)


class TestTile(unittest.TestCase):

    def test_tile_str(self):
        tile = Tile(Material.HILL, (None, None))
        self.assertEqual(str(tile), Material.HILL.txt)


class TestGenerator(unittest.TestCase):

    def setUp(self):
        config_data1 = {"world": {"width": 5, "height": 5, "continent-size": 10}}
        config_data2 = {"world": {"width": 10, "height": 10, "continent-size": 15}}
        self.seeded_generator = Generator(config_data1, seed=100)
        self.random_generator1 = Generator(config_data2)
        self.random_generator2 = Generator(config_data2)

    def test_seeds_unequal(self):
        self.assertNotEqual(self.seeded_generator.seed, self.random_generator1.seed)
        self.assertNotEqual(self.random_generator1.seed, self.random_generator2.seed)

    def test_correct_seed(self):
        self.assertEqual(str(self.seeded_generator.tile_map[0][0]), '/')
        self.assertEqual(str(self.seeded_generator.tile_map[0][1]), '/')
        self.assertEqual(str(self.seeded_generator.tile_map[1][0]), '_')
        self.assertEqual(str(self.seeded_generator.tile_map[1][1]), '/')

    def test_random_seeds_different(self):
        self.assertNotEqual(str(self.random_generator1.tile_map), str(self.random_generator2.tile_map))

    def test_size_initialization(self):
        self.assertEqual(self.seeded_generator.y_height, 5)
        self.assertEqual(self.seeded_generator.x_height, 5)
        self.assertEqual(self.random_generator1.y_height, 10)
        self.assertEqual(self.random_generator1.x_height, 10)


class TestParser(unittest.TestCase):

    def setUp(self):
        self.config_data = parse_config("config/default-config.yaml")

    def test_parsed_generator_settings(self):
        self.assertEqual(self.config_data["world"]["width"], 100)
        self.assertEqual(self.config_data["world"]["height"], 100)
        self.assertEqual(self.config_data["world"]["continent-size"], 10)

    def test_material_configs(self):
        self.assertEqual(material.deep_shallow_water_border, .44)
        self.assertEqual(material.shallow_water_sand_border, .49)
        self.assertEqual(material.sand_shrub_border, .525)
        self.assertEqual(material.shrub_grass_border, .54)
        self.assertEqual(material.grass_hill_border, .62)
        self.assertEqual(material.hill_mountain_border, .66)
        self.assertEqual(material.mountain_snow_border, .71)

    def test_decoration_config_dict(self):
        config_dict = decoration.config_dict
        self.assertEqual(config_dict["deep-water"], {'None': 100})
        self.assertEqual(config_dict["sand"], {DecorationType.PALM: 5, 'None': 95})
        self.assertEqual(config_dict["mountain"], {DecorationType.EDELWEISS: 6, 'None': 94})


if __name__ == '__main__':
    unittest.main()
