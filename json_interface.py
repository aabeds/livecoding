import json
import os

from pathlib import Path


def create_new_json_file(filepath):
    with open(filepath, 'w') as file:
        json.dump({}, file)


def write_json_file(filepath, data):
    with open(filepath, "w") as jsonFile:
        json.dump(data, jsonFile)


def read_json_file(filepath):
    with open(filepath, "r") as jsonFile:
        data = json.load(jsonFile)
    return data


def update_json_file(path):
    if not os.path.exists(path):
        create_new_json_file(path)

    data = read_json_file(path)
    write_json_file(data)
