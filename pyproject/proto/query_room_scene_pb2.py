# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: query_room_scene.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='query_room_scene.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x16query_room_scene.proto\"\'\n\x14query_room_scene_req\x12\x0f\n\x07room_id\x18\x01 \x02(\r\"H\n\x14query_room_scene_rsp\x12\x0b\n\x03ret\x18\x01 \x02(\r\x12\x0f\n\x07room_id\x18\x02 \x02(\r\x12\x12\n\nscene_name\x18\x03 \x02(\x0c')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_QUERY_ROOM_SCENE_REQ = _descriptor.Descriptor(
  name='query_room_scene_req',
  full_name='query_room_scene_req',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_id', full_name='query_room_scene_req.room_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=65,
)


_QUERY_ROOM_SCENE_RSP = _descriptor.Descriptor(
  name='query_room_scene_rsp',
  full_name='query_room_scene_rsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ret', full_name='query_room_scene_rsp.ret', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='room_id', full_name='query_room_scene_rsp.room_id', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scene_name', full_name='query_room_scene_rsp.scene_name', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=67,
  serialized_end=139,
)

DESCRIPTOR.message_types_by_name['query_room_scene_req'] = _QUERY_ROOM_SCENE_REQ
DESCRIPTOR.message_types_by_name['query_room_scene_rsp'] = _QUERY_ROOM_SCENE_RSP

query_room_scene_req = _reflection.GeneratedProtocolMessageType('query_room_scene_req', (_message.Message,), dict(
  DESCRIPTOR = _QUERY_ROOM_SCENE_REQ,
  __module__ = 'query_room_scene_pb2'
  # @@protoc_insertion_point(class_scope:query_room_scene_req)
  ))
_sym_db.RegisterMessage(query_room_scene_req)

query_room_scene_rsp = _reflection.GeneratedProtocolMessageType('query_room_scene_rsp', (_message.Message,), dict(
  DESCRIPTOR = _QUERY_ROOM_SCENE_RSP,
  __module__ = 'query_room_scene_pb2'
  # @@protoc_insertion_point(class_scope:query_room_scene_rsp)
  ))
_sym_db.RegisterMessage(query_room_scene_rsp)


# @@protoc_insertion_point(module_scope)
