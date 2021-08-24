import unittest
import randomize_color_bananas
from colorBananaData import color_banana_data_japes
from validator import kong_list

def countBananasForKong(kong_groups: list):
    totalCount = 0
    for group in kong_groups:
        for banana in group['locations']:
            totalCount += banana["amount"]
    return totalCount

def checkKongAccessibility(kong_groups: list, kong):
    for group in kong_groups:
        if group['kongs'][kong] == False:
            return False
    return True

class ColorBananaRandoTest(unittest.TestCase):
    def setUp(self):
        self.result = randomize_color_bananas.randomize(color_banana_data_japes.japes_new_banana_groups)

    def test_randomize_returnsListOfLocationsForEachKong(self):
        for kong in kong_list:
            self.assertGreater(len(self.result[kong]), 0)

    def test_randomize_thatEachKongGets100Bananas(self):
        for kong in kong_list:
            self.assertEqual(countBananasForKong(self.result[kong]), 100)
        
    def test_randomize_thatKongCanAccessEachOfTheirGroups(self):
        for kong in kong_list:
            self.assertTrue(checkKongAccessibility(self.result[kong], kong))
        
    def test_randomize_thatEveryBananaHasXYZCoordinates(self):
        for kong in kong_list:
            for banana_group in self.result[kong]:
                for banana in banana_group['locations']:
                    self.assertIsNotNone(banana['x'])
                    self.assertIsNotNone(banana['y'])
                    self.assertIsNotNone(banana['z'])
