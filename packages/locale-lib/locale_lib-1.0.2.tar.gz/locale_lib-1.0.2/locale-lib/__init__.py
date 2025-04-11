import os

class Locale:
    code: str

    def __init__(self, code: str, dictionary: dict[str, str]):
        self.code = code
        for arg, val in dictionary.items():
            setattr(self, arg, val)

    def get(self, word: str, default: str = ''):
        try:
            return eval(f'self.{word}', {'self': self})
        except AttributeError:
            return default

    def add(self, word: str, locale: str) -> None:
        setattr(self, word, locale)

    def __getitem__(self, item):
        try:
            return eval(f'self.{item}', {'self': self})
        except NameError:
            return f'{item} (translation missing)'


class LocaleManager:
    locales: list[Locale] = []

    def __init__(self, locale_folder: str):
        if not os.path.exists(locale_folder):
            raise FileNotFoundError(f'locale folder {locale_folder} not found')
        self.locales_folder = locale_folder

    def setup(self):
        if self.locales_folder:
            import os
            for filename in os.listdir(self.locales_folder):
                if not filename.startswith('locale_') and not filename.endswith('.lc'):
                    continue
                with open(os.path.join(self.locales_folder, filename), 'r', encoding='utf-8') as file:
                    locale_dict = {}
                    lines = file.read().split('\n')
                    code = filename[filename.rfind('_') + 1: filename.rfind('.')]
                    for entry in lines:
                        if entry == '':
                            continue

                        key, val = entry.split(': ')
                        val = val.replace(':/ ', ': ').replace('\\n', '\n')
                        locale_dict[key] = val

                    self.locales.append(Locale(code, locale_dict))
            return self

    def get(self, code: str) -> Locale:
        for locale in self.locales:
            if locale.code == code:
                return locale
        raise KeyError
