# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/sensores.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x14proto/sensores.proto"t\n\x06Sensor\x12\x0c\n\x04tipo\x18\x01 \x02(\t\x12\n\n\x02id\x18\x02 \x02(\t\x12\x13\n\x0btemperatura\x18\x03 \x01(\x02\x12\x1b\n\x13temperatura_freezer\x18\x04 \x01(\x02\x12\x10\n\x08presenca\x18\x05 \x01(\x08\x12\x0c\n\x04nome\x18\x06 \x01(\t"(\n\x0bSensor_List\x12\x19\n\x08sensores\x18\x01 \x03(\x0b\x32\x07.Sensor"\'\n\x0b\x44\x65vice_List\x12\x18\n\x07\x64\x65vices\x18\x01 \x03(\x0b\x32\x07.Device"r\n\x06\x44\x65vice\x12\x0c\n\x04tipo\x18\x01 \x02(\t\x12\n\n\x02id\x18\x02 \x02(\t\x12\x13\n\x0btemperatura\x18\x03 \x01(\x02\x12\x1b\n\x13temperatura_freezer\x18\x04 \x01(\x02\x12\x0e\n\x06ligado\x18\x05 \x01(\x08\x12\x0c\n\x04nome\x18\x06 \x01(\t"x\n\x05Input\x12\x0c\n\x04tipo\x18\x01 \x02(\t\x12\x14\n\x0ctipo_request\x18\x02 \x01(\t\x12\x0f\n\x07\x64\x65st_id\x18\x03 \x01(\t\x12\x15\n\rtipo_desejado\x18\x04 \x01(\t\x12\x0e\n\x06ligado\x18\x05 \x01(\x08\x12\x13\n\x0btemperatura\x18\x06 \x01(\x02\x32P\n\x0bRouteDevice\x12\x1e\n\tGetDevice\x12\x06.Input\x1a\x07.Device"\x00\x12!\n\x0cUpdateDevice\x12\x06.Input\x1a\x07.Device"\x00'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "proto.sensores_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _SENSOR._serialized_start = 24
    _SENSOR._serialized_end = 140
    _SENSOR_LIST._serialized_start = 142
    _SENSOR_LIST._serialized_end = 182
    _DEVICE_LIST._serialized_start = 184
    _DEVICE_LIST._serialized_end = 223
    _DEVICE._serialized_start = 225
    _DEVICE._serialized_end = 339
    _INPUT._serialized_start = 341
    _INPUT._serialized_end = 461
    _ROUTEDEVICE._serialized_start = 463
    _ROUTEDEVICE._serialized_end = 543
# @@protoc_insertion_point(module_scope)