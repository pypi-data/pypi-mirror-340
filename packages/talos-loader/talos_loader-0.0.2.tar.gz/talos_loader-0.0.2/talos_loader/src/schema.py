from enum import Enum

from pydantic import BaseModel, Field
from talos_aclient import CleanConfig, SplitterConfig, LoaderConfigInput, AutoContextConfig


class TalosParseConfig(BaseModel):
    clean_config: CleanConfig = Field(default_factory=lambda: CleanConfig())
    splitter_config: SplitterConfig = Field(default_factory=lambda: SplitterConfig())
    loader_config: LoaderConfigInput = Field(default_factory=lambda: LoaderConfigInput())
    auto_context_config: AutoContextConfig = Field(default_factory=lambda: AutoContextConfig())


class ContentType(str, Enum):
    title_ = 'title'
    section_header = 'section_header'
    image = 'image'
    text = 'text'
    table = 'table'


class Page(BaseModel):
    page_num: int = 0
    page_height: int = 0
    page_width: int = 0


class Block(BaseModel):
    type: ContentType
    rect: tuple[float, float, float, float] | None = None
    content: str
    font_size: list[float] = []  # font_size of each line/span
    page: Page = Field(default_factory=lambda: Page())
