# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

MAX_QUALITY = 50
MIN_QUALITY = 0

class QualityRules:
    '''For quality adjustments with bounds'''
    def increase_quality(self, item, amount=1):
        item.quality = max(MIN_QUALITY, min(MAX_QUALITY, item.quality + amount))
    def decrease_quality(self, item, amount=1): 
        item.quality = max(MIN_QUALITY, min(MAX_QUALITY, item.quality - amount))
        

class UpdateStrategy(ABC, QualityRules):
    @abstractmethod
    def update_item(self, item):
        pass

class NormalItems(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in > 0:
            # degrade by 1 
            self.decrease_quality(item, 1)
        else:
            # degrade twice
            self.decrease_quality(item, 2)
        item.sell_in -= 1

class AgedBrie(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in > 0:
            # increase by 1
            self.increase_quality(item, 1)
        else:
            # increase twice
            self.increase_quality(item, 2)
        item.sell_in -= 1

class BackstagePasses(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in <= 0:
           item.quality = 0
        elif item.sell_in <= 5:
            # increase by 3
            self.increase_quality(item, 3)
        elif item.sell_in <= 10:
            # increase by 2
            self.increase_quality(item, 2)
        else:
            # increase by 1
            self.increase_quality(item, 1)
        item.sell_in -= 1

class Sulfuras(UpdateStrategy):
    def update_item(self, item):
        # No changes for Sulfuras
        pass

class Conjured(UpdateStrategy):
    def update_item(self, item):
        if item.sell_in > 0:
            # degrade twice
            self.decrease_quality(item, 2)
        else:
            # degrade four times
            self.decrease_quality(item, 4)
        item.sell_in -= 1

# Mapping item names to their respective strategies
STRATEGY_MAP = {
    "Aged Brie": AgedBrie,
    "Backstage passes to a TAFKAL80ETC concert": BackstagePasses,
    "Sulfuras, Hand of Ragnaros": Sulfuras,
}

# mapping for items with specific prefixes
PREFIX_STRATEGIES = {
    "Conjured": Conjured,
}


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def get_strategy(self, item):
        if item.name in STRATEGY_MAP:
            return STRATEGY_MAP[item.name]()
        for prefix, strategy in PREFIX_STRATEGIES.items():
            if item.name.startswith(prefix):
                return strategy()
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
