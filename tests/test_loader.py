import pytest
import ruamel.yaml
from os import path
from src.loader import Loader

yaml = ruamel.yaml.YAML()

with open("settings.yaml") as f:
    settings = yaml.load(f)
    f.close()


def test_build_path():
    loader = Loader(settings)
    current_path = path.dirname(__file__)
    path_string = path.split(current_path)

    loader.build_path()

    assert loader.data_folder == path_string[0] + "/src/data"
    assert loader.img_folder == path_string[0] + "/src/data/img"
