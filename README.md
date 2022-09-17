# fa21-cs242-project

This project represents a world generator, build on a simple perlin noise
algorithm. It can be tested by running main.py in the command line with arguments.

Basic Random Map:
python main.py

Create a map that will be saved to "file_name_here":
python main.py -w "file_name_here"

Read a saved map from "file_name_here.npy":
python main.py -r "file_name_here.npy"

Add "--debug true" to the end of either command to print
a text representation of the map to the terminal

Create a map using a specific config file: 
python main.py -c "config/config_file_name.yaml"

See the config folder for examples of what can be done with config files


When in game, move using WASD and zoom using the scroll wheel. 

Terrain can be lowered and raised with left and right click respectively.
