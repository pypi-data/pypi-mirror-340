from abc import ABC, abstractmethod

from talos_loader.src.schema import TalosParseConfig, Block


class TalosLoader(ABC):
    def __init__(self, parse_config: TalosParseConfig | None = None):
        self.parse_config = parse_config

    @abstractmethod
    def load(self, contents: bytes) -> list[Block]:
        ...
