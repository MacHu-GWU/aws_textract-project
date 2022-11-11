# -*- coding: utf-8 -*-

import json
from .paths import dir_tests

dir_tests_data = dir_tests / "data"
path_tests_data_line_json = dir_tests_data / "line.json"

path_tests_data_key_value_set_key_has_relationships = (
    dir_tests_data / "key_value_set_key_has_relationships.json"
)
path_tests_data_key_value_set_value_has_relationships_json = (
    dir_tests_data / "key_value_set_value_has_relationships.json"
)
path_tests_data_key_value_set_value_no_relationships_json = (
    dir_tests_data / "key_value_set_value_no_relationships.json"
)


class TestData:
    @property
    def line(self):
        return json.loads(path_tests_data_line_json.read_text())

    @property
    def key_value_set_key_has_relationships(self):
        return json.loads(
            path_tests_data_key_value_set_key_has_relationships.read_text()
        )

    @property
    def key_value_set_value_has_relationships(self):
        return json.loads(
            path_tests_data_key_value_set_value_has_relationships_json.read_text()
        )

    @property
    def key_value_set_value_no_relationships(self):
        return json.loads(
            path_tests_data_key_value_set_value_no_relationships_json.read_text()
        )


test_data = TestData()
