import json
import os

from pathlib import Path

path = Path("data.json")


def create_new_json_file(filepath):
    with open(filepath, 'w') as file:
        json.dump({}, file)


if not os.path.exists(path):
    print("file not exists")
    create_new_json_file(path)


def write_json_file(data):
    with open(path, "w") as jsonFile:
        json.dump(data, jsonFile)


def read_json_file(filepath):
    with open(filepath, "r") as jsonFile:
        data = json.load(jsonFile)
    return data


def update_json_file():
    if not os.path.exists(path):
        create_new_json_file(path)

    data = read_json_file()
    write_json_file(data)

create_new_json_file(path)
update_json_file()
