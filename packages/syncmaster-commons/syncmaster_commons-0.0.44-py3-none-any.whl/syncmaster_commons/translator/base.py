from langchain_openai import ChatOpenAI
import os
from .parsers import translation_parser
from .prompt import translation_prompt

class Translator:

    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.0):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            api_key=os.getenv("SYNC_OPENAI_API_KEY"),
        )
    
    @property
    def translator(self):
        chain =  translation_prompt |  self.llm | translation_parser
        # print("Chain:", chain)
        return chain

    def translate(self, text: str, target_language: str, source_language: str = "en" ) -> str:
        """Translate text from source_language to target_language."""
        response =  self.translator.invoke(
            {
                "input_text": text,
                "source_language": source_language,
                "target_language": target_language,
            }
        )
        return response["translation"]
