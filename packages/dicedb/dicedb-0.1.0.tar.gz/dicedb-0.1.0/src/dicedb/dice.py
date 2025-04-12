import socket
from typing import Any

from .commands import DiceCommands
from .exceptions import (
    DiceConnectionError,
    DiceSendCommandError,
    DiceResponseTooLargeError,
    DiceResponseError,
)
from .cmd_pb2 import Command as PBCommand
from .cmd_pb2 import Response as PBResponse
from . import const



def _serialize_as_pytype(resp: PBResponse) -> Any:
    if resp.err:
        return DiceResponseError(resp.err)

    if resp.WhichOneof('value') is not None:
        one_of = resp.WhichOneof('value')
        if one_of == "v_nil" and resp.v_nil:
            return None
        return getattr(resp, one_of)


    if resp.v_ss_map:
        return dict(resp.v_ss_map.items())

    return None



class Dice(DiceCommands):
    """
    An synchronous client for DiceDB.
    """

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        """Initialize the Dice client.

        Args:
            host (str): DiceDB server host
            port (int): DiceDB server port
            timeout (float): Connection timeout in seconds
        """
        self._host = host
        self._port = port
        self._timeout = timeout
        self._socket = None
        self._connected: bool = False
        self._connect()
        self._do_handshake()

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self._timeout)
        try:
            self._socket.connect((self._host, self._port))
            self._connected = True
        except socket.timeout:
            raise DiceConnectionError(
                f'Connection to {self._host}:{self._port} timed out'
            )
        except ConnectionRefusedError:
            raise DiceConnectionError(
                f'Connection to {self._host}:{self._port} was refused'
            )
        except OSError as e:
            raise DiceConnectionError(
                f'Failed to connect to {self._host}:{self._port}: {e}'
            ) from e

    def _do_handshake(self):
        self._handshake()

    def _fire(self, cmd: str, *args):
        if not self._connected:
            raise DiceConnectionError('Not connected to the server.')

        # Create a command protobuf object
        current_command = PBCommand()
        current_command.cmd = cmd
        current_command.args.extend([str(arg) for arg in args])

        self._send_command(current_command)
        return _serialize_as_pytype(self._read_response_and_parse())

    def _send_command(self, cmd: PBCommand):
        byte_string = cmd.SerializeToString()
        try:
            self._socket.sendall(byte_string)
        except OSError as e:
            raise DiceSendCommandError('Failed to send command') from e

    def _read_response_and_parse(self) -> PBResponse:
        buffer = bytearray(const.MAX_REQUEST_SIZE)
        mv = memoryview(buffer)
        received_bytes_size = 0

        while True:
            chunk_view = mv[
                received_bytes_size : received_bytes_size
                + const.IO_BUFFER_SIZE
            ]
            nbytes = self._socket.recv_into(chunk_view)

            if not nbytes:
                break

            received_bytes_size += nbytes
            if received_bytes_size > const.MAX_REQUEST_SIZE:
                raise DiceResponseTooLargeError(
                    f'Response too large: {received_bytes_size} bytes'
                )

            if nbytes < const.IO_BUFFER_SIZE:
                break

        pb_response = PBResponse()
        pb_response.ParseFromString(mv[:received_bytes_size])
        return pb_response

    def close(self):
        """Close the connection to the server.

        Returns:
            None
        """
        if self._socket and self._connected:
            self._socket.close()
            self._connected = False

    def __enter__(self):
        """Enter method for the context manager.

        Returns:
            `Dice`
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method for the context manager.
        Returns:
            None
        """
        self.close()