from abc import ABC, abstractmethod


class API(ABC):
    """Methods for updating and setting the brightness values"""

    @abstractmethod
    def parse_response(self, response: bytes) -> int:
        """Parses the response and return the brightness in percent"""
        pass

    @abstractmethod
    def get_update_command(self) -> str:
        pass

    @abstractmethod
    def get_set_brightness_command(self, brightness_percent: int) -> str:
        pass
