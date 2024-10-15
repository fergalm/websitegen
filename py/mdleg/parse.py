from ipdb import set_trace as idebug
import pandas as pd
import datetime
import os

"""
Track bill progress in legislature

Input json file is from
https://mgaleg.maryland.gov/mgawebsite/Legislation/Index/house
Click "Download Legistlative Data" at bottom right of footer

Run the script main, and two html pages are uploaded to
https://fergalm.neocities.org/politics/state/

house.html is a searchable table of house bills
senate.html is a searchable table of senate bills

TODO:
o Set up an always on machine to run this code
o Setup up gmail connectivity to email on errors
o Advertise
o Filter out bills with no action??
o html title tags of house and senate
o Column renaming
o Site statistics
o Why does -- become garbled in html?
"""

from io import StringIO
import requests
from website.utils import neocities
from website.utils import error
from website.utils import gmail

def main(jsontext=None):

    year = 2024
    api_key = os.environ['NEOCITIES_API_KEY']
    nc = neocities.NeoCities(api_key=api_key)

    from_addr = os.environ['GMAIL_ADDRESS']
    app_pwd = os.environ['GMAIL_APP_PWD']
    to_addr = "fergal.mullally@gmail.com"
    emailer = gmail.Gmail(from_addr, app_pwd)
    #emailer = gmail.DummyEmail()

    with error.ErrorHandler(emailer, to_addr):
        run(year, nc )

def run(year, neocities, jsontext=None):
    if jsontext is None:
        jsontext = download(year)
    df = pd.read_json(StringIO(jsontext))

    house = df[df.BillNumber.str[:2].isin(["HB", "HJ"])]
    senate = df[df.BillNumber.str[:2].isin(["SB", "SJ"])]
    assert len(df) == len(house) + len(senate)

    house= convert_to_html(house, "House Bills", year)
    senate= convert_to_html(senate, "Senate Bills", year)

    upload(neocities, house,  "politics/state/house.html")
    upload(neocities, senate, "politics/state/senate.html")
    #save(house, "politics/state/house.html")
    return df


def save(html, remote_path):
    """A debugging func"""
    local_file = remote_path.split('/')[-1]

    with open(local_file, 'w') as fp:
        fp.write(html)


def upload(neocities, html,remote_path):
    local_file = remote_path.split('/')[-1]

    with open(local_file, 'w') as fp:
        fp.write(html)

    neocities.upload( (local_file, remote_path))




def download(year):
    url = f"https://mgaleg.maryland.gov/{year}rs/misc/billsmasterlist/legislation.json"

    response = requests.get(url)
    response.raise_for_status()

    text = response.text
    return text



def convert_to_html(df, title, year):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    status = map(set_current_status, df.iterrows())
    status = pd.concat(status)
    df = df.merge(status, on='BillNumber')

    #df = df[:5]

    df['BillNumber'] = df.BillNumber.apply(make_link, year=year)

    cols = "BillNumber CrossfileBillNumber SponsorPrimary Title CommitteePrimaryOrigin Progression DateNextAction".split()

    html = df[cols].to_html(table_id="myTable", index=False, escape=False, classes=["stripe", "hover", "cell-border"])
    template = load_template("template.html")
    html = template %(title, now, html)
    return html

def make_link(billnum, year):
    strr = f"<A href='https://mgaleg.maryland.gov/mgawebsite/Legislation/Details/{billnum.lower()}?ys={year}RS'>{billnum}</A>"

    return strr


def load_template(fn):
    with open(fn) as fp:
        return fp.read()



def set_current_status(row):
    i, row = row

    cols = """
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
        ReportDateOppositeHouse                                                                    """.split()

    status = "Unfiled"
    date = "2011-09-18"
    for c in cols:

        if isinstance(row[c], str) and len(row[c]) > 9:
            status = c
            date = row[c]

    out = pd.DataFrame()
    out['BillNumber'] = [row.BillNumber]
    out['Progression'] = [status]
    out['DateNextAction'] = [date]
    return out

