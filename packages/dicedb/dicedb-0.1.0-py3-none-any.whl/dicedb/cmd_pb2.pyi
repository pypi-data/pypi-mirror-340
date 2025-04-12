from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Command(_message.Message):
    __slots__ = ["args", "cmd"]
    ARGS_FIELD_NUMBER: ClassVar[int]
    CMD_FIELD_NUMBER: ClassVar[int]
    args: _containers.RepeatedScalarFieldContainer[str]
    cmd: str
    def __init__(self, cmd: Optional[str] = ..., args: Optional[Iterable[str]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["attrs", "err", "v_bytes", "v_float", "v_int", "v_list", "v_nil", "v_ss_map", "v_str"]
    class VSsMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    ATTRS_FIELD_NUMBER: ClassVar[int]
    ERR_FIELD_NUMBER: ClassVar[int]
    V_BYTES_FIELD_NUMBER: ClassVar[int]
    V_FLOAT_FIELD_NUMBER: ClassVar[int]
    V_INT_FIELD_NUMBER: ClassVar[int]
    V_LIST_FIELD_NUMBER: ClassVar[int]
    V_NIL_FIELD_NUMBER: ClassVar[int]
    V_SS_MAP_FIELD_NUMBER: ClassVar[int]
    V_STR_FIELD_NUMBER: ClassVar[int]
    attrs: _struct_pb2.Struct
    err: str
    v_bytes: bytes
    v_float: float
    v_int: int
    v_list: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    v_nil: bool
    v_ss_map: _containers.ScalarMap[str, str]
    v_str: str
    def __init__(self, err: Optional[str] = ..., v_nil: bool = ..., v_int: Optional[int] = ..., v_str: Optional[str] = ..., v_float: Optional[float] = ..., v_bytes: Optional[bytes] = ..., attrs: Optional[Union[_struct_pb2.Struct, Mapping]] = ..., v_list: Optional[Iterable[Union[_struct_pb2.Value, Mapping]]] = ..., v_ss_map: Optional[Mapping[str, str]] = ...) -> None: ...
