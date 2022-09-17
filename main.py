import numpy as np
import argparse
import game
from generator import Generator
from config_parser import parse_config

parser = argparse.ArgumentParser(description="Manage creation, loading and saving of world maps")
group = parser.add_mutually_exclusive_group()
group.add_argument("-r", "--read", type=str, help="File containing world map to be read in")
group.add_argument("-w", "--write", type=str, help="Location to output world map to")
parser.add_argument("--debug", type=bool, help="Prints a text representation of the map before saving/ after loading")
parser.add_argument("-c", "--config", type=str, help="Path to a YAML config file")
args = parser.parse_args()

""" Main and its helper functions

 argparse variables are listed above everything,
 main does nothing if not called with either -w or -r
 If called with -w and a file name, it creates a world and saves it to that file
 If called with -r and a file name, it reads that file in and represents it as a numpy array
 
 Otherwise, it starts up pygame and opens up the window
"""


def main():
    if args.config is not None:
        config_data = parse_config(args.config)
    else:
        config_data = parse_config("config/default-config.yaml")

    if args.read is not None:
        loaded_tile_map = read_map(args.read)
        if args.debug:
            for row in loaded_tile_map:
                print([str(tile) for tile in row])
        game.start_game(config_data, loaded_tile_map)
        return
    elif args.write is not None:
        tile_map = game.start_game(config_data)
        write_map(args.write, tile_map)
        return

    game.start_game(config_data)


def write_map(output_file, data):
    if args.debug:
        for row in data:
            print([str(tile) for tile in row])
    np.save(output_file, data)


def read_map(input_file):
    data = np.load(input_file, allow_pickle=True)
    return data


if __name__ == '__main__':
    main()
