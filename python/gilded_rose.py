# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

MAX_QUALITY = 50
MIN_QUALITY = 0

class UpdateStrategy(ABC):
    @abstractmethod
    def update_item(self, item):
        pass

class NormalItems(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in > 0:
            # degrade by 1
            item.quality = max(item.quality - 1, MIN_QUALITY)
        else:
            # degrade twice
            item.quality = max(item.quality - 2, MIN_QUALITY)
        item.sell_in -= 1

class AgedBrie(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in > 0:
            # increase by 1
            item.quality = min(item.quality + 1, MAX_QUALITY)
        else:
            # increase twice
            item.quality = min(item.quality + 2, MAX_QUALITY)
        item.sell_in -= 1

class BackstagePasses(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in <= 0:
           item.quality = 0
        elif item.sell_in <= 5:
            # increase by 3
            item.quality = min(item.quality + 3, MAX_QUALITY)
        elif item.sell_in <= 10:
            # increase by 2
            item.quality = min(item.quality + 2, MAX_QUALITY)
        else:
            # increase by 1
            item.quality = min(item.quality + 1, MAX_QUALITY)
        item.sell_in -= 1

class Sulfuras(UpdateStrategy):
    def update_item(self, item):
        # No changes for Sulfuras
        pass


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
