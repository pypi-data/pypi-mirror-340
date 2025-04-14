

from dotenv import load_dotenv
from syncmaster_commons.translator.base import Translator

load_dotenv()  # Load .env file into os.environ
def test_translator():

    sample_english = "Hello, how are you?"

    target_language = "Marathi"

    translator = Translator()

    # Test translation
    translated_text = translator.translate(
        text=sample_english,
        target_language=target_language,
    )
    assert translated_text is not None
    assert translated_text != sample_english
    assert isinstance(translated_text, str)