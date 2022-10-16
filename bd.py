import googletrans

print(googletrans.LANGUAGES)
from googletrans import Translator


translator = Translator()
result = translator.translate('apple')
