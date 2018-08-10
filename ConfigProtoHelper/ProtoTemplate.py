# _*_coding:utf-8_*_


PROTO_TEMPLATE = """
syntax = "proto3";
option csharp_namespace = "Config";
%(enums)s

%(messages)s
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