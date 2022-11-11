# -*- coding: utf-8 -*-

import typing as T
import enum
import dataclasses

from .compat import cached_property


class BlockTypeEnum(enum.Enum):
    page = "PAGE"
    line = "LINE"
    word = "WORD"

    key_value_set = "KEY_VALUE_SET"
    selection_element = "SELECTION_ELEMENT"

    table = "TABLE"
    cell = "CELL"
    merged_cell = "MERGED_CELL"

    query = "QUERY"
    query_result = "QUERY_RESULT"


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


class TextTypeEnum(enum.Enum):
    hand_writing = "HANDWRITING"
    printed = "PRINTED"


class RelationshipTypeEnum(enum.Enum):
    child = "CHILD"
    value = "VALUE"
    complex_features = "COMPLEX_FEATURES"
    merged_cell = "MERGED_CELL"
    title = "TITLE"
    answer = "ANSWER"


class EntityTypeEnum(enum.Enum):
    key = "KEY"
    value = "VALUE"
    column_header = "COLUMN_HEADER"


class SelectionEnum(enum.Enum):
    selected = "SELECTED"
    not_selected = "NOT_SELECTED"


# ------------------------------------------------------------------------------
# Block
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class BoundingBox:
    height: float
    width: float
    left: float
    top: float


@dataclasses.dataclass
class Point:
    x: float
    y: float


@dataclasses.dataclass
class Polygon:
    points: T.List[Point]


@dataclasses.dataclass
class Geometry:
    bounding_box: BoundingBox
    polygon: Polygon


@dataclasses.dataclass
class Relationship:
    ids: T.List[str]
    type: str


@dataclasses.dataclass
class Block:
    """
    Ref:

    - https://docs.aws.amazon.com/textract/latest/dg/API_Block.html
    """

    data: T.Dict[str, T.Any] = dataclasses.field()

    @property
    def id(self) -> str:
        return self.data["Id"]

    @property
    def type(self) -> str:
        return self.data["BlockType"]

    @property
    def confidence(self) -> float:
        return self.data["Confidence"]

    @cached_property
    def geometry(self) -> T.Optional[Geometry]:
        geometry = self.data.get("Geometry")
        if geometry is None:
            return geometry
        else:
            return Geometry(
                bounding_box=BoundingBox(
                    height=geometry["BoundingBox"]["Height"],
                    left=geometry["BoundingBox"]["Left"],
                    top=geometry["BoundingBox"]["Top"],
                    width=geometry["BoundingBox"]["Width"],
                ),
                polygon=Polygon(
                    points=[
                        Point(x=dct["X"], y=dct["Y"]) for dct in geometry["Polygon"]
                    ]
                ),
            )

    @cached_property
    def bounding_box(self) -> T.Optional[BoundingBox]:
        if self.geometry is None:
            return None
        else:
            return self.geometry.bounding_box

    @cached_property
    def polygon(self) -> T.Optional[Polygon]:
        if self.geometry is None:
            return None
        else:
            return self.geometry.polygon

    @property
    def entity_types(self) -> T.Optional[T.List[str]]:
        return self.data.get("EntityTypes", None)

    @cached_property
    def relationships(self) -> T.Optional[T.List[Relationship]]:
        relationships = self.data.get("Relationships")
        if relationships is None:
            return relationships
        else:
            return [
                Relationship(
                    ids=dct["Ids"],
                    type=dct["Type"],
                )
                for dct in relationships
            ]

    @property
    def text(self) -> T.Optional[str]:
        return self.data.get("Text")

    @property
    def text_type(self) -> T.Optional[str]:
        return self.data.get("TextType")

    # -------------------------------------------------------------------------
    # Key Value Pair related
    # -------------------------------------------------------------------------
    @property
    def selection_status(self) -> T.Optional[str]:
        return self.data.get("SelectionStatus")

    # -------------------------------------------------------------------------
    # Table Cell related
    # -------------------------------------------------------------------------
    @property
    def column_index(self) -> T.Optional[int]:
        return self.data.get("ColumnIndex")

    @property
    def row_index(self) -> T.Optional[int]:
        return self.data.get("ColumnIndex")

    # -------------------------------------------------------------------------
    # Helper Attributes
    # -------------------------------------------------------------------------
    # --- block type related
    @property
    def is_page_block_type(self) -> bool:
        return self.type == BlockTypeEnum.page.value

    @property
    def is_line_block_type(self) -> bool:
        return self.type == BlockTypeEnum.line.value

    @property
    def is_word_block_type(self) -> bool:
        return self.type == BlockTypeEnum.word.value

    @property
    def is_key_value_set_block_type(self) -> bool:
        return self.type == BlockTypeEnum.key_value_set.value

    @property
    def is_selection_element_block_type(self) -> bool:
        return self.type == BlockTypeEnum.selection_element.value

    @property
    def is_table_block_type(self) -> bool:
        return self.type == BlockTypeEnum.table.value

    @property
    def is_cell_block_type(self) -> bool:
        return self.type == BlockTypeEnum.cell.value

    @property
    def is_merged_cell_block_type(self) -> bool:
        return self.type == BlockTypeEnum.merged_cell.value

    @property
    def is_query_block_type(self) -> bool:
        return self.type == BlockTypeEnum.query.value

    @property
    def is_query_result_block_type(self) -> bool:
        return self.type == BlockTypeEnum.query_result.value

    # --- entity types related
    @property
    def is_single_entity(self) -> bool:
        if self.entity_types is None:
            return False
        else:
            return len(self.entity_types) == 1

    @property
    def is_key_entity(self) -> bool:
        return (
            self.is_single_entity and self.entity_types[0] == EntityTypeEnum.key.value
        )

    @property
    def is_value_entity(self) -> bool:
        return (
            self.is_single_entity and self.entity_types[0] == EntityTypeEnum.value.value
        )

    @property
    def is_column_header_entity(self) -> bool:
        return (
            self.is_single_entity
            and self.entity_types[0] == EntityTypeEnum.column_header.value
        )

    @property
    def is_key_value_set_key(self) -> bool:
        return (
            self.is_single_entity
            and self.entity_types[0] == EntityTypeEnum.column_header.value
        )

    # --- relationships related
    @cached_property
    def _relationships_mapper(self) -> T.Dict[str, Relationship]:
        if self.relationships is None:
            return {}
        else:
            return {
                relationship.type: relationship for relationship in self.relationships
            }

    def _get_relationship_by_type(
        self, relationship_type: RelationshipTypeEnum
    ) -> Relationship:
        if self._relationships_mapper:
            return self._relationships_mapper[relationship_type.value]

    @property
    def child_ids(self) -> T.List[str]:
        return self._get_relationship_by_type(RelationshipTypeEnum.child).ids

    @property
    def value_ids(self) -> T.List[str]:
        return self._get_relationship_by_type(RelationshipTypeEnum.value).ids

    @property
    def complex_features_ids(self) -> T.List[str]:
        return self._get_relationship_by_type(RelationshipTypeEnum.complex_features).ids

    @property
    def merged_cell_ids(self) -> T.List[str]:
        return self._get_relationship_by_type(RelationshipTypeEnum.merged_cell).ids

    @property
    def title_ids(self) -> T.List[str]:
        return self._get_relationship_by_type(RelationshipTypeEnum.title).ids

    @property
    def answer_ids(self) -> T.List[str]:
        return self._get_relationship_by_type(RelationshipTypeEnum.answer).ids
