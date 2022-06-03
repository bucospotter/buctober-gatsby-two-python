# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function
import urllib.request
from bs4 import BeautifulSoup

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1FV4JCdbJ6GiTgJiARXflbdth7kRB8WXu6izFndP6Um8'
SAMPLE_RANGE_NAME = 'Pittsburgh Pirates!A1:Z14'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        sitesList = []

        if not values:
            print('No data found.')
            return

        # print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            sitesList.append(row)
    except HttpError as err:
        print(err)
    print("---------------------------------------------------------")
    for site in sitesList[1:]:
        url = site[1]
        text = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(text,'html.parser')
        hrefList = []
        titleList = []
        # print(site)

        if site[4]:
            for item in soup.select(site[9]):
                if item[site[10]] and item.select(site[11]) and item.select(site[11])[0] and item.select(site[11])[0].text:
                    # print(item.select(site[11])[0].text)
                    hrefList.append(item[site[10]])
                    hrefList.append(item.select(site[11])[0].text)
                # print(hrefList)
            used = set()
            unique = [x for x in hrefList if x not in used and (used.add(x) or True)]
            zipped = zip(unique[0::2], unique[1::2])
            for x in zipped:
                print(x[0], x[1])
            """
            for item in soup.select(site[4]):
                hrefList.append(item[site[5]])
            """
        """
        if site[6]:
            for item in soup.select(site[6]):
                titleList.append(item.text)
            used = set()
            unique = [x for x in titleList if x not in used and (used.add(x) or True)]
            #print(unique)
        """

if __name__ == '__main__':
    main()
# [END sheets_quickstart]