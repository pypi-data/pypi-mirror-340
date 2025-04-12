from component_repo import ComponentMetadata, ComponentRepo, IComponentProvider
import requests
from typing import Any, Type, Optional
from pydantic import BaseModel, ValidationError
from scraipe import IAnalyzer, IScraper
import logging

_default_links = [
    "https://example.com",
    "https://rickandmortyapi.com/api/character/1",
    "https://ckaestne.github.io/seai/"
]

def get_default_links():
    """
    Get the default links for the scrapers.
    
    Returns:
        list: A list of default links.
    """
    return _default_links.copy()


from scraipe.defaults import (
    TextScraper,
    RawScraper,
    TextStatsAnalyzer,
)

from scraipe.extended import (
    TelegramMessageScraper,
    NewsScraper,
    TelegramNewsScraper,
    OpenAiAnalyzer,
    GeminiAnalyzer
)

class DefaultcomponentProvider(IComponentProvider):
    def __init__(self, schema:Type[BaseModel], target_class:Type[IAnalyzer|IScraper], default_config:BaseModel = None):
        self.schema = schema
        self.target_class = target_class
        self.default_config = default_config
        try: 
            # Validate the default config against the schema
            if default_config:
                validated_config = self.schema(**default_config.model_dump())
        except ValidationError as e:
            raise Exception("Default config validation failed.") from e
    def get_config_schema(self) -> Type[BaseModel]:
        return self.schema
    def get_component(self, config:BaseModel) -> Any:
        # Validate the config against the schema
        validated_config = self.schema(**config.model_dump())
        # Create an instance of the target class with the validated config
        component = self.target_class(**validated_config.model_dump())
        return component
    def get_default_config(self):
        return self.default_config

from typing_extensions import Annotated
from pydantic import Field
class LlmAnalyzerSchema(BaseModel):
    api_key: str = Field(..., description="API key for the LLM service.")
    instruction:str = Field(..., format="multi-line", description="Craft an instruction prompt to tell the LLM how to analyze the content.")
    

_default_scrapers = [
    (TextScraper(), ComponentMetadata(
        name="Text Scraper", description="Scrapes visible text from a website.")),
    (NewsScraper(), ComponentMetadata(
        name="News Scraper", description="Scrapes and cleans news articles.")),
    (RawScraper(), ComponentMetadata(
        name="Raw Scraper", description="Scrapes raw HTTP content.")),
]


import os
default_llm_instruction = \
"""Identify market gaps from the text with a focus on unmet needs or complaints.
Output the result with the following JSON format:
{
    "gaps": [need1, ...]
}"""
default_openai_config = LlmAnalyzerSchema(
    api_key=os.getenv("OPENAI_API_KEY", ""),
    instruction=default_llm_instruction
    )
default_gemini_config = LlmAnalyzerSchema(
    api_key=os.getenv("GEMINI_API_KEY", ""),
    instruction=default_llm_instruction
    )
_default_analyzers = [
    (TextStatsAnalyzer(), ComponentMetadata(
        name="Text Stats Analyzer", description="Computes word count, character count, sentence count, and average word length.")),
    (DefaultcomponentProvider(LlmAnalyzerSchema, target_class= OpenAiAnalyzer, default_config=default_openai_config), ComponentMetadata(
        name="OpenAI Analyzer", description="Analyzes text using the OpenAI API. Set the API key and instruction in the config.")),
    (DefaultcomponentProvider(LlmAnalyzerSchema, target_class= GeminiAnalyzer, default_config=default_gemini_config), ComponentMetadata(
        name="Gemini Analyzer", description="Analyzes text using the Gemini API. Set the API key and instruction in the config.")),
]

def register_default_components(repo: ComponentRepo):
    """
    Register default components with the component repository.
    
    Args:
        repo (ComponentRepo): The component repository to register components with.
    """
    # Register default scrapers
    for scraper in _default_scrapers:
        repo.register_scraper(scraper[0], scraper[1])
    
    # Register default analyzers
    for analyzer in _default_analyzers:
        repo.register_analyzer(analyzer[0], analyzer[1])