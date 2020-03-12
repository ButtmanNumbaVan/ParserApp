import gspread
from oauth2client.service_account import ServiceAccountCredentials


class SpreadSheet:
    def __init__(self):
        self.spreadsheet_id = "1syTl113rlIufTgg5bR_zcDxu_3p_GqZUzBrx3do4TMQ"
        self.sheet_name = "kek"

        self._init_spread_sheet()

    def _init_spread_sheet(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('testing-api-82e1a3c7de92.json', scope)

        self.client = gspread.authorize(creds)
        self.sheet = self.client.open('testapi_data').sheet1

        self.ss = self.client.open_by_key(self.spreadsheet_id)
        self.sheet_id = self.ss.worksheet(self.sheet_name)._properties['sheetId']

    def merge_cells(self, rows_merge_range, column):
        start_row_index = rows_merge_range[0]
        end_row_index = rows_merge_range[1]

        start_column_index = 0
        end_column_index = column

        body = {
            "requests": [
                {
                    "mergeCells": {
                        "mergeType": "MERGE_COLUMNS",
                        "range": {
                            "sheetId": self.sheet_id,
                            "startRowIndex": start_row_index,
                            "endRowIndex": end_row_index,
                            "startColumnIndex": start_column_index,
                            "endColumnIndex": end_column_index
                        }
                    }
                }
            ]
        }

        self.ss.batch_update(body)

    def update_cell_value(self, cell, value):
        self.sheet.update_acell(cell, value)






