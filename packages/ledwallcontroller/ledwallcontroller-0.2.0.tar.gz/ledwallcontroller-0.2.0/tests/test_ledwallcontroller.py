from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ledwallcontroller import Controller, MatchError, Multivision, OnlyGlass, TCPHandler


@pytest.fixture
def mock_connection():
    conn = MagicMock()
    conn.send_data = AsyncMock()
    return conn


@pytest.fixture
def multivision(mock_connection):
    return Multivision(mock_connection, controller_id=1)


@pytest.fixture
def onlyglass(mock_connection):
    return OnlyGlass(mock_connection)


class TestController:
    @patch.multiple(Controller, __abstractmethods__=set())
    def test_brightness_conversion(self, mock_connection):
        controller = Controller(mock_connection)
        controller._brightness_percent = 50
        assert controller.brightness_percent == 50
        assert controller.brightness_8bit == 127
        assert controller.brightness_normalized == pytest.approx(0.5)


class TestMultivision:
    def test_get_update_command(self, multivision):
        assert multivision.get_update_command() == "\x01LEDGBRIGH01=?\x0d"

    def test_get_set_brightness_command(self, multivision):
        assert multivision.get_set_brightness_command(50) == "\x01LEDSBRIGH01=50\x0d"

    def test_parse_response_valid(self, multivision):
        response = b"\x01LEDRBRIGH01=75\x0d"
        assert multivision.parse_response(response) == 75

    def test_parse_response_invalid_format(self, multivision):
        response = b"\x01LEDRTRIGH99=75\x0d"
        with pytest.raises(MatchError):
            multivision.parse_response(response)

    def test_parse_response_invalid_brightness(self, multivision):
        response = b"\x01LEDRBRIGH01=150\x0d"
        with pytest.raises(ValueError):
            multivision.parse_response(response)

    @pytest.mark.asyncio
    async def test_set_brightness_valid(self, multivision, mock_connection):
        await multivision.set_brightness_percent(50)
        mock_connection.send_data.assert_called_with("\x01LEDSBRIGH01=50\x0d")

    @pytest.mark.asyncio
    async def test_set_brightness_invalid(self, multivision):
        with pytest.raises(ValueError):
            await multivision.set_brightness_percent(200)

    @pytest.mark.asyncio
    async def test_update(self, multivision, mock_connection):
        async def mock_send_data(command):
            if multivision._pending_update and not multivision._pending_update.done():
                multivision._pending_update.set_result(69)

        mock_connection.send_data.side_effect = mock_send_data

        await multivision.update()
        mock_connection.send_data.assert_called_with("\x01LEDGBRIGH01=?\x0d")
        assert multivision.brightness_percent == 69


class TestOnlyGlass:
    def test_get_update_command(self, onlyglass):
        assert onlyglass.get_update_command() == "RP\x0d"

    def test_get_set_brightness_command_valid(self, onlyglass):
        assert onlyglass.get_set_brightness_command(50) == "SH2\x0d"

    def test_get_set_brightness_command_invalid(self, onlyglass):
        with pytest.raises(ValueError):
            onlyglass.get_set_brightness_command(101)

    def test_parse_response_valid(self, onlyglass):
        response = b"RP\x0d\x07\xb9\x32\x64\x64\x64"
        assert onlyglass.parse_response(response) == 50

    def test_parse_response_invalid_prefix(self, onlyglass):
        with pytest.raises(MatchError):
            response = b"WRONGFORMAT"
            onlyglass.parse_response(response)

    def test_parse_response_invalid_length(self, onlyglass):
        with pytest.raises(
            ValueError,
            match="Expected response length to be at least 6, got 4, response: b'RPDF'",
        ):
            response = b"RPDF"
            onlyglass.parse_response(response)

    @pytest.mark.asyncio
    async def test_set_brightness_valid(self, onlyglass, mock_connection):
        await onlyglass.set_brightness_percent(50)
        mock_connection.send_data.assert_called_with("SH2\x0d")

    @pytest.mark.asyncio
    async def test_update(self, onlyglass, mock_connection):
        async def mock_send_data(command):
            if onlyglass._pending_update and not onlyglass._pending_update.done():
                onlyglass._pending_update.set_result(33)

        mock_connection.send_data.side_effect = mock_send_data

        await onlyglass.update()
        mock_connection.send_data.assert_called_with("RP\x0d")
        assert onlyglass.brightness_percent == 33


@pytest.fixture
async def tcp_handler():
    handler = TCPHandler(host="localhost", port=4010)
    return handler


class TestTCPHandler:
    @pytest.mark.asyncio
    async def test_connect(self, tcp_handler):
        with patch("asyncio.open_connection", new_callable=AsyncMock) as mock_open:
            mock_reader, mock_writer = AsyncMock(), AsyncMock()
            mock_writer.is_closing.return_value = False
            mock_open.return_value = (mock_reader, mock_writer)

            assert not tcp_handler.connected

            await tcp_handler.connect()

            mock_open.assert_called_once_with("localhost", 4010)

            assert tcp_handler._reader is mock_reader
            assert tcp_handler._writer is mock_writer

    @pytest.mark.asyncio
    async def test_disconnect(self, tcp_handler):
        tcp_handler._reader = AsyncMock()
        tcp_handler._writer = AsyncMock()
        tcp_handler._writer.wait_closed = AsyncMock()
        tcp_handler._writer.is_closing.return_value = False
        tcp_handler._read_task = None

        writer = tcp_handler._writer
        await tcp_handler.disconnect()

        writer.close.assert_called_once()
        writer.wait_closed.assert_called_once()
        assert tcp_handler._writer is None
        assert tcp_handler._reader is None
        assert tcp_handler._read_task is None

    @pytest.mark.asyncio
    async def test_send_data(self, tcp_handler):
        tcp_handler._writer = AsyncMock()
        tcp_handler._writer.is_closing.return_value = False
        tcp_handler._reader = AsyncMock()
        tcp_handler.connect = AsyncMock()

        await tcp_handler.send_data("TESTCOMMAND")

        tcp_handler.connect.assert_called_once()
        tcp_handler._writer.write.assert_called_with(b"TESTCOMMAND")
        tcp_handler._writer.drain.assert_called_once()

    @pytest.mark.asyncio
    async def test_response_handling(self, tcp_handler):
        callback = MagicMock()
        tcp_handler.register_callback(callback)

        fake_response = b"\x01LEDRBRIGH03=50\x0d"

        for cb in tcp_handler._response_callbacks:
            cb(fake_response)

        callback.assert_called_once_with(fake_response)
