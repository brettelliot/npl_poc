from unittest import TestCase

import npl_poc

class TestTruncateToLimit(TestCase):

    def test_truncate_text_to_limit(self):
        # Given
        filepath = 'dummy_filepath'
        text = 'aaaaaaaaaaa'
        max_length = 10
        actual = npl_poc.truncate_text_to_limit(filepath, text, max_length)
        expected = 'aaaaaaaaaa'
        self.assertEqual(actual, expected)