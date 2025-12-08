# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    # tests for normal items
    def test_normal_item_degrades_by_one(self):
        '''test that normal item quality degrades by one before sell by date'''
        items = [Item("foo", 10, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(19, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

    def test_normal_item_quality_never_negative(self):
        '''normal item quality never goes below zero'''
        items = [Item("foo", 5, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_normal_item_degrades_twice_as_fast_after_sell_by(self):
        '''normal item degrades twice as fast after sell by date'''
        items = [Item("foo", 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(18, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)
    

    # tests for Aged Brie
    def test_aged_brie_increases_in_quality(self):
        '''Aged Brie increases in quality as it ages'''
        items = [Item("Aged Brie", 2, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(1, items[0].quality)
        self.assertEqual(1, items[0].sell_in)

    def test_aged_brie_quality_never_exceeds_50(self):
        '''Aged Brie quality is capped at 50'''
        items = [Item("Aged Brie", 5, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)

    def test_aged_brie_increases_twice_as_fast_after_sell_by(self):
        '''Aged Brie increases in quality twice as fast after sell by date'''
        items = [Item("Aged Brie", 0, 48)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    # tests for backstage passes
    def test_backstage_pass_increases_by_one_when_more_than_10_days(self):
        '''Backstage pass quality increases by 1 when more than 10 days left'''
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(21, items[0].quality)
        self.assertEqual(14, items[0].sell_in)

    def test_backstage_pass_increases_by_two_when_10_days_or_less(self):
        '''Backstage pass quality increases by 2 when 10 days or less left'''
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(22, items[0].quality) # increase by 2
        self.assertEqual(9, items[0].sell_in)

    def test_backstage_pass_increases_by_three_when_5_days_or_less(self):
        '''Backstage pass quality increases by 3 when 5 days or less left'''
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(23, items[0].quality) # increase by 3
        self.assertEqual(4, items[0].sell_in)

    def test_backstage_pass_quality_drops_to_zero_after_concert(self):
        '''Backstage pass quality drops to 0 after the concert'''
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_backstage_pass_quality_never_exceeds_50(self):
        '''Backstage pass quality is capped at 50'''
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)

    # tests for Sulfuras
    def test_sulfuras_quality_never_changes(self):
        '''Sulfuras quality never changes'''
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)

    def test_sulfuras_sell_in_never_changes(self):
        '''Sulfuras sell_in value never changes'''
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(5, items[0].sell_in)

    def test_sulfuras_unchanged_even_after_sell_date(self):
        '''Sulfuras remains unchanged even after sell by date'''
        items = [Item("Sulfuras, Hand of Ragnaros", -1, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    # # tests for Conjured items (Should be passed after modification)
    # def test_conjured_items_degrade_twice_as_fast(self):
    #     '''Conjured items degrade in quality twice as fast as normal items'''
    #     items = [Item("Conjured Mana Cake", 3, 6)]
    #     gilded_rose = GildedRose(items)
    #     gilded_rose.update_quality()
    #     self.assertEqual(4, items[0].quality)  # 6 - 2
    #     self.assertEqual(2, items[0].sell_in)

    # def test_conjured_items_degrade_four_times_after_sell_date(self):
    #     '''Conjured items degrade in quality four times as fast after sell by date'''
    #     items = [Item("Conjured Mana Cake", 0, 8)]
    #     gilded_rose = GildedRose(items)
    #     gilded_rose.update_quality()
    #     self.assertEqual(4, items[0].quality)  # 8 - 4
    #     self.assertEqual(-1, items[0].sell_in)

    # def test_conjured_items_quality_never_negative(self):
    #     '''Conjured items quality never goes below zero'''
    #     items = [Item("Conjured Mana Cake", 5, 1)]
    #     gilded_rose = GildedRose(items)
    #     gilded_rose.update_quality()
    #     self.assertEqual(0, items[0].quality)  # 1 - 2 → cannot go below zero

    # def test_conjured_items_quality_floor(self):
    #     '''Conjured items quality does not go negative when starting at zero'''
    #     items = [Item("Conjured Mana Cake", 5, 0)]
    #     gilded_rose = GildedRose(items)
    #     gilded_rose.update_quality()
    #     self.assertEqual(0, items[0].quality)

        
if __name__ == '__main__':
    unittest.main(verbosity=2)
