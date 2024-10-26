# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 20:50:19 2024

@author: fergal
"""

from ipdb import set_trace as idebug
from pdb import set_trace as debug
import pandas as pd
import numpy as np

from .query import HomeHarvestMlsQuery

from .abstractmls import AbstractMlsQuery
from website.utils import error
from website.utils import gmail
import os


def main():


    from_addr = os.environ['GMAIL_ADDRESS']
    app_pwd = os.environ['GMAIL_APP_PWD']
    to_addr = "fergal.mullally@gmail.com"
    # emailer = gmail.Gmail(from_addr, app_pwd)
    emailer = gmail.DummyEmail()

    error_handler = error.ErrorHandler(emailer, to_addr)
    query =HomeHarvestMlsQuery()
    outpath = os.path.join(os.environ['HOME'], "data/mls")

    run(error_handler, query, outpath)

def run(error_handler: error.ErrorHandler, mls_query:AbstractMlsQuery, outpath:str):
    with error_handler:
        end = pd.to_datetime("now")
        end = end.floor('1D') + pd.to_timedelta('6H')
        start = end - pd.DateOffset(months=1)

        os.makedirs(outpath, exist_ok=True)
        idebug()
        df = mls_query.query(start, end)
        save(df, outpath, start, end)


def save(df, path, start, end):
    d1 = start.isoformat()[:7]
    d2 = end.isoformat()[:7]
    fn = f"mls_{d1}to{d2}.csv"
    path = os.path.join(path, fn)
    df.to_csv(path)
