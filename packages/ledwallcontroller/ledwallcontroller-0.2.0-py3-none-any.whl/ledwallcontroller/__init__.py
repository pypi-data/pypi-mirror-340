import re
from .controller import Controller, MatchError
from .handler import TCPHandler


class Multivision(Controller):
    """Implementation for the Mulitvision LED Controllers"""

    def __init__(self, connection: TCPHandler, controller_id: int):
        if not (0 <= controller_id <= 99):
            raise ValueError("ID must be 0 ... 99")
        self.controller_id = controller_id
        super().__init__(connection)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._handler.host}', id={self.controller_id})"

    def parse_response(self, response: bytes) -> int:
        """
        Parse the response from the Multivision control PC.
        Expected format: "\\x01LEDRBRIGHXX=YY\\x0D"
        - XX (00-99) is the controller ID.
        - YY (00-100) is the brightness.
        """
        response = response.decode("ascii")
        pattern = rf"\x01LEDRBRIGH{self.controller_id:02d}=(\d+)\x0d"
        match = re.search(pattern, response)
        if not match:
            raise MatchError()

        brightness = int(match.group(1))

        if not (0 <= brightness <= 100):
            raise ValueError(f"Received invalid brightness value: {brightness}")

        return brightness

    def get_update_command(self) -> str:
        return f"\x01LEDGBRIGH{self.controller_id:02d}=?\x0d"

    def get_set_brightness_command(self, brightness_percent: int):
        if not 0 <= brightness_percent <= 100:
            raise ValueError("Brightness value must be between 0 and 100")

        return f"\x01LEDSBRIGH{self.controller_id:02d}={brightness_percent}\x0d"


class OnlyGlass(Controller):
    """Implementation for the OnlyGlass LED Controllers"""

    def __init__(self, connection: TCPHandler):
        super().__init__(connection)

    def parse_response(self, response: bytes) -> int:
        """
        Parse the response from the Only Glass Controller
        Expected format: "RP\r\x07\xb9..." where
        Byte 6: Brightness,
        Byte 7: Red,
        Byte 8: Green,
        Byte 9: Blue
        """

        if not response.startswith(b"RP"):
            raise MatchError()

        if len(response) < 6:
            raise ValueError(
                f"Expected response length to be at least 6, got {len(response)}, response: {response}"
            )

        brightness = int(response[5])  # cast 6th byte to an int
        return brightness

    def get_update_command(self) -> str:
        return "RP\x0d"

    def get_set_brightness_command(self, brightness_percent: int):
        """Get a string command to set the brightness.

        Expected Format:"SH"+CHAR+0x0d where CHAR represents the brightness as an ascii char (eg. "2" = 50% as 50 is the integer representation for the char "2")."""

        if not 0 <= brightness_percent <= 100:
            raise ValueError("Brightness value must be between 0 and 100")

        brightnes_char = chr(brightness_percent)
        return f"SH{brightnes_char}\x0d"
