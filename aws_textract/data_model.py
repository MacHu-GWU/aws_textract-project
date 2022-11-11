# -*- coding: utf-8 -*-

import enum
import dataclasses


class BlockTypeEnum(enum.Enum):
    page = "PAGE"
    line = "LINE"
    word = "WORD"

    key_value_set = "KEY_VALUE_SET"
    selection_element = "SELECTION_ELEMENT"

    table = "TABLE"
    cell = "CELL"
    merged_cell = "MERGED_CELL"


_text_type = [
    BlockTypeEnum.page.value,
    BlockTypeEnum.line.value,
    BlockTypeEnum.word.value,
]

_form_type = [
    BlockTypeEnum.key_value_set.value,
    BlockTypeEnum.selection_element.value,
]

_table_type = [
    BlockTypeEnum.table.value,
    BlockTypeEnum.cell.value,
    BlockTypeEnum.merged_cell.value,
]


class RelationshipTypeEnum(enum.Enum):
    child = "CHILD"
    value = "VALUE"


class EntityValueEnum(enum.Enum):
    key = "KEY"
    value = "VALUE"
