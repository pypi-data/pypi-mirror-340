from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CheckAuthorizationRequest(_message.Message):
    __slots__ = ("principal_id", "permission", "resource_id")
    PRINCIPAL_ID_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    principal_id: str
    permission: str
    resource_id: str
    def __init__(self, principal_id: _Optional[str] = ..., permission: _Optional[str] = ..., resource_id: _Optional[str] = ...) -> None: ...

class CheckAuthorizationResponse(_message.Message):
    __slots__ = ("authorized",)
    AUTHORIZED_FIELD_NUMBER: _ClassVar[int]
    authorized: bool
    def __init__(self, authorized: bool = ...) -> None: ...
