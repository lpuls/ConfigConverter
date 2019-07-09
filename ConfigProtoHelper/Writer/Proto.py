# _*_coding:utf-8_*_

from ConfigBase.CommonIntermediateFormat import CommonIntermediateFormat as CIFormat


# _*_coding:utf-8_*_


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


def write(format_data, dest_path):
    prefix = format_data[:2]
    if 'e_' == prefix:
        return

