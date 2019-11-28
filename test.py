import unittest

import locale
from juancito import format_date 

class TestMarkdown(unittest.TestCase):
    def test_format_date(self):
        data = '2019-11-28'
        result = format_date(data)
        self.assertEqual(result, "Jueves 28 de Noviembre de 2019")

if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, 'es_AR')
    unittest.main()
