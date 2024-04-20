# -*- coding: utf-8 -*-

import typing as T

from .contants import BlockTypeEnum

if T.TYPE_CHECKING: # pragma: no cover
    from mypy_boto3_textract.type_defs import BlockTypeDef


def blocks_to_text(
    blocks: T.List["BlockTypeDef"],
) -> str:
    """
    Convert Textract blocks to text.

    :param blocks: List of Textract `blocks <https://docs.aws.amazon.com/textract/latest/dg/API_Block.html>`_.
    """
    lines = list()
    for block in blocks:
        if block["BlockType"] == BlockTypeEnum.LINE.value:
            lines.append(block["Text"])
    return "\n".join(lines)


def split_blocks_by_page(
    blocks: T.List["BlockTypeDef"],
) -> T.Dict[int, T.List["BlockTypeDef"]]:
    block_mapper: T.Dict[int, T.List[dict]] = dict()
    for block in blocks:
        page = block["Page"]
        try:
            block_mapper[page].append(block)
        except KeyError:
            block_mapper[page] = [block]
    block_mapper = dict(sorted(block_mapper.items(), key=lambda x: x[0]))
    return block_mapper
