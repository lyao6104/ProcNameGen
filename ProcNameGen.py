import string

import src.names as names

language = names.Language.new_language("TestLang")
for i in range(0, 10):
    print(f"{i}. {language.get_name()}")
