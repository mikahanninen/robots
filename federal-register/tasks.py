from robocorp.tasks import task

from bs4 import BeautifulSoup
import requests

from SQLiteDatabase import SQLiteDatabase

from RPA.Notifier import Notifier
from RPA.Robocorp.Storage import Storage
from RPA.Robocorp.Vault import Vault
from RPA.Tables import Tables

PUBLICATIONS_URL = "https://www.bis.doc.gov/index.php/federal-register-notices"
SQLITE_FILENAME = 'publications.db'
SQLITE_ASSET_NAME = 'Federal Register Notices (SQLITE DB)'
SQLITE_ASSET_EXISTS = False

def parse_table():
    html_content = requests.get(PUBLICATIONS_URL).text
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    # Extract data into a Python structure
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    columns = []
    for d in data[0]:
        # Modified column name
        if "Effective Date" in d:
            columns.append("Effective Date")
        else:
            columns.append(d)
    return Tables().create_table(data=data[1:], columns=columns)

def initialize_database():
    """Create database file if it does not exist in Asset Storage"""
    global SQLITE_ASSET_EXISTS

    DB = SQLiteDatabase(SQLITE_FILENAME)
    try:
        Storage().get_file_asset(SQLITE_ASSET_NAME, SQLITE_FILENAME, overwrite=True)
        DB.connect()
        SQLITE_ASSET_EXISTS = True
    except:
        DB.create_publications_database()
    return DB

@task
def minimal_task():
    global SQLITE_ASSET_EXISTS

    secrets = Vault().get_secret("SlackFederalRegister")
    DB = initialize_database()
    table = parse_table()
    updates = False
    for row in table:
        result = DB.execute_query(f"SELECT * FROM government_publications WHERE citation = '{row['Federal Register Citation']}'", True)
        if len(result)==0:
            DB.execute_query("INSERT INTO government_publications VALUES ('%s', '%s', '%s', '%s', '%s')" %
                (row['Federal Register Citation'],
                row['Publication Date'],
                row['Effective Date'],
                row['End of Comment Period'],
                row['Title of Federal Register'])
            )
            print(row)
            updates = True
        else:
            print(f"Already in database '{row['Federal Register Citation']}'")

    if updates:
        Storage().set_file_asset(SQLITE_ASSET_NAME, SQLITE_FILENAME)
        SQLITE_ASSET_EXISTS = True
        Notifier().notify_slack(message="New Federal Register Citations added to database", channel=secrets['channel'], webhook_url=secrets['webhookurl'])
    if not SQLITE_ASSET_EXISTS:
        Storage().set_file_asset(SQLITE_ASSET_NAME, SQLITE_FILENAME)

