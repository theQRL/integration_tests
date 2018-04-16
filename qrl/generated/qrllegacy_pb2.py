# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qrllegacy.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import qrl.generated.qrl_pb2 as qrl__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='qrllegacy.proto',
  package='qrl',
  syntax='proto3',
  serialized_pb=_b('\n\x0fqrllegacy.proto\x12\x03qrl\x1a\tqrl.proto\"\xee\x07\n\rLegacyMessage\x12.\n\tfunc_name\x18\x01 \x01(\x0e\x32\x1b.qrl.LegacyMessage.FuncName\x12\x1d\n\x06noData\x18\x02 \x01(\x0b\x32\x0b.qrl.NoDataH\x00\x12\x1d\n\x06veData\x18\x03 \x01(\x0b\x32\x0b.qrl.VEDataH\x00\x12\x1d\n\x06plData\x18\x04 \x01(\x0b\x32\x0b.qrl.PLDataH\x00\x12!\n\x08pongData\x18\x05 \x01(\x0b\x32\r.qrl.PONGDataH\x00\x12\x1d\n\x06mrData\x18\x06 \x01(\x0b\x32\x0b.qrl.MRDataH\x00\x12\x1b\n\x05\x62lock\x18\x07 \x01(\x0b\x32\n.qrl.BlockH\x00\x12\x1d\n\x06\x66\x62\x44\x61ta\x18\x08 \x01(\x0b\x32\x0b.qrl.FBDataH\x00\x12\x1d\n\x06pbData\x18\t \x01(\x0b\x32\x0b.qrl.PBDataH\x00\x12&\n\x06\x62hData\x18\n \x01(\x0b\x32\x14.qrl.BlockHeightDataH\x00\x12\"\n\x06txData\x18\x0b \x01(\x0b\x32\x10.qrl.TransactionH\x00\x12\"\n\x06mtData\x18\x0c \x01(\x0b\x32\x10.qrl.TransactionH\x00\x12\"\n\x06tkData\x18\r \x01(\x0b\x32\x10.qrl.TransactionH\x00\x12\"\n\x06ttData\x18\x0e \x01(\x0b\x32\x10.qrl.TransactionH\x00\x12\"\n\x06ltData\x18\x0f \x01(\x0b\x32\x10.qrl.TransactionH\x00\x12\"\n\x06slData\x18\x10 \x01(\x0b\x32\x10.qrl.TransactionH\x00\x12\x31\n\x07\x65phData\x18\x11 \x01(\x0b\x32\x1e.qrl.EncryptedEphemeralMessageH\x00\x12!\n\x08syncData\x18\x12 \x01(\x0b\x32\r.qrl.SYNCDataH\x00\x12-\n\x0e\x63hainStateData\x18\x13 \x01(\x0b\x32\x13.qrl.NodeChainStateH\x00\x12-\n\x0enodeHeaderHash\x18\x14 \x01(\x0b\x32\x13.qrl.NodeHeaderHashH\x00\x12-\n\np2pAckData\x18\x15 \x01(\x0b\x32\x17.qrl.P2PAcknowledgementH\x00\"\xc7\x01\n\x08\x46uncName\x12\x06\n\x02VE\x10\x00\x12\x06\n\x02PL\x10\x01\x12\x08\n\x04PONG\x10\x02\x12\x06\n\x02MR\x10\x03\x12\x07\n\x03SFM\x10\x04\x12\x06\n\x02\x42K\x10\x05\x12\x06\n\x02\x46\x42\x10\x06\x12\x06\n\x02PB\x10\x07\x12\x06\n\x02\x42H\x10\x08\x12\x06\n\x02TX\x10\t\x12\x06\n\x02LT\x10\n\x12\x07\n\x03\x45PH\x10\x0b\x12\x06\n\x02MT\x10\x0c\x12\x06\n\x02TK\x10\r\x12\x06\n\x02TT\x10\x0e\x12\x06\n\x02SL\x10\x0f\x12\x08\n\x04SYNC\x10\x10\x12\x0e\n\nCHAINSTATE\x10\x11\x12\x10\n\x0cHEADERHASHES\x10\x12\x12\x0b\n\x07P2P_ACK\x10\x13\x42\x06\n\x04\x64\x61ta\"\x08\n\x06NoData\"H\n\x06VEData\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x19\n\x11genesis_prev_hash\x18\x02 \x01(\x0c\x12\x12\n\nrate_limit\x18\x03 \x01(\x04\"/\n\x06PLData\x12\x10\n\x08peer_ips\x18\x01 \x03(\t\x12\x13\n\x0bpublic_port\x18\x02 \x01(\r\"\n\n\x08PONGData\"\x9d\x01\n\x06MRData\x12\x0c\n\x04hash\x18\x01 \x01(\x0c\x12)\n\x04type\x18\x02 \x01(\x0e\x32\x1b.qrl.LegacyMessage.FuncName\x12\x16\n\x0estake_selector\x18\x03 \x01(\x0c\x12\x14\n\x0c\x62lock_number\x18\x04 \x01(\x04\x12\x17\n\x0fprev_headerhash\x18\x05 \x01(\x0c\x12\x13\n\x0breveal_hash\x18\x06 \x01(\x0c\"@\n\x06\x42KData\x12\x1b\n\x06mrData\x18\x01 \x01(\x0b\x32\x0b.qrl.MRData\x12\x19\n\x05\x62lock\x18\x02 \x01(\x0b\x32\n.qrl.Block\"\x17\n\x06\x46\x42\x44\x61ta\x12\r\n\x05index\x18\x01 \x01(\x04\"#\n\x06PBData\x12\x19\n\x05\x62lock\x18\x01 \x01(\x0b\x32\n.qrl.Block\"\x19\n\x08SYNCData\x12\r\n\x05state\x18\x01 \x01(\tb\x06proto3')
  ,
  dependencies=[qrl__pb2.DESCRIPTOR,])



_LEGACYMESSAGE_FUNCNAME = _descriptor.EnumDescriptor(
  name='FuncName',
  full_name='qrl.LegacyMessage.FuncName',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PL', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PONG', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MR', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SFM', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BK', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FB', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PB', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BH', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TX', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LT', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EPH', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MT', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TK', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TT', index=14, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SL', index=15, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SYNC', index=16, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHAINSTATE', index=17, number=17,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HEADERHASHES', index=18, number=18,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='P2P_ACK', index=19, number=19,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=835,
  serialized_end=1034,
)
_sym_db.RegisterEnumDescriptor(_LEGACYMESSAGE_FUNCNAME)


_LEGACYMESSAGE = _descriptor.Descriptor(
  name='LegacyMessage',
  full_name='qrl.LegacyMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='func_name', full_name='qrl.LegacyMessage.func_name', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='noData', full_name='qrl.LegacyMessage.noData', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='veData', full_name='qrl.LegacyMessage.veData', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='plData', full_name='qrl.LegacyMessage.plData', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pongData', full_name='qrl.LegacyMessage.pongData', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mrData', full_name='qrl.LegacyMessage.mrData', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='block', full_name='qrl.LegacyMessage.block', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fbData', full_name='qrl.LegacyMessage.fbData', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pbData', full_name='qrl.LegacyMessage.pbData', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bhData', full_name='qrl.LegacyMessage.bhData', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='txData', full_name='qrl.LegacyMessage.txData', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mtData', full_name='qrl.LegacyMessage.mtData', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tkData', full_name='qrl.LegacyMessage.tkData', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ttData', full_name='qrl.LegacyMessage.ttData', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ltData', full_name='qrl.LegacyMessage.ltData', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slData', full_name='qrl.LegacyMessage.slData', index=15,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ephData', full_name='qrl.LegacyMessage.ephData', index=16,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='syncData', full_name='qrl.LegacyMessage.syncData', index=17,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chainStateData', full_name='qrl.LegacyMessage.chainStateData', index=18,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nodeHeaderHash', full_name='qrl.LegacyMessage.nodeHeaderHash', index=19,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='p2pAckData', full_name='qrl.LegacyMessage.p2pAckData', index=20,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LEGACYMESSAGE_FUNCNAME,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='qrl.LegacyMessage.data',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=36,
  serialized_end=1042,
)


_NODATA = _descriptor.Descriptor(
  name='NoData',
  full_name='qrl.NoData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=1044,
  serialized_end=1052,
)


_VEDATA = _descriptor.Descriptor(
  name='VEData',
  full_name='qrl.VEData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='qrl.VEData.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='genesis_prev_hash', full_name='qrl.VEData.genesis_prev_hash', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rate_limit', full_name='qrl.VEData.rate_limit', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=1054,
  serialized_end=1126,
)


_PLDATA = _descriptor.Descriptor(
  name='PLData',
  full_name='qrl.PLData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='peer_ips', full_name='qrl.PLData.peer_ips', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='public_port', full_name='qrl.PLData.public_port', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=1128,
  serialized_end=1175,
)


_PONGDATA = _descriptor.Descriptor(
  name='PONGData',
  full_name='qrl.PONGData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
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
  serialized_start=1177,
  serialized_end=1187,
)


_MRDATA = _descriptor.Descriptor(
  name='MRData',
  full_name='qrl.MRData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hash', full_name='qrl.MRData.hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='qrl.MRData.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stake_selector', full_name='qrl.MRData.stake_selector', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='block_number', full_name='qrl.MRData.block_number', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='prev_headerhash', full_name='qrl.MRData.prev_headerhash', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reveal_hash', full_name='qrl.MRData.reveal_hash', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=1190,
  serialized_end=1347,
)


_BKDATA = _descriptor.Descriptor(
  name='BKData',
  full_name='qrl.BKData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mrData', full_name='qrl.BKData.mrData', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='block', full_name='qrl.BKData.block', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=1349,
  serialized_end=1413,
)


_FBDATA = _descriptor.Descriptor(
  name='FBData',
  full_name='qrl.FBData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='qrl.FBData.index', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=1415,
  serialized_end=1438,
)


_PBDATA = _descriptor.Descriptor(
  name='PBData',
  full_name='qrl.PBData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='block', full_name='qrl.PBData.block', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=1440,
  serialized_end=1475,
)


_SYNCDATA = _descriptor.Descriptor(
  name='SYNCData',
  full_name='qrl.SYNCData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='qrl.SYNCData.state', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=1477,
  serialized_end=1502,
)

_LEGACYMESSAGE.fields_by_name['func_name'].enum_type = _LEGACYMESSAGE_FUNCNAME
_LEGACYMESSAGE.fields_by_name['noData'].message_type = _NODATA
_LEGACYMESSAGE.fields_by_name['veData'].message_type = _VEDATA
_LEGACYMESSAGE.fields_by_name['plData'].message_type = _PLDATA
_LEGACYMESSAGE.fields_by_name['pongData'].message_type = _PONGDATA
_LEGACYMESSAGE.fields_by_name['mrData'].message_type = _MRDATA
_LEGACYMESSAGE.fields_by_name['block'].message_type = qrl__pb2._BLOCK
_LEGACYMESSAGE.fields_by_name['fbData'].message_type = _FBDATA
_LEGACYMESSAGE.fields_by_name['pbData'].message_type = _PBDATA
_LEGACYMESSAGE.fields_by_name['bhData'].message_type = qrl__pb2._BLOCKHEIGHTDATA
_LEGACYMESSAGE.fields_by_name['txData'].message_type = qrl__pb2._TRANSACTION
_LEGACYMESSAGE.fields_by_name['mtData'].message_type = qrl__pb2._TRANSACTION
_LEGACYMESSAGE.fields_by_name['tkData'].message_type = qrl__pb2._TRANSACTION
_LEGACYMESSAGE.fields_by_name['ttData'].message_type = qrl__pb2._TRANSACTION
_LEGACYMESSAGE.fields_by_name['ltData'].message_type = qrl__pb2._TRANSACTION
_LEGACYMESSAGE.fields_by_name['slData'].message_type = qrl__pb2._TRANSACTION
_LEGACYMESSAGE.fields_by_name['ephData'].message_type = qrl__pb2._ENCRYPTEDEPHEMERALMESSAGE
_LEGACYMESSAGE.fields_by_name['syncData'].message_type = _SYNCDATA
_LEGACYMESSAGE.fields_by_name['chainStateData'].message_type = qrl__pb2._NODECHAINSTATE
_LEGACYMESSAGE.fields_by_name['nodeHeaderHash'].message_type = qrl__pb2._NODEHEADERHASH
_LEGACYMESSAGE.fields_by_name['p2pAckData'].message_type = qrl__pb2._P2PACKNOWLEDGEMENT
_LEGACYMESSAGE_FUNCNAME.containing_type = _LEGACYMESSAGE
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['noData'])
_LEGACYMESSAGE.fields_by_name['noData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['veData'])
_LEGACYMESSAGE.fields_by_name['veData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['plData'])
_LEGACYMESSAGE.fields_by_name['plData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['pongData'])
_LEGACYMESSAGE.fields_by_name['pongData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['mrData'])
_LEGACYMESSAGE.fields_by_name['mrData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['block'])
_LEGACYMESSAGE.fields_by_name['block'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['fbData'])
_LEGACYMESSAGE.fields_by_name['fbData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['pbData'])
_LEGACYMESSAGE.fields_by_name['pbData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['bhData'])
_LEGACYMESSAGE.fields_by_name['bhData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['txData'])
_LEGACYMESSAGE.fields_by_name['txData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['mtData'])
_LEGACYMESSAGE.fields_by_name['mtData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['tkData'])
_LEGACYMESSAGE.fields_by_name['tkData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['ttData'])
_LEGACYMESSAGE.fields_by_name['ttData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['ltData'])
_LEGACYMESSAGE.fields_by_name['ltData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['slData'])
_LEGACYMESSAGE.fields_by_name['slData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['ephData'])
_LEGACYMESSAGE.fields_by_name['ephData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['syncData'])
_LEGACYMESSAGE.fields_by_name['syncData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['chainStateData'])
_LEGACYMESSAGE.fields_by_name['chainStateData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['nodeHeaderHash'])
_LEGACYMESSAGE.fields_by_name['nodeHeaderHash'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_LEGACYMESSAGE.oneofs_by_name['data'].fields.append(
  _LEGACYMESSAGE.fields_by_name['p2pAckData'])
_LEGACYMESSAGE.fields_by_name['p2pAckData'].containing_oneof = _LEGACYMESSAGE.oneofs_by_name['data']
_MRDATA.fields_by_name['type'].enum_type = _LEGACYMESSAGE_FUNCNAME
_BKDATA.fields_by_name['mrData'].message_type = _MRDATA
_BKDATA.fields_by_name['block'].message_type = qrl__pb2._BLOCK
_PBDATA.fields_by_name['block'].message_type = qrl__pb2._BLOCK
DESCRIPTOR.message_types_by_name['LegacyMessage'] = _LEGACYMESSAGE
DESCRIPTOR.message_types_by_name['NoData'] = _NODATA
DESCRIPTOR.message_types_by_name['VEData'] = _VEDATA
DESCRIPTOR.message_types_by_name['PLData'] = _PLDATA
DESCRIPTOR.message_types_by_name['PONGData'] = _PONGDATA
DESCRIPTOR.message_types_by_name['MRData'] = _MRDATA
DESCRIPTOR.message_types_by_name['BKData'] = _BKDATA
DESCRIPTOR.message_types_by_name['FBData'] = _FBDATA
DESCRIPTOR.message_types_by_name['PBData'] = _PBDATA
DESCRIPTOR.message_types_by_name['SYNCData'] = _SYNCDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LegacyMessage = _reflection.GeneratedProtocolMessageType('LegacyMessage', (_message.Message,), dict(
  DESCRIPTOR = _LEGACYMESSAGE,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.LegacyMessage)
  ))
_sym_db.RegisterMessage(LegacyMessage)

NoData = _reflection.GeneratedProtocolMessageType('NoData', (_message.Message,), dict(
  DESCRIPTOR = _NODATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.NoData)
  ))
_sym_db.RegisterMessage(NoData)

VEData = _reflection.GeneratedProtocolMessageType('VEData', (_message.Message,), dict(
  DESCRIPTOR = _VEDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.VEData)
  ))
_sym_db.RegisterMessage(VEData)

PLData = _reflection.GeneratedProtocolMessageType('PLData', (_message.Message,), dict(
  DESCRIPTOR = _PLDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.PLData)
  ))
_sym_db.RegisterMessage(PLData)

PONGData = _reflection.GeneratedProtocolMessageType('PONGData', (_message.Message,), dict(
  DESCRIPTOR = _PONGDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.PONGData)
  ))
_sym_db.RegisterMessage(PONGData)

MRData = _reflection.GeneratedProtocolMessageType('MRData', (_message.Message,), dict(
  DESCRIPTOR = _MRDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.MRData)
  ))
_sym_db.RegisterMessage(MRData)

BKData = _reflection.GeneratedProtocolMessageType('BKData', (_message.Message,), dict(
  DESCRIPTOR = _BKDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.BKData)
  ))
_sym_db.RegisterMessage(BKData)

FBData = _reflection.GeneratedProtocolMessageType('FBData', (_message.Message,), dict(
  DESCRIPTOR = _FBDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.FBData)
  ))
_sym_db.RegisterMessage(FBData)

PBData = _reflection.GeneratedProtocolMessageType('PBData', (_message.Message,), dict(
  DESCRIPTOR = _PBDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.PBData)
  ))
_sym_db.RegisterMessage(PBData)

SYNCData = _reflection.GeneratedProtocolMessageType('SYNCData', (_message.Message,), dict(
  DESCRIPTOR = _SYNCDATA,
  __module__ = 'qrllegacy_pb2'
  # @@protoc_insertion_point(class_scope:qrl.SYNCData)
  ))
_sym_db.RegisterMessage(SYNCData)


# @@protoc_insertion_point(module_scope)
