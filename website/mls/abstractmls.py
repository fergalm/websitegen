# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 21:23:36 2024

@author: fergal
"""

from ipdb import set_trace as idebug
from pdb import set_trace as debug
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class AbstractMlsQuery:
    def query(self, start, end):
        raise NotImplementedError



class DummyMlsQuery(AbstractMlsQuery):
    def query(self, start, end):
        return pd.DataFrame()



