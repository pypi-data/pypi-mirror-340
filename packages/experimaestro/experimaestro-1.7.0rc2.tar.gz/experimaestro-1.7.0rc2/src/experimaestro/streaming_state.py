"""Handles streaming states

Allows to track a global state via a file

- partial states can be output
- every K bytes, a global state is output

The reader can then recover quickly by seeking the last global state output.

"""

import struct
from io import BufferedWriter, BufferedReader, SEEK_END
from typing import Type, Generator, Union

from google.protobuf.message import Message

# Constants
PARTIAL_UPDATE = 1
GLOBAL_STATE = 2
HEADER_FORMAT = ">BI"  # 1-byte type tag, 4-byte message size
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
MAGIC_NUMBER = b"\xab\xcd\xef\x00"
MAGIC_SIZE = len(MAGIC_NUMBER)


class StreamingStateWriter:
    def __init__(
        self,
        file: BufferedWriter,
        partial_cls: Type[Message],
        snapshot_cls: Type[Message],
        chunk_size: int = 8192,
    ):
        self.file = file
        self.partial_cls = partial_cls
        self.snapshot_cls = snapshot_cls
        self.chunk_size = chunk_size
        self.bytes_since_last_snapshot = 0

    def write_partial(self, message: Message):
        assert isinstance(message, self.partial_cls)
        self._write_message(PARTIAL_UPDATE, message)

    def write_snapshot_if_needed(self, message: Message):
        assert isinstance(message, self.snapshot_cls)
        if self.bytes_since_last_snapshot >= self.chunk_size:
            self._write_message(GLOBAL_STATE, message, with_magic=True)
            self.bytes_since_last_snapshot = 0

    def _write_message(self, type_tag: int, message: Message, with_magic: bool = False):
        data = message.SerializeToString()
        header = struct.pack(HEADER_FORMAT, type_tag, len(data))
        if with_magic:
            self.file.write(MAGIC_NUMBER)
            self.bytes_since_last_snapshot += MAGIC_SIZE
        self.file.write(header + data)
        self.file.flush()
        self.bytes_since_last_snapshot += HEADER_SIZE + len(data)


class StreamingStateReader:
    def __init__(
        self,
        file: BufferedReader,
        partial_cls: Type[Message],
        snapshot_cls: Type[Message],
    ):
        self.file = file
        self.partial_cls = partial_cls
        self.snapshot_cls = snapshot_cls

    def __iter__(self) -> Generator[Union[Message, Message], None, None]:
        while True:
            peek = self.file.peek(MAGIC_SIZE)[:MAGIC_SIZE]
            if peek == MAGIC_NUMBER:
                self.file.read(MAGIC_SIZE)

            header = self.file.read(HEADER_SIZE)
            if len(header) < HEADER_SIZE:
                break

            type_tag, length = struct.unpack(HEADER_FORMAT, header)
            payload = self.file.read(length)

            if type_tag == PARTIAL_UPDATE:
                msg = self.partial_cls()
            elif type_tag == GLOBAL_STATE:
                msg = self.snapshot_cls()
            else:
                raise ValueError(f"Unknown type tag: {type_tag}")

            msg.ParseFromString(payload)
            yield msg

    def seek_last_snapshot(self) -> Union[Message, None]:
        self.file.seek(0, SEEK_END)
        file_size = self.file.tell()

        window = 4096
        pos = file_size

        while pos > 0:
            read_size = min(window, pos)
            pos -= read_size
            self.file.seek(pos)
            data = self.file.read(read_size)

            idx = data.rfind(MAGIC_NUMBER)
            if idx != -1:
                snapshot_pos = pos + idx + MAGIC_SIZE
                self.file.seek(snapshot_pos)
                header = self.file.read(HEADER_SIZE)
                if len(header) < HEADER_SIZE:
                    break
                type_tag, length = struct.unpack(HEADER_FORMAT, header)
                if type_tag != GLOBAL_STATE:
                    continue
                payload = self.file.read(length)
                msg = self.snapshot_cls()
                msg.ParseFromString(payload)
                return msg

        return None
