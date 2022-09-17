import yaml
from material import set_values
import decoration
from decoration import update_decoration_config
from decoration import DecorationType

""" Parses through the config file and initializes generation data

 Updates the Material and Decoration modules so they don't have to 
 read in data from the config files themselves
"""


def parse_config(filepath):

    with open(filepath, "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)

    set_values(data["world"]["material-heights"])

    decoration.aging_speed = data["world"]["aging-speed"]
    decos = data["world"]["decorations"]
    new_decos = {}
    for material in decos:
        material_dict = {}
        for key in decos[material]:
            # Check which decoration this entry is for
            if key == "None":
                material_dict["None"] = decos[material][key]
            else:
                for deco in DecorationType:
                    if deco.id_name == key:
                        material_dict[deco] = decos[material][key]
                        break
        new_decos[material] = material_dict

    update_decoration_config(new_decos)
    return data
