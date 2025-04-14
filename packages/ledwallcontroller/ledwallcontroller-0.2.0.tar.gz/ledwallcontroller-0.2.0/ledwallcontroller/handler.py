import asyncio
from asyncio import Task
from typing import Callable, Optional


class TCPHandler:
    """
    A simplified TCP connection handler that only manages the connection and raw data transmission.

    :param host: The IP-Adress of the host computer running the control software
    :param port: The port used for TCP communication
    :param timeout: Timeout for TCP communication
    """

    def __init__(
        self,
        host: str,
        port: int = 4010,
        timeout: float = 30.0,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._read_task: Optional[Task] = None
        self._response_callbacks: list[Callable[[bytes], None]] = []
        self._lock = asyncio.Lock()

    @property
    def connected(self) -> bool:
        return not (self._writer is None or self._writer.is_closing())

    async def connect(self):
        """Establish TCP connection if not already connected"""
        async with self._lock:
            if not self.connected:
                self._reader, self._writer = await asyncio.open_connection(
                    self.host, self.port
                )
                self._read_task = asyncio.create_task(self._read_responses())

    async def disconnect(self):
        """Close the TCP connection"""
        async with self._lock:
            if self._writer:
                if self._read_task:
                    self._read_task.cancel()
                    try:
                        await self._read_task
                    except asyncio.CancelledError:
                        pass
                    self._read_task = None

                self._writer.close()
                await self._writer.wait_closed()
                self._reader, self._writer = None, None

    def register_callback(self, callback: Callable[[bytes], None]) -> None:
        self._response_callbacks.append(callback)

    async def send_data(self, data: str) -> None:
        """Send raw data over the TCP connection"""
        await self.connect()
        self._writer.write(data.encode("ascii"))
        await self._writer.drain()

    async def _read_responses(self):
        """Continuously read from the TCP connection and pass responses to callback"""
        while self.connected:
            try:
                response = await asyncio.wait_for(
                    self._reader.read(1024), timeout=self.timeout
                )
                if not response:  # Empty response means connection closed
                    continue

                for callback in self._response_callbacks:
                    callback(response)

            except asyncio.TimeoutError:
                pass  # Ignore timeouts and continue listening
            except asyncio.CancelledError:
                break  # Task was cancelled (likely during disconnect)
            except asyncio.IncompleteReadError:
                break  # gets raised on disconnect()
            except Exception as e:
                await self.disconnect()
                raise Exception(f"Error reading responses: {e}") from e
