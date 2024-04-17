# -*- coding: utf-8 -*-

import typing as T

from .contants import BlockTypeEnum

if T.TYPE_CHECKING:
    from mypy_boto3_textract.type_defs import BlockTypeDef


def blocks_to_text(blocks: T.List["BlockTypeDef"]) -> str:
    """
    Convert Textract blocks to text.

    :param blocks: List of Textract `blocks <https://docs.aws.amazon.com/textract/latest/dg/API_Block.html>`_.
    """
    lines = list()
    for block in blocks:
        if block["BlockType"] == BlockTypeEnum.LINE.value:
            lines.append(block["Text"])
    return "\n".join(lines)
