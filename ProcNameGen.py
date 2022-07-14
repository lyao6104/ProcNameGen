import string

import src.names as names
import src.util as util
from src.names_util import *

# languages = get_saved_languages("./languages")
# print(f"Found {len(languages)} saved languages:")
# for name in languages.keys():
#     print(f"- {name}")

# language = load_language(list(languages.values())[0])
language = Language.language_template()
for i in range(0, 10):
    print(f"{i}. {language.get_name()}")

save_language("./languages/TestLang.json", language, True)
