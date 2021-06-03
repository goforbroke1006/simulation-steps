from unittest import TestCase

from simulationsteps.utils import json_get_value


class UtilsTest(TestCase):
    def test_json_get_value(self):
        content = """
        {
          "items": [
            {"name": "item 1", "summary": {"age": 10, "height": 175}},
            {"name": "item 2", "summary": {"age": 20, "height": 185}},
            {"name": "item 3", "summary": {"age": 30, "height": 195}}
          ]
        }
        """

        expected = ["item 2"]
        actual = json_get_value(content, "$.items[1].name")

        assert expected == actual, f'{actual} != {expected}'
