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
import ssl

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
SAMPLE_RANGE_NAME = 'Boston Red Sox!A1:X14'


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
        print("---------------------------------------------------------")
        ssl._create_default_https_context = ssl._create_unverified_context
        hrefList = []
        for site in sitesList[1:]:
            titleList = []
            # print(site)

            if site[4]:
                url = site[1]
                text = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(text, 'html.parser')
                for item in soup.select(site[4]):
                    if item[site[5]] and item.select(site[6]) and item.select(site[6])[0] and item.select(site[6])[
                        0].text:
                        # print(item.select(site[6])[0].text)
                        hrefList.append(item[site[5]])
                        hrefList.append(item.select(site[6])[0].text)
                    elif item[site[5]] and site[6] == "a":
                        hrefList.append(item[site[5]])
                        hrefList.append(item.text)
                    # print(hrefList)
                used = set()
                unique = [x for x in hrefList if x not in used and (used.add(x) or True)]
                hrefList = unique
                zipped = zip(unique[0::2], unique[1::2])
                """
                for x in zipped:
                    print(x[0], x[1])
                """
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
            if site[7]:
                hrefListTemp = []
                for item in soup.select(site[7]):
                    if item[site[8]] and site[9] != "a" and item.select(site[9]) and item.select(site[9])[0] and \
                            item.select(site[9])[0].text:
                        # print(item.select(site[6])[0].text)
                        hrefListTemp.append(item[site[8]])
                        hrefListTemp.append(item.select(site[9])[0].text)
                    elif item[site[8]] and site[9] == "a":
                        hrefListTemp.append(item[site[8]])
                        hrefListTemp.append(item.text)
                    # print(hrefList)
                used = set()
                unique = [x for x in hrefListTemp if x not in used and (used.add(x) or True)]
                hrefList = hrefList + unique
                zipped = zip(unique[0::2], unique[1::2])
                """
                for x in zipped:
                    print(x[0], x[1])
                """
        print("hrefList")
        print(hrefList)
        zipped = zip(hrefList[0::2], hrefList[1::2])
        print("zipped")
        print(zipped)
        for x in zipped:
            print(x[0], x[1])

    except HttpError as err:
        print(err)

if __name__ == '__main__':
    main()
# [END sheets_quickstart]