# import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from collections import defaultdict
import json

from app import app
from app.color_print import cprint, PrintException


# SPREADSHEET_ID = app.config['SPREADSHEET_ID']


class MySpreadSheet(object):

    def __init__(self, spreadsheet_id=None, pth_to_credentials=None, range=None):
        self._spreadsheet_id = spreadsheet_id
        self.sheet_title = []
        self.spread_dict = defaultdict(list)
        self.spread_dict.clear()

        if pth_to_credentials is not None:
            self._credentials_file = pth_to_credentials
        else:
            self._credentials_file = 'credentials/client_secret.json'

        if range is None:
            self.range = "A1:AG15"
        else:
            self.range = range

    def _get_credentials(self):
        creds = None

        cprint('BLUE', "[_get_credentials] current dir: " + os.path.abspath(os.getcwd()))

        if os.path.exists('credentials/token.pickle'):

            with open('credentials/token.pickle', 'rb') as token:

                creds = pickle.load(token)

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:

                creds.refresh(Request())
            else:

                flow = InstalledAppFlow.from_client_secrets_file(self._credentials_file, app.config['SCOPES'])  # here enter the name of your downloaded JSON file
                creds = flow.run_local_server(port=0)

            with open('credentials/token.pickle', 'wb') as token:

                pickle.dump(creds, token)

        if creds:
            return creds
        else:
            cprint("RED", "[MySpreadSheet] ERROR creds is None")

    def get_spreadheets(self):
        try:
            service = build('sheets', 'v4', credentials=self._get_credentials())
        except Exception as ex:
            cprint("RED", "[get_spreadheets] Ex: {}".format(ex))
            PrintException(app.config['ERR_PTH'])

        return service.spreadsheets()

    def get_sheet_title(self):
        spreadsheets = self.get_spreadheets()
        spreadsheets_metadata = spreadsheets.get(spreadsheetId=self._spreadsheet_id).execute()

        sheets = spreadsheets_metadata.get('sheets', '')

        for sheet in sheets:
            title = sheet.get("properties", {}).get("title", "Not found")
            cprint("GREEN", "[get_sheet_title] title: " + title)
            self.sheet_title.append(title)

        return self.sheet_title

    def get_sheet_all_values(self):
        spreadsheets = self.get_spreadheets()
        titles = self.get_sheet_title()
        for title in titles:
            RANGE_NAME = "'{}'!{}".format(title, self.range)
            sheet_val = spreadsheets.values().get(spreadsheetId=self._spreadsheet_id, range=RANGE_NAME).execute()
            rows = sheet_val.get('values', [])
            cprint("GREEN", "TITLE: {} VALUES: {}".format(title, rows))
            self.spread_dict[title].append(rows)

        return self.spread_dict

    def get_sheet_values(self):
        spreadsheets = self.get_spreadheets()
        titles = self.get_sheet_title()

        RANGE_NAME = "'{}'!{}".format(titles[-1], self.range)
        sheet_val = spreadsheets.values().get(spreadsheetId=self._spreadsheet_id, range=RANGE_NAME).execute()
        rows = sheet_val.get('values', [])
        cprint("GREEN", "TITLE: {} VALUES: {}".format(titles[-1], rows))
        # self.spread_dict[title].append(rows)

        return rows

    def get_sheet_colors(self):
        spreadsheets = self.get_spreadheets()
        titles = self.get_sheet_title()
        RANGE_NAME = "'{}'!{}".format(titles[-1], self.range)

        spreadsheets_metadata = spreadsheets.get(spreadsheetId=self._spreadsheet_id, ranges=RANGE_NAME, includeGridData=True).execute()

        sheet = spreadsheets_metadata.get('sheets', '')
        # sheets[0].get('data')[0].get('rowData')[3].get('values')[1].get('formattedValue','Not found')

        return sheet

    def get_sheet_values_hard(self):
        spreadsheets = self.get_spreadheets()
        titles = self.get_sheet_title()
        RANGE_NAME = "'{}'!{}".format(titles[-1], self.range)

        spreadsheets_metadata = spreadsheets.get(spreadsheetId=self._spreadsheet_id, ranges=RANGE_NAME, includeGridData=True).execute()

        sheets = spreadsheets_metadata.get('sheets', '')
        rows = sheets[0].get('data')[0].get('rowData', [])

        # rows = json.dumps(json_rows)
        try:
            for row in rows:
                if row and row is not None:
                    for cell in row['values']:
                        if cell and cell is not None:
                            # print(cell)
                            # cprint("GREEN", "[get_sheet_values_hard] cell data: {}".format(cell['formattedValue']))
                            # cell.get(4'formattedValue', '')
                            # return rows
                            if cell.get('effectiveFormat').get('backgroundColor').get('red') is not None or cell.get('effectiveFormat').get('backgroundColor').get('green') is not None or cell.get('effectiveFormat').get('backgroundColor').get('blue') is not None:

                                if cell.get('effectiveFormat').get('backgroundColor').get('red') is None:
                                    red = 0
                                else:
                                    red = cell.get('effectiveFormat').get('backgroundColor').get('red')

                                if cell.get('effectiveFormat').get('backgroundColor').get('green') is None:
                                    green = 0
                                else:
                                    green = cell.get('effectiveFormat').get('backgroundColor').get('green')

                                if cell.get('effectiveFormat').get('backgroundColor').get('blue') is None:
                                    blue = 0
                                else:
                                    blue = cell.get('effectiveFormat').get('backgroundColor').get('blue')

                                backgroundColor = Color(red, green, blue).toHex()
                                cell['backgroundColor'] = backgroundColor
                            else:
                                backgroundColor = Color(1, 1, 1).toHex()
                                cell['backgroundColor'] = backgroundColor

                            if 'red' in cell.get('effectiveFormat').get('textFormat').get('foregroundColor') or 'green' in cell.get('effectiveFormat').get('textFormat').get('foregroundColor') or 'blue' in cell.get('effectiveFormat').get('textFormat').get('foregroundColor'):

                                if cell.get('effectiveFormat').get('textFormat').get('foregroundColor').get('red') is None:
                                    red = 0
                                else:
                                    red = cell.get('effectiveFormat').get('textFormat').get('foregroundColor').get('red')

                                if cell.get('effectiveFormat').get('textFormat').get('foregroundColor').get('green') is None:
                                    green = 0
                                else:
                                    green = cell.get('effectiveFormat').get('textFormat').get('foregroundColor').get('green')

                                if cell.get('effectiveFormat').get('textFormat').get('foregroundColor').get('blue') is None:
                                    blue = 0
                                else:
                                    blue = cell.get('effectiveFormat').get('textFormat').get('foregroundColor').get('blue')

                                foregroundColor = Color(red, green, blue).toHex()

                                cell['foregroundColor'] = foregroundColor
                            else:
                                foregroundColor = Color(0, 0, 0).toHex()
                                cell['foregroundColor'] = foregroundColor

                                # cprint("GREEN", "[get_sheet_values_hard] cell data: {}".format(cell.get('effectiveFormat').get('backgroundColor')))

                    # print()
        except Exception as ex:
            cprint("RED", "[get_sheet_values_hard] Ex: {}".format(ex))
            PrintException(app.config['ERR_PTH'])

        # sheets[0].get('data')[0].get('rowData')[3].get('values')[1].get('formattedValue','Not found')
        return rows


class Color(object):
    _FIELDS = ('red', 'green', 'blue', 'alpha')

    def __init__(self, red=None, green=None, blue=None, alpha=None):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def toHex(self):
        RR = format(int((self.red if self.red else 0) * 255), '02x')
        GG = format(int((self.green if self.green else 0) * 255), '02x')
        BB = format(int((self.blue if self.blue else 0) * 255), '02x')
        AA = format(int((self.alpha if self.alpha else 0) * 255), '02x')

        if self.alpha is not None:
            hexformat = '#{RR}{GG}{BB}{AA}'.format(RR=RR, GG=GG, BB=BB, AA=AA)
        else:
            hexformat = '#{RR}{GG}{BB}'.format(RR=RR, GG=GG, BB=BB)
        return hexformat
