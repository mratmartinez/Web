import unittest

import locale
from juancito import format_date, slugify

class TestMarkdown(unittest.TestCase):
    def test_format_date(self):
        data = '2019-11-28'
        result = format_date(data)
        self.assertEqual(result, "Jueves 28 de Noviembre de 2019")


    def test_slugify(self):
        data = "¡Este podría ser el mejor título del mundo si no fuera testing!"
        result = slugify(data)
        expected = "este-podria-ser-el-mejor-titulo-del-mundo-si-no-fuera-testing"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, 'es_AR')
    unittest.main()
