import unittest

from genpage import extract_title


class TestGenPage(unittest.TestCase):
    def test_title(self):
        self.assertEqual("Gut!", extract_title("# Gut!"))
        self.assertRaises(Exception, extract_title, "Bye")


if __name__ == "__main__":
    unittest.main()
