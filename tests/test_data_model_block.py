# -*- coding: utf-8 -*-

import json
from aws_textract.data_model import Block
from aws_textract.tests import test_data


class TestBlock:
    def test(self):
        block_line = Block(data=test_data.line)
        block_key_value_set_key_has_relationships = Block(
            data=test_data.key_value_set_key_has_relationships
        )
        block_key_value_set_value_has_relationships = Block(
            data=test_data.key_value_set_value_has_relationships
        )
        block_key_value_set_value_no_relationships = Block(
            data=test_data.key_value_set_value_no_relationships
        )

        blocks = [
            block_line,
            block_key_value_set_key_has_relationships,
            block_key_value_set_value_has_relationships,
            block_key_value_set_value_no_relationships,
        ]

        for block in blocks:
            _ = block.id
            _ = block.type
            _ = block.geometry
            _ = block.bounding_box
            _ = block.polygon
            _ = block.entity_types
            _ = block.relationships
            _ = block.text
            _ = block.text_type
            _ = block.selection_status
            _ = block.column_index
            _ = block.row_index

            _ = block.is_page_block_type
            _ = block.is_line_block_type
            _ = block.is_word_block_type
            _ = block.is_key_value_set_block_type
            _ = block.is_selection_element_block_type
            _ = block.is_table_block_type
            _ = block.is_cell_block_type
            _ = block.is_merged_cell_block_type
            _ = block.is_query_block_type
            _ = block.is_query_result_block_type

        _ = block_key_value_set_key_has_relationships.child_ids
        _ = block_key_value_set_key_has_relationships.value_ids


if __name__ == "__main__":
    from aws_textract.tests import run_cov_test

    run_cov_test(__file__, "aws_textract.data_model")
