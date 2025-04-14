from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetAuthorizationRequest(_message.Message):
    __slots__ = ("principal_id", "project_id", "organization_id", "roles")
    PRINCIPAL_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    principal_id: str
    project_id: str
    organization_id: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, principal_id: _Optional[str] = ..., project_id: _Optional[str] = ..., organization_id: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ...) -> None: ...
