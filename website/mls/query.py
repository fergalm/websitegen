# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 21:13:46 2024

@author: fergal
"""

from .abstractmls import AbstractMlsQuery
import homeharvest

class HomeHarvestMlsQuery(AbstractMlsQuery):
    def query(self, start, end):


        df = homeharvest.scrape_property(
            location="Baltimore County, MD",
            listing_type='sold',
            date_from=str(start)[:10],
            date_to=str(end)[:10],
        )
        return df


