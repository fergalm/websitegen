# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 21:32:20 2024

@author: fergal
"""

from io import StringIO
import pandas as pd
import requests

class DummyMdLegQuery:
    def download(self, year:int) -> pd.DataFrame:

        cols = """
            Billumber
            CrossfileBillNumber
            SponsorPrimary
            Title
            CommitteePrimaryOrigin
            Progression
            DateNextAction
            FirstReadingDateHouseOfOrigin
            HearingDateTimePrimaryHouseOfOrigin
            HearingDateTimeSecondaryHouseOfOrigin
            ReportDateHouseOfOrigin
            ReportActionHouseOfOrigin
            SecondReadingDateHouseOfOrigin
            SecondReadingActionHouseOfOrigin
            ThirdReadingDateHouseOfOrigin
            ThirdReadingActionHouseOfOrigin
            FirstReadingDateOppositeHouse
            HearingDateTimePrimaryOppositeHouse
            HearingDateTimeSecondaryOppositeHouse
            ReportDateOppositeHouse
        """.split()

        cols = [
            'BillNumber', 'ChapterNumber', 'CrossfileBillNumber',
           'SponsorPrimary', 'Sponsors', 'Synopsis', 'Title', 'Status',
           'CommitteePrimaryOrigin', 'CommitteeSecondaryOrigin',
           'CommitteePrimaryOpposite', 'CommitteeSecondaryOpposite',
           'FirstReadingDateHouseOfOrigin', 'HearingDateTimePrimaryHouseOfOrigin',
           'HearingDateTimeSecondaryHouseOfOrigin', 'ReportDateHouseOfOrigin',
           'ReportActionHouseOfOrigin', 'SecondReadingDateHouseOfOrigin',
           'SecondReadingActionHouseOfOrigin', 'ThirdReadingDateHouseOfOrigin',
           'ThirdReadingActionHouseOfOrigin', 'FirstReadingDateOppositeHouse',
           'HearingDateTimePrimaryOppositeHouse',
           'HearingDateTimeSecondaryOppositeHouse', 'ReportDateOppositeHouse',
           'ReportActionOppositeHouse', 'SecondReadingDateOppositeHouse',
           'SecondReadingActionOppositeHouse', 'ThirdReadingDateOppositeHouse',
           'ThirdReadingActionOppositeHouse', 'InteractionBetweenChambers',
           'PassedByMGA', 'EmergencyBill', 'ConstitutionalAmendment',
           'BroadSubjects', 'NarrowSubjects', 'BillType', 'BillVersion',
           'Statutes', 'YearAndSession', 'StatusCurrentAsOf'
          ],

        df = pd.DataFrame(columns=cols)
        df['BillNumber'] = "HB1 SB1".split()
        df['FirstReadingDateHouseOfOrigin'] = f"{year}-09-18"

        return df

class MdLegQuery:
    def download(self, year:int) -> pd.DataFrame:
        url = f"https://mgaleg.maryland.gov/{year}rs/misc/billsmasterlist/legislation.json"

        response = requests.get(url)
        response.raise_for_status()

        text = response.text
        df = pd.read_json(StringIO(text))
        df.to_csv('tmp.csv')
        return df
