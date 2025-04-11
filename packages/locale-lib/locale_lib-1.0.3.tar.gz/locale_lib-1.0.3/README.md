# locale-lib
This is a simple lib for localisation your services.
## Installation
Installation is possible using the Python pip command line tool. For you the command to install this library may look like this: 

`pip3 install locale-lib`
## Usage
To use localisation package create instance of `LocaleManager` and get strings via property.


```python
from locale_lib import LocaleManager
from datetime import datetime
locale_man = LocaleManager('./locales').setup()  # FileNotFoundError if not found

locale = locale_man.get(input('enter your country code: '))

...

print(locale.greeting_message)
print(locale.f_time_now.format(time=datetime.now()))
```

./locales/locale_en:
```
greeting_message: hello, user!
f_time_now: Current datetime is:/ {time}
```

./locales/locale_es:
```
greeting_message: hola, usuario!
f_time_now: La fecha actual es:/ {time}
```

./locales/locale_ru:
```
greeting_message: Привет, пользователь!!
f_time_now: Сейчас:/ {time}
```
## Tips
* <code>: </code> must be replaced to <code>:/ </code> (<code>variable_name: value is:/ value</code>)
* To add new line use `\n` in locale file
* `locale.<string>` (or `locale.get(<string>)`) returning instance of `str` class and might be formatted via `format()` method
* Locale file should look like `locale_<country_code>.lc`, other will be skipped

## How it's meant to be used
* Standard strings should look like `var_name: Variable value`
* F-strings should look like `f_var_name: Variable {param_a} {param_d} {param_c} value`

