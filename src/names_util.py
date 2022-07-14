import json
from math import log
from os import walk
from typing import Dict

from .names import *


def load_language(path: str) -> Language:
    with open(path, "r") as file:
        language_dict = json.loads(file.read())
        return Language(
            language_dict["name"],
            [
                SegmentType(
                    st["name"],
                    st["probability"],
                    st["segments"],
                )
                for st in language_dict["segmentTypes"]
            ],
            language_dict["openers"],
            language_dict["minSegments"],
            language_dict["maxSegments"],
        )


def save_language(path: str, language: Language, overwrite: bool = False) -> None:
    # First open the given path in read mode to see if it already exists.
    try:
        with open(path, "x") as _:
            pass
    except FileExistsError:
        if not overwrite:
            print(
                f'Warning: Language "{language.name}" not saved as file already exists.'
            )
            return

    with open(path, "w") as file:
        file.write(language.to_json(pretty=True))


def get_saved_languages(languages_path: str) -> Dict[str, str]:
    languages = {}
    for (dir_path, _, file_names) in walk(languages_path):
        for file_name in file_names:
            language_path = f"{dir_path}/{file_name}"
            with open(language_path, "r") as language_file:
                language_name = json.loads(language_file.read())["name"]
                languages[language_name] = language_path
    return languages


def train_language(language_path: str):
    language = load_language(language_path)
    user_input = ""
    while user_input != "stop":
        generated_name = language.get_name()
        user_input = input(
            f"Is {generated_name} a good name for the {language.name} language (stop/y/N)? "
        )

        # Increase probability of encountering segments that are in good names
        if user_input == "y":
            language.mark_name(generated_name, True)
        elif user_input == "stop":
            save_language(language_path, language, True)
        # Decrease probability of bad segments
        else:
            language.mark_name(generated_name, False)
