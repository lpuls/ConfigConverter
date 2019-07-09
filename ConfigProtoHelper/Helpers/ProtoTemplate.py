# _*_coding:utf-8_*_


PROTO_TEMPLATE = """
syntax = "proto3";
option csharp_namespace = "Config";
%(enums)s

message IntArray
{
    repeated int32 data = 1;
}

message LongArray
{
    repeated int32 data = 1;
}

message FloatArray
{
    repeated float data = 1;
}

message StringArray
{
    repeated string data = 1;
}

message BoolArray
{
    repeated bool data = 1;
}

%(messages)s

message DataHelper 
{
    repeated string messageType = 1;
%(message_list)s
}
"""

MESSAGE_TEMPLATE = """
message %(message_name)s
{
%(message_fields)s
}
"""

ENUM_TEMPLATE = """
enum %(enum_name)s {
%(enum_fields)s
}
"""