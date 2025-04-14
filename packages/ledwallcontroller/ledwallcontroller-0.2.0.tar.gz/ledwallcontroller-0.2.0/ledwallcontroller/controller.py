import asyncio
from typing import Optional
from .api import API
from .handler import TCPHandler


class MatchError(Exception):
    """Is used, when the message won't be handled by the controller"""


class Controller(API):
    """A dataclass to cache the state of a LED Controller and handle number-conversion."""

    def __init__(self, handler: TCPHandler):
        self._handler = handler
        self._pending_update: Optional[asyncio.Future] = None
        self._handler.register_callback(self._on_response)
        self._brightness_percent: Optional[int] = None

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._handler.host}')"

    async def connect(self):
        """Connect to the TCP host."""
        await self._handler.connect()

    async def disconnect(self):
        """Disconnect from the TCP host."""
        await self._handler.disconnect()

    async def update(self, timeout=3) -> None:
        """Requests a the current brightness value from the controller. A timeout can be specified in seconds."""
        if self._pending_update and not self._pending_update.done():
            raise RuntimeError("Update already in progress")

        self._pending_update = asyncio.Future()

        command = self.get_update_command()
        await self._handler.send_data(command)

        try:
            brightness = await asyncio.wait_for(self._pending_update, timeout)
            self._brightness_percent = brightness
        except asyncio.CancelledError:
            pass
        finally:
            # still gets called before returning from the function
            self._pending_update = None

    async def set_brightness_percent(self, brightness: int):
        """Set the brightness in percent (0-100) for a controller."""
        if not (0 <= brightness <= 100):
            raise ValueError("Brightness must be between 0 and 100.")

        command = self.get_set_brightness_command(brightness)
        await self._handler.send_data(command)

    async def set_brightness_normalized(self, brightness: float):
        """Set the brightness as a normalized value (0.0-1.0) for a controller."""
        if not (0 <= brightness <= 1):
            raise ValueError("Brightness must be between 0.0 and 1.0.")

        await self.set_brightness_percent(int(brightness * 100))

    async def set_brightness_8bit(self, brightness: int):
        """Set the brightness as an 8-bit value (0-255) for a controller."""
        if not (0 <= brightness <= 255):
            raise ValueError("Brightness must be between 0 and 255.")

        await self.set_brightness_percent(int(brightness / 255 * 100))

    @property
    def brightness_normalized(self) -> float:
        """Get the normalized brightness 0. ... 1."""
        if self._brightness_percent is None:
            return None

        return self._brightness_percent / 100

    @property
    def brightness_8bit(self):
        """Get the brightness as an 8bit int 0 ... 255"""
        if self._brightness_percent is None:
            return None

        return int(self._brightness_percent / 100 * 255)

    @property
    def brightness_percent(self) -> int:
        """Get the brightness in percent 0 ... 100"""
        return self._brightness_percent

    def _on_response(self, response: bytes):
        try:
            brightness = self.parse_response(response)

            if self._pending_update and not self._pending_update.done():
                self._pending_update.set_result(brightness)
        except MatchError:
            pass
        except Exception:
            if self._pending_update and not self._pending_update.done():
                self._pending_update.cancel()
            raise
