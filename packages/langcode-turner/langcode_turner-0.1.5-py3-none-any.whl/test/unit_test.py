from langcode_turner import langcode_turner
import unittest

class Test(unittest.TestCase):

    def test_iso639_turner(self):
        turn = langcode_turner("fr")
        assert turn.iso_639_3 == "fra"

    def test_iso639_turn_to_ids_code(self):
        turn = langcode_turner("est")
        assert turn.ids_code == "127"

    def test_iso639_turn_to_ids_code_error(self):
        turn = langcode_turner("jpn")
        assert turn.ids_code == ""
    
    def test_language_name_to_turn(self):
        turn = langcode_turner("French")
        assert turn.iso_639_3 == "fra"

    def test_lanauge_name_to_wordnet(self):
        turn = langcode_turner("Chinese")
        assert turn.wordnet() == "cmn"
        turn = langcode_turner("French")
        assert turn.wordnet() == "fr"
if __name__ == '__main__':
    unittest.main()