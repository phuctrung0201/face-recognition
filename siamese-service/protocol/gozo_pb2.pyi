from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PredictReply(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class PredictRequest(_message.Message):
    __slots__ = ["file"]
    FILE_FIELD_NUMBER: _ClassVar[int]
    file: bytes
    def __init__(self, file: _Optional[bytes] = ...) -> None: ...

class StoreFaceReply(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class StoreFaceRequest(_message.Message):
    __slots__ = ["file", "name"]
    FILE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    file: bytes
    name: str
    def __init__(self, file: _Optional[bytes] = ..., name: _Optional[str] = ...) -> None: ...
