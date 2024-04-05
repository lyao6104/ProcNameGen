import json
from os import walk
from typing import Dict

from .names import *


def load_language(path: str) -> Language:
    with open(path, "r", encoding="utf-8") as file:
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
        with open(path, "x", encoding="utf-8") as _:
            pass
    except FileExistsError:
        if not overwrite:
            print(
                f'Warning: Language "{language.name}" not saved as file already exists.'
            )
            return

    with open(path, "w", encoding="utf-8") as file:
        file.write(language.to_json(pretty=True))


def get_saved_languages(languages_path: str) -> Dict[str, str]:
    languages = {}
    for dir_path, _, file_names in walk(languages_path):
        for file_name in file_names:
            language_path = f"{dir_path}/{file_name}"
            with open(language_path, "r", encoding="utf-8") as language_file:
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


def scan_names(
    names_path: str, order: int = 2, language_name: str = "New Language"
) -> Language:
    names = []
    with open(names_path, "r", encoding="utf-8") as file:
        names = file.readlines()
        names = list(map(lambda name: name.strip(), names))
    segments = {}
    openers = {}
    for name in names:
        if name[0].lower() in openers:
            openers[name[0].lower()] += 1
        else:
            openers[name[0].lower()] = 1
        for i in range(1, order + 1):
            for j in range(0, len(name)):
                if j + i > len(name):
                    continue
                cur_segment = name[j].lower()
                if cur_segment not in segments:
                    segments[cur_segment] = []

                next_segment = name[j + 1 : j + 1 + i].lower()
                if not next_segment:
                    continue

                contains_next = False
                for k, (key, p) in enumerate(segments[cur_segment]):
                    if key == next_segment:
                        segments[cur_segment][k] = (key, p + 1)
                        contains_next = True
                        break
                if not contains_next:
                    segments[cur_segment].append((next_segment, 1))

    segment_type = SegmentType("Base Segment", 1, segments)
    # Note that average length will just be auto-calculated,
    # since we only have number of letters here, not segments.
    new_lang = Language(
        language_name,
        [segment_type],
        openers,
        round(len(min(names, key=len)) * 1.2),
        round(len(max(names, key=len)) * 0.8),
    )
    return new_lang
