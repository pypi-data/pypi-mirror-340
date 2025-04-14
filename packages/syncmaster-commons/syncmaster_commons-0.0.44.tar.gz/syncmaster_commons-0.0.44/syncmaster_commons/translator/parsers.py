from langchain.output_parsers.structured import ResponseSchema, StructuredOutputParser


schema = ResponseSchema(
    name="translation",
    description="translated text in the target language",
    type="string",
)


translation_parser = StructuredOutputParser.from_response_schemas(
    response_schemas=[schema],
)

