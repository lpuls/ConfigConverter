# _*_coding:utf-8_*_


DEFAULT_KEY = "ID"
DEFAULT_STRING_KEY = "KEY"

PROTO_TEMPLATE = """
syntax = "proto3";
option csharp_namespace = "Config";
%(enums)s
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