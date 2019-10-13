# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Temp/Config.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Temp/Config.proto',
  package='',
  syntax='proto3',
  serialized_options=_b('\252\002\006Config'),
  serialized_pb=_b('\n\x11Temp/Config.proto\"/\n\x05Skill\x12\n\n\x02ID\x18\x01 \x01(\x05\x12\x0c\n\x04Name\x18\x02 \x01(\t\x12\x0c\n\x04\x43ost\x18\x03 \x01(\x05\"\x1d\n\rStringArray2D\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\t\"\xc3\x01\n\x03\x42ox\x12\n\n\x02ID\x18\x01 \x01(\x05\x12\x0e\n\x06Prefab\x18\x02 \x01(\t\x12\x16\n\x04Type\x18\x03 \x01(\x0e\x32\x08.BoxType\x12\x0c\n\x04Lose\x18\x04 \x03(\x05\x12&\n\tLoseCount\x18\x05 \x03(\x0b\x32\x13.Box.LoseCountEntry\x12 \n\x0bSpecialTest\x18\x06 \x01(\x0b\x32\x0b.IntArray2D\x1a\x30\n\x0eLoseCountEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"8\n\x06Studen\x12\n\n\x02ID\x18\x01 \x01(\x05\x12\x15\n\x05Skill\x18\x02 \x03(\x0b\x32\x06.Skill\x12\x0b\n\x03\x41ge\x18\x03 \x03(\x05\"\x1c\n\x0c\x46loatArray2D\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\x02\"\x1b\n\x0b\x42oolArray2D\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\x08\"\x1a\n\nIntArray2D\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\x05\"\x1b\n\x0bLongArray2D\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\x03*i\n\x07\x42oxType\x12\x10\n\x0c\x42oxType_NONE\x10\x00\x12\x12\n\x0e\x42oxType_NORMAL\x10\x01\x12\x11\n\rBoxType_METAL\x10\x02\x12\x13\n\x0f\x42oxType_ELEMENT\x10\x03\x12\x10\n\x0c\x42oxType_BOOM\x10\x04\x42\t\xaa\x02\x06\x43onfigb\x06proto3')
)

_BOXTYPE = _descriptor.EnumDescriptor(
  name='BoxType',
  full_name='BoxType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BoxType_NONE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BoxType_NORMAL', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BoxType_METAL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BoxType_ELEMENT', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BoxType_BOOM', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=473,
  serialized_end=578,
)
_sym_db.RegisterEnumDescriptor(_BOXTYPE)

BoxType = enum_type_wrapper.EnumTypeWrapper(_BOXTYPE)
BoxType_NONE = 0
BoxType_NORMAL = 1
BoxType_METAL = 2
BoxType_ELEMENT = 3
BoxType_BOOM = 4



_SKILL = _descriptor.Descriptor(
  name='Skill',
  full_name='Skill',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='Skill.ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Name', full_name='Skill.Name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Cost', full_name='Skill.Cost', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=68,
)


_STRINGARRAY2D = _descriptor.Descriptor(
  name='StringArray2D',
  full_name='StringArray2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='StringArray2D.Data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=99,
)


_BOX_LOSECOUNTENTRY = _descriptor.Descriptor(
  name='LoseCountEntry',
  full_name='Box.LoseCountEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Box.LoseCountEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='Box.LoseCountEntry.value', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=249,
  serialized_end=297,
)

_BOX = _descriptor.Descriptor(
  name='Box',
  full_name='Box',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='Box.ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Prefab', full_name='Box.Prefab', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Type', full_name='Box.Type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Lose', full_name='Box.Lose', index=3,
      number=4, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='LoseCount', full_name='Box.LoseCount', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='SpecialTest', full_name='Box.SpecialTest', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BOX_LOSECOUNTENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=297,
)


_STUDEN = _descriptor.Descriptor(
  name='Studen',
  full_name='Studen',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='Studen.ID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Skill', full_name='Studen.Skill', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='Age', full_name='Studen.Age', index=2,
      number=3, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=299,
  serialized_end=355,
)


_FLOATARRAY2D = _descriptor.Descriptor(
  name='FloatArray2D',
  full_name='FloatArray2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='FloatArray2D.Data', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=357,
  serialized_end=385,
)


_BOOLARRAY2D = _descriptor.Descriptor(
  name='BoolArray2D',
  full_name='BoolArray2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='BoolArray2D.Data', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=387,
  serialized_end=414,
)


_INTARRAY2D = _descriptor.Descriptor(
  name='IntArray2D',
  full_name='IntArray2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='IntArray2D.Data', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=416,
  serialized_end=442,
)


_LONGARRAY2D = _descriptor.Descriptor(
  name='LongArray2D',
  full_name='LongArray2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Data', full_name='LongArray2D.Data', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=444,
  serialized_end=471,
)

_BOX_LOSECOUNTENTRY.containing_type = _BOX
_BOX.fields_by_name['Type'].enum_type = _BOXTYPE
_BOX.fields_by_name['LoseCount'].message_type = _BOX_LOSECOUNTENTRY
_BOX.fields_by_name['SpecialTest'].message_type = _INTARRAY2D
_STUDEN.fields_by_name['Skill'].message_type = _SKILL
DESCRIPTOR.message_types_by_name['Skill'] = _SKILL
DESCRIPTOR.message_types_by_name['StringArray2D'] = _STRINGARRAY2D
DESCRIPTOR.message_types_by_name['Box'] = _BOX
DESCRIPTOR.message_types_by_name['Studen'] = _STUDEN
DESCRIPTOR.message_types_by_name['FloatArray2D'] = _FLOATARRAY2D
DESCRIPTOR.message_types_by_name['BoolArray2D'] = _BOOLARRAY2D
DESCRIPTOR.message_types_by_name['IntArray2D'] = _INTARRAY2D
DESCRIPTOR.message_types_by_name['LongArray2D'] = _LONGARRAY2D
DESCRIPTOR.enum_types_by_name['BoxType'] = _BOXTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Skill = _reflection.GeneratedProtocolMessageType('Skill', (_message.Message,), {
  'DESCRIPTOR' : _SKILL,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:Skill)
  })
_sym_db.RegisterMessage(Skill)

StringArray2D = _reflection.GeneratedProtocolMessageType('StringArray2D', (_message.Message,), {
  'DESCRIPTOR' : _STRINGARRAY2D,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:StringArray2D)
  })
_sym_db.RegisterMessage(StringArray2D)

Box = _reflection.GeneratedProtocolMessageType('Box', (_message.Message,), {

  'LoseCountEntry' : _reflection.GeneratedProtocolMessageType('LoseCountEntry', (_message.Message,), {
    'DESCRIPTOR' : _BOX_LOSECOUNTENTRY,
    '__module__' : 'Temp.Config_pb2'
    # @@protoc_insertion_point(class_scope:Box.LoseCountEntry)
    })
  ,
  'DESCRIPTOR' : _BOX,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:Box)
  })
_sym_db.RegisterMessage(Box)
_sym_db.RegisterMessage(Box.LoseCountEntry)

Studen = _reflection.GeneratedProtocolMessageType('Studen', (_message.Message,), {
  'DESCRIPTOR' : _STUDEN,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:Studen)
  })
_sym_db.RegisterMessage(Studen)

FloatArray2D = _reflection.GeneratedProtocolMessageType('FloatArray2D', (_message.Message,), {
  'DESCRIPTOR' : _FLOATARRAY2D,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:FloatArray2D)
  })
_sym_db.RegisterMessage(FloatArray2D)

BoolArray2D = _reflection.GeneratedProtocolMessageType('BoolArray2D', (_message.Message,), {
  'DESCRIPTOR' : _BOOLARRAY2D,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:BoolArray2D)
  })
_sym_db.RegisterMessage(BoolArray2D)

IntArray2D = _reflection.GeneratedProtocolMessageType('IntArray2D', (_message.Message,), {
  'DESCRIPTOR' : _INTARRAY2D,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:IntArray2D)
  })
_sym_db.RegisterMessage(IntArray2D)

LongArray2D = _reflection.GeneratedProtocolMessageType('LongArray2D', (_message.Message,), {
  'DESCRIPTOR' : _LONGARRAY2D,
  '__module__' : 'Temp.Config_pb2'
  # @@protoc_insertion_point(class_scope:LongArray2D)
  })
_sym_db.RegisterMessage(LongArray2D)


DESCRIPTOR._options = None
_BOX_LOSECOUNTENTRY._options = None
# @@protoc_insertion_point(module_scope)
