#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pp1
import unittest

class KnownValues(unittest.TestCase):
    known_values = (('森林里住着一只小兔子，它叫“丑丑”', ['森', '林', '里', '住', '着', '一', '只', '小', '兔', '子', '它', '叫', '丑', '丑']),
                    ('一次，森林里最好看的小兔子美美来找它玩，可丑丑觉得自己太丑了，没脸见它。', ['一', '次', '森', '林', '里', '最', '好', '看', '的', '小', '兔', '子', '美', '美', '来', '找', '它', '玩', '可', '丑', '丑', '觉', '得', '自', '己', '太', '丑', '了', '没', '脸', '见', '它']))

    def test_remove_punctuation_known_values(self):
        """Remove_punctuation should give known result with known input."""
        for str_punct, str_unpunct in self.known_values:
            result = pp1.remove_punctuation(str_punct)
            self.assertEqual(str_unpunct, result)

if __name__ == '__main__':
    unittest.main()


