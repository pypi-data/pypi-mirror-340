
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from .parsers import translation_parser
TEMPLATE = """
You will be given a text in {source_language} and you need to translate it to {target_language}.


The text is as follows:
{input_text}


{format_instructions}
"""

translation_prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant that translates text from one language to another."
        ),
        HumanMessagePromptTemplate.from_template(
            TEMPLATE,
        ),
    ],
    input_variables=["input_text", "source_language", "target_language"],
    partial_variables={
        "format_instructions": translation_parser.get_format_instructions(only_json=True),
    },
)