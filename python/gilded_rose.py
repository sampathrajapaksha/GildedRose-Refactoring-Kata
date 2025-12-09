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

class Conjured(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in > 0:
            # degrade twice
            item.quality = max(item.quality - 2, MIN_QUALITY)
        else:
            # degrade four times
            item.quality = max(item.quality - 4, MIN_QUALITY)
        item.sell_in -= 1


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def get_strategy(self, item):
        if item.name == "Aged Brie":
            return AgedBrie()
        elif item.name.startswith("Backstage passes"):
            return BackstagePasses()
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return Sulfuras()
        elif item.name.startswith("Conjured"):
            return Conjured()  # Placeholder with normal item behavior
        else:
            return NormalItems()

    def update_quality(self):
        for item in self.items:
            strategy = self.get_strategy(item)
            strategy.update_item(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
