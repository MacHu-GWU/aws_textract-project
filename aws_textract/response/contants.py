# -*- coding: utf-8 -*-

import enum


class BlockTypeEnum(str, enum.Enum):
    """
    The value enum for ``response["Blocks"][0]["BlockType"]`` in the textract
    response object.

    See more details at: https://docs.aws.amazon.com/textract/latest/dg/API_Block.html
    """

    PAGE = "PAGE"
    LINE = "LINE"
    WORD = "WORD"
    KEY_VALUE_SET = "KEY_VALUE_SET"
    TABLE = "TABLE"
    TABLE_TITLE = "TABLE_TITLE"
    TABLE_FOOTER = "TABLE_FOOTER"
    CELL = "CELL"
    MERGED_CELL = "MERGED_CELL"
    SELECTION_ELEMENT = "SELECTION_ELEMENT"
    SIGNATURE = "SIGNATURE"
    QUERY = "QUERY"
    QUERY_RESULT = "QUERY_RESULT"
    LAYOUT_TITLE = "LAYOUT_TITLE"
    LAYOUT_HEADER = "LAYOUT_HEADER"
    LAYOUT_FOOTER = "LAYOUT_FOOTER"
    LAYOUT_SECTION_HEADER = "LAYOUT_SECTION_HEADER"
    LAYOUT_PAGE_NUMBER = "LAYOUT_PAGE_NUMBER"
    LAYOUT_LIST = "LAYOUT_LIST"
    LAYOUT_FIGURE = "LAYOUT_FIGURE"
    LAYOUT_TABLE = "LAYOUT_TABLE"
    LAYOUT_KEY_VALUE = "LAYOUT_KEY_VALUE"
    LAYOUT_TEXT = "LAYOUT_TEXT"
