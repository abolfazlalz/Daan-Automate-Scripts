import yaml
from yaml import Loader
from os import path


setting_path = 'config.yml'


def set(data: dict[str, str]):
    file = open(setting_path, 'w')
    yml = yaml.dump(data)
    file.write(yml)


def create():
    username = input("Enter your Daan username: ")
    password = input("Enter your Daan password: ")

    data = {
        "username": username,
        "password": password
    }

    set(data)
    return data


def get() -> dict[str, str]:
    if not path.exists(setting_path):
        return create()
    file = open(setting_path, 'r')
    return yaml.load(file, Loader=Loader)
