# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common_info.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common_info.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x11\x63ommon_info.proto\"i\n\x11other_player_info\x12\x11\n\tplayer_id\x18\x01 \x02(\x04\x12\x13\n\x0bplayer_name\x18\x02 \x02(\x0c\x12\x13\n\x0bwechat_info\x18\x03 \x02(\x0c\x12\n\n\x02ip\x18\x04 \x02(\x0c\x12\x0b\n\x03pos\x18\x05 \x02(\r\"f\n\x08game_cfg\x12\x12\n\nmember_num\x18\x01 \x02(\r\x12\r\n\x05multi\x18\x02 \x02(\r\x12\x1c\n\x14total_start_game_num\x18\x03 \x02(\r\x12\x19\n\x03opt\x18\x04 \x02(\x0e\x32\x0c.room_option\"\xfa\x01\n\rsyn_game_info\x12\x0f\n\x07room_id\x18\x01 \x02(\r\x12\x16\n\x03\x63\x66g\x18\x02 \x02(\x0b\x32\t.game_cfg\x12\x14\n\x0c\x63ur_game_num\x18\x03 \x02(\r\x12\x11\n\tcur_round\x18\x04 \x02(\r\x12\x10\n\x08\x63ur_turn\x18\x05 \x02(\r\x12\x17\n\x0fremain_card_num\x18\x06 \x02(\r\x12\x11\n\tmaster_id\x18\x07 \x02(\r\x12\x16\n\x0elist_gold_card\x18\x08 \x03(\r\x12\x17\n\x0flist_owner_card\x18\t \x03(\r\x12(\n\x0clist_members\x18\n \x03(\x0b\x32\x12.other_player_info\"R\n\x0eon_touch_event\x12\x1c\n\x07\x65v_type\x18\x01 \x02(\x0e\x32\x0b.event_type\x12\x11\n\tev_target\x18\x02 \x02(\x04\x12\x0f\n\x07\x65v_data\x18\x03 \x02(\x0c\"e\n\x15on_touch_event_member\x12#\n\x07\x65v_type\x18\x01 \x02(\x0e\x32\x12.event_type_member\x12\'\n\x0blist_member\x18\x02 \x03(\x0b\x32\x12.other_player_info\"G\n\x0b\x63\x61rd_serial\x12\x11\n\tplayer_id\x18\x01 \x02(\x04\x12\x16\n\x0elist_card_info\x18\x02 \x03(\r\x12\r\n\x05score\x18\x03 \x02(\r\"o\n\x0csyn_game_ret\x12\x0f\n\x07room_id\x18\x01 \x02(\r\x12\'\n\x0blist_member\x18\x02 \x03(\x0b\x32\x12.other_player_info\x12%\n\x0flist_car_serial\x18\x03 \x03(\x0b\x32\x0c.card_serial*!\n\x0broom_option\x12\x08\n\x04half\x10\x01\x12\x08\n\x04\x66ull\x10\x02*<\n\x11\x65vent_type_member\x12\x13\n\x0f\x65v_member_enter\x10\x01\x12\x12\n\x0e\x65v_member_exit\x10\x02*\xf5\x03\n\nevent_type\x12\x15\n\x11\x65v_gang_with_peng\x10\x01\x12\x11\n\rev_gang_other\x10\x02\x12\x0f\n\x0b\x65v_gang_all\x10\x03\x12\x0b\n\x07\x65v_peng\x10\x0b\x12\n\n\x06\x65v_chi\x10\x0c\x12\r\n\tev_bu_hua\x10\r\x12\x0e\n\nev_kai_jin\x10\x0e\x12\r\n\tev_mo_pai\x10\x0f\x12\r\n\tev_qi_pai\x10\x10\x12\x0e\n\nev_dan_you\x10\x15\x12\x11\n\rev_shuang_you\x10\x16\x12\x0e\n\nev_san_you\x10\x17\x12\x11\n\rev_fen_bing_1\x10\x18\x12\x11\n\rev_fen_bing_2\x10\x19\x12\x10\n\x0c\x65v_hu_normal\x10Q\x12\x11\n\rev_hu_cha_hua\x10R\x12\x14\n\x10\x65v_hu_qiang_gang\x10S\x12\x13\n\x0f\x65v_hu_qiang_jin\x10T\x12\x15\n\x11\x65v_hu_san_jin_dao\x10U\x12\x14\n\x10\x65v_hu_si_jin_dao\x10V\x12\x14\n\x10\x65v_hu_wu_jin_dao\x10W\x12\x19\n\x15\x65v_hu_ba_xian_guo_hai\x10X\x12\x15\n\x11\x65v_hu_shi_san_yao\x10Y\x12\x13\n\x0f\x65v_hu_qi_dui_zi\x10Z\x12\x10\n\x0b\x65v_syn_card\x10\x95\x01\x12\x11\n\x0c\x65v_syn_order\x10\x96\x01')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_ROOM_OPTION = _descriptor.EnumDescriptor(
  name='room_option',
  full_name='room_option',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='half', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='full', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=858,
  serialized_end=891,
)
_sym_db.RegisterEnumDescriptor(_ROOM_OPTION)

room_option = enum_type_wrapper.EnumTypeWrapper(_ROOM_OPTION)
_EVENT_TYPE_MEMBER = _descriptor.EnumDescriptor(
  name='event_type_member',
  full_name='event_type_member',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ev_member_enter', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_member_exit', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=893,
  serialized_end=953,
)
_sym_db.RegisterEnumDescriptor(_EVENT_TYPE_MEMBER)

event_type_member = enum_type_wrapper.EnumTypeWrapper(_EVENT_TYPE_MEMBER)
_EVENT_TYPE = _descriptor.EnumDescriptor(
  name='event_type',
  full_name='event_type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ev_gang_with_peng', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_gang_other', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_gang_all', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_peng', index=3, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_chi', index=4, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_bu_hua', index=5, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_kai_jin', index=6, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_mo_pai', index=7, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_qi_pai', index=8, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_dan_you', index=9, number=21,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_shuang_you', index=10, number=22,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_san_you', index=11, number=23,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_fen_bing_1', index=12, number=24,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_fen_bing_2', index=13, number=25,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_normal', index=14, number=81,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_cha_hua', index=15, number=82,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_qiang_gang', index=16, number=83,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_qiang_jin', index=17, number=84,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_san_jin_dao', index=18, number=85,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_si_jin_dao', index=19, number=86,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_wu_jin_dao', index=20, number=87,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_ba_xian_guo_hai', index=21, number=88,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_shi_san_yao', index=22, number=89,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_hu_qi_dui_zi', index=23, number=90,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_syn_card', index=24, number=149,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ev_syn_order', index=25, number=150,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=956,
  serialized_end=1457,
)
_sym_db.RegisterEnumDescriptor(_EVENT_TYPE)

event_type = enum_type_wrapper.EnumTypeWrapper(_EVENT_TYPE)
half = 1
full = 2
ev_member_enter = 1
ev_member_exit = 2
ev_gang_with_peng = 1
ev_gang_other = 2
ev_gang_all = 3
ev_peng = 11
ev_chi = 12
ev_bu_hua = 13
ev_kai_jin = 14
ev_mo_pai = 15
ev_qi_pai = 16
ev_dan_you = 21
ev_shuang_you = 22
ev_san_you = 23
ev_fen_bing_1 = 24
ev_fen_bing_2 = 25
ev_hu_normal = 81
ev_hu_cha_hua = 82
ev_hu_qiang_gang = 83
ev_hu_qiang_jin = 84
ev_hu_san_jin_dao = 85
ev_hu_si_jin_dao = 86
ev_hu_wu_jin_dao = 87
ev_hu_ba_xian_guo_hai = 88
ev_hu_shi_san_yao = 89
ev_hu_qi_dui_zi = 90
ev_syn_card = 149
ev_syn_order = 150



_OTHER_PLAYER_INFO = _descriptor.Descriptor(
  name='other_player_info',
  full_name='other_player_info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='other_player_info.player_id', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player_name', full_name='other_player_info.player_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='wechat_info', full_name='other_player_info.wechat_info', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='other_player_info.ip', index=3,
      number=4, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pos', full_name='other_player_info.pos', index=4,
      number=5, type=13, cpp_type=3, label=2,
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
  serialized_start=21,
  serialized_end=126,
)


_GAME_CFG = _descriptor.Descriptor(
  name='game_cfg',
  full_name='game_cfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='member_num', full_name='game_cfg.member_num', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='multi', full_name='game_cfg.multi', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='total_start_game_num', full_name='game_cfg.total_start_game_num', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opt', full_name='game_cfg.opt', index=3,
      number=4, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
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
  serialized_start=128,
  serialized_end=230,
)


_SYN_GAME_INFO = _descriptor.Descriptor(
  name='syn_game_info',
  full_name='syn_game_info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_id', full_name='syn_game_info.room_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cfg', full_name='syn_game_info.cfg', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cur_game_num', full_name='syn_game_info.cur_game_num', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cur_round', full_name='syn_game_info.cur_round', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cur_turn', full_name='syn_game_info.cur_turn', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='remain_card_num', full_name='syn_game_info.remain_card_num', index=5,
      number=6, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='master_id', full_name='syn_game_info.master_id', index=6,
      number=7, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_gold_card', full_name='syn_game_info.list_gold_card', index=7,
      number=8, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_owner_card', full_name='syn_game_info.list_owner_card', index=8,
      number=9, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_members', full_name='syn_game_info.list_members', index=9,
      number=10, type=11, cpp_type=10, label=3,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=233,
  serialized_end=483,
)


_ON_TOUCH_EVENT = _descriptor.Descriptor(
  name='on_touch_event',
  full_name='on_touch_event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ev_type', full_name='on_touch_event.ev_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ev_target', full_name='on_touch_event.ev_target', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ev_data', full_name='on_touch_event.ev_data', index=2,
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
  serialized_start=485,
  serialized_end=567,
)


_ON_TOUCH_EVENT_MEMBER = _descriptor.Descriptor(
  name='on_touch_event_member',
  full_name='on_touch_event_member',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ev_type', full_name='on_touch_event_member.ev_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_member', full_name='on_touch_event_member.list_member', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=569,
  serialized_end=670,
)


_CARD_SERIAL = _descriptor.Descriptor(
  name='card_serial',
  full_name='card_serial',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='card_serial.player_id', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_card_info', full_name='card_serial.list_card_info', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='score', full_name='card_serial.score', index=2,
      number=3, type=13, cpp_type=3, label=2,
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
  serialized_start=672,
  serialized_end=743,
)


_SYN_GAME_RET = _descriptor.Descriptor(
  name='syn_game_ret',
  full_name='syn_game_ret',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='room_id', full_name='syn_game_ret.room_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_member', full_name='syn_game_ret.list_member', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_car_serial', full_name='syn_game_ret.list_car_serial', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=745,
  serialized_end=856,
)

_GAME_CFG.fields_by_name['opt'].enum_type = _ROOM_OPTION
_SYN_GAME_INFO.fields_by_name['cfg'].message_type = _GAME_CFG
_SYN_GAME_INFO.fields_by_name['list_members'].message_type = _OTHER_PLAYER_INFO
_ON_TOUCH_EVENT.fields_by_name['ev_type'].enum_type = _EVENT_TYPE
_ON_TOUCH_EVENT_MEMBER.fields_by_name['ev_type'].enum_type = _EVENT_TYPE_MEMBER
_ON_TOUCH_EVENT_MEMBER.fields_by_name['list_member'].message_type = _OTHER_PLAYER_INFO
_SYN_GAME_RET.fields_by_name['list_member'].message_type = _OTHER_PLAYER_INFO
_SYN_GAME_RET.fields_by_name['list_car_serial'].message_type = _CARD_SERIAL
DESCRIPTOR.message_types_by_name['other_player_info'] = _OTHER_PLAYER_INFO
DESCRIPTOR.message_types_by_name['game_cfg'] = _GAME_CFG
DESCRIPTOR.message_types_by_name['syn_game_info'] = _SYN_GAME_INFO
DESCRIPTOR.message_types_by_name['on_touch_event'] = _ON_TOUCH_EVENT
DESCRIPTOR.message_types_by_name['on_touch_event_member'] = _ON_TOUCH_EVENT_MEMBER
DESCRIPTOR.message_types_by_name['card_serial'] = _CARD_SERIAL
DESCRIPTOR.message_types_by_name['syn_game_ret'] = _SYN_GAME_RET
DESCRIPTOR.enum_types_by_name['room_option'] = _ROOM_OPTION
DESCRIPTOR.enum_types_by_name['event_type_member'] = _EVENT_TYPE_MEMBER
DESCRIPTOR.enum_types_by_name['event_type'] = _EVENT_TYPE

other_player_info = _reflection.GeneratedProtocolMessageType('other_player_info', (_message.Message,), dict(
  DESCRIPTOR = _OTHER_PLAYER_INFO,
  __module__ = 'common_info_pb2'
  # @@protoc_insertion_point(class_scope:other_player_info)
  ))
_sym_db.RegisterMessage(other_player_info)

game_cfg = _reflection.GeneratedProtocolMessageType('game_cfg', (_message.Message,), dict(
  DESCRIPTOR = _GAME_CFG,
  __module__ = 'common_info_pb2'
  # @@protoc_insertion_point(class_scope:game_cfg)
  ))
_sym_db.RegisterMessage(game_cfg)

syn_game_info = _reflection.GeneratedProtocolMessageType('syn_game_info', (_message.Message,), dict(
  DESCRIPTOR = _SYN_GAME_INFO,
  __module__ = 'common_info_pb2'
  # @@protoc_insertion_point(class_scope:syn_game_info)
  ))
_sym_db.RegisterMessage(syn_game_info)

on_touch_event = _reflection.GeneratedProtocolMessageType('on_touch_event', (_message.Message,), dict(
  DESCRIPTOR = _ON_TOUCH_EVENT,
  __module__ = 'common_info_pb2'
  # @@protoc_insertion_point(class_scope:on_touch_event)
  ))
_sym_db.RegisterMessage(on_touch_event)

on_touch_event_member = _reflection.GeneratedProtocolMessageType('on_touch_event_member', (_message.Message,), dict(
  DESCRIPTOR = _ON_TOUCH_EVENT_MEMBER,
  __module__ = 'common_info_pb2'
  # @@protoc_insertion_point(class_scope:on_touch_event_member)
  ))
_sym_db.RegisterMessage(on_touch_event_member)

card_serial = _reflection.GeneratedProtocolMessageType('card_serial', (_message.Message,), dict(
  DESCRIPTOR = _CARD_SERIAL,
  __module__ = 'common_info_pb2'
  # @@protoc_insertion_point(class_scope:card_serial)
  ))
_sym_db.RegisterMessage(card_serial)

syn_game_ret = _reflection.GeneratedProtocolMessageType('syn_game_ret', (_message.Message,), dict(
  DESCRIPTOR = _SYN_GAME_RET,
  __module__ = 'common_info_pb2'
  # @@protoc_insertion_point(class_scope:syn_game_ret)
  ))
_sym_db.RegisterMessage(syn_game_ret)


# @@protoc_insertion_point(module_scope)