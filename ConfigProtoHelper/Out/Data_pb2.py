# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Out/Data.proto

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
  name='Out/Data.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0eOut/Data.proto\"f\n\x04Test\x12\x12\n\nARRAY_TEST\x18\x01 \x03(\x05\x12\x1d\n\x04TEST\x18\x02 \x03(\x0b\x32\x0f.Test.TESTEntry\x1a+\n\tTESTEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"&\n\nDataHelper\x12\x18\n\tTest_list\x18\x01 \x03(\x0b\x32\x05.TestB\t\xaa\x02\x06\x43onfigb\x06proto3')
)




_TEST_TESTENTRY = _descriptor.Descriptor(
  name='TESTEntry',
  full_name='Test.TESTEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Test.TESTEntry.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='Test.TESTEntry.value', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=120,
)

_TEST = _descriptor.Descriptor(
  name='Test',
  full_name='Test',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ARRAY_TEST', full_name='Test.ARRAY_TEST', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='TEST', full_name='Test.TEST', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TEST_TESTENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=120,
)


_DATAHELPER = _descriptor.Descriptor(
  name='DataHelper',
  full_name='DataHelper',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Test_list', full_name='DataHelper.Test_list', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=160,
)

_TEST_TESTENTRY.containing_type = _TEST
_TEST.fields_by_name['TEST'].message_type = _TEST_TESTENTRY
_DATAHELPER.fields_by_name['Test_list'].message_type = _TEST
DESCRIPTOR.message_types_by_name['Test'] = _TEST
DESCRIPTOR.message_types_by_name['DataHelper'] = _DATAHELPER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Test = _reflection.GeneratedProtocolMessageType('Test', (_message.Message,), dict(

  TESTEntry = _reflection.GeneratedProtocolMessageType('TESTEntry', (_message.Message,), dict(
    DESCRIPTOR = _TEST_TESTENTRY,
    __module__ = 'Out.Data_pb2'
    # @@protoc_insertion_point(class_scope:Test.TESTEntry)
    ))
  ,
  DESCRIPTOR = _TEST,
  __module__ = 'Out.Data_pb2'
  # @@protoc_insertion_point(class_scope:Test)
  ))
_sym_db.RegisterMessage(Test)
_sym_db.RegisterMessage(Test.TESTEntry)

DataHelper = _reflection.GeneratedProtocolMessageType('DataHelper', (_message.Message,), dict(
  DESCRIPTOR = _DATAHELPER,
  __module__ = 'Out.Data_pb2'
  # @@protoc_insertion_point(class_scope:DataHelper)
  ))
_sym_db.RegisterMessage(DataHelper)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\252\002\006Config'))
_TEST_TESTENTRY.has_options = True
_TEST_TESTENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
