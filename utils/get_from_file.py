from pathlib import Path
import json
PROJECT_DIR = Path(__file__).parent
DICT_FILE_PATH = PROJECT_DIR / '../dictionary.json'
JS_FILE_PATH = PROJECT_DIR / '../alter_sources.js'


def get_dict_data() -> list:
    with open(DICT_FILE_PATH, "r", encoding="utf-8") as file:
        words: list = json.load(file)["dictionary"]
    return words

def get_js_commands() -> str:
    with open(JS_FILE_PATH, "r", encoding="utf-8") as file:
        return file.read()
