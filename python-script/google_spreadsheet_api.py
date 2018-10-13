from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import json
from pathlib import Path

from utilities import *

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# Google Spreadsheet API Setup: https://developers.google.com/sheets/api/quickstart/python

class SheetAPI():

    def __init__(self, spreadsheet_id, sheet_tab_name):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_tab_name = sheet_tab_name
        self.service = self.get_service()
        self.raw_api_columns, self.raw_api_rows = self.get_raw_data_spreadsheet_api(f'{self.sheet_tab_name}!A4:AH')
        self.student_names_order = self.get_student_name_order_spreadsheet()

    def get_service(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        return service

    def get_raw_data_spreadsheet_api(self, range):
        data_range = range
        service = self.service
        
        result = service.spreadsheets().values().get( # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet
            spreadsheetId=self.spreadsheet_id,
            range=data_range,
            majorDimension='COLUMNS'
        ).execute()
        raw_api_columns = result.get('values', [])

        result = service.spreadsheets().values().get( # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet
            spreadsheetId=self.spreadsheet_id,
            range=data_range,
            majorDimension='ROWS'
        ).execute()
        raw_api_rows = result.get('values', [])

        return (raw_api_columns, raw_api_rows)
    
    def get_student_names(self):
        row_fields = self.raw_api_rows[1]
        return row_fields[3:]
    
    def get_github_accounts(self):
        row_fields = self.raw_api_rows[0]
        return row_fields[3:]

    def get_student_name_order_spreadsheet(self):
        student_names = self.get_student_names()
        student_names_order_position = {}
        for i, student_name in enumerate(student_names):
            student_names_order_position[student_name] = i
        return student_names_order_position

    def write_data_to_spreadsheet(self, service, rows_data=[]):
        # clean data
        try:
            body = {
                'requests': [
                    {
                        'insertDimension': {
                                'range': {
                                'dimension': "ROWS",
                                'start_index': 5,
                                'end_index': 99
                            },
                            "inheritFromBefore": False
                        }
                    },
                    {
                        'deleteDimension': {
                            'range': {
                                'dimension': 'ROWS',
                                'start_index': 99
                            }
                        }
                    },
                ]
            }
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body).execute()
        except Exception as e:
            print(f'ERROR: failed to clean sheet: {e}')
        
        # write data
        body = { # https://developers.google.com/sheets/api/guides/values#writing_to_a_single_range
            'data': [
                row_data for row_data in rows_data
                # {
                #     'range': 'main!A6:C13',
                #     'values': [[ '' for i in range(24) ]]
                # }
            ],
            'valueInputOption': 'RAW'
        }
        result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=self.spreadsheet_id, body=body).execute()
        print('INFO: {} cells updated.'.format(result.get('totalUpdatedCells')))

    def load_all_records(self, service):
        records_path = DATA_FOLDER_PATH / 'records'
        records_files_path_collect = records_path.glob('record-*.json')
        record_files_path_sorted = []
        for file_path in records_files_path_collect:
            record_files_path_sorted.append(file_path)
        record_files_path_sorted.sort()
        
        assignment_list = []
        for file_path in record_files_path_sorted:
            with file_path.open(mode='r') as f:
                json_data = json.load(f)

                # indexing for student name
                json_data['submits_by_student_name'] = {}
                for submit in json_data.get('submits'):
                    json_data['submits_by_student_name'][submit['student_name']] = submit
                
                # normalizing (order, mapping)
                json_data['submits_by_student_name_normalized'] = {}
                json_data['submits_not_exist'] = [] # name in sheet, but no repo (yet) or not yet downloaded
                json_data['submits_not_in_sheet'] = {} # repo created and downloaded, but not in sheet's roster
                for student_name in self.student_names_order:
                    if student_name in json_data['submits_by_student_name']:
                        json_data['submits_by_student_name_normalized'][student_name] = json_data['submits_by_student_name'][student_name]
                        json_data['submits_by_student_name'].pop(student_name)
                    else:
                        json_data['submits_by_student_name_normalized'][student_name] = { 'student_name': student_name }
                        json_data['submits_not_exist'].append(student_name)
                json_data['submits_not_in_sheet'] = [ '{}/{}'.format(submit['student_name'], submit['github_account']) for submit in json_data['submits_by_student_name'] ]

                assignment_list.append(json_data)
        
        for assignment in assignment_list:
            print('INFO: Loaded assignment: {}, {} submits.'.format(
                assignment['prefix'],
                len(assignment['submits'])
            ))
        print(f'INFO: Loaded {len(assignment_list)} assignments in total.')
        
        return assignment_list

    def retrieve_fields(self, assignment, fields):
        retrieved_fields = {}
        for field in fields:
            retrieved_fields[field] = []

        for student_name, submit in assignment['submits_by_student_name_normalized'].items():
            for field in fields:
                try:
                    retrieved_fields[field].append(submit[field])
                except:
                    retrieved_fields[field].append('Not exist')
        
        return retrieved_fields

    def push_submit_field_row_data(self, rows_data, row_meta, r, field):
        row_data = r[field]
        prepend_data = []
        if field == 'grade':
            prepend_data = [ row_meta['full_points'], row_meta['assignment_prefix'] ]
        else:
            prepend_data = ['', '']

        rows_data.append({
            'range': '{}!A{}'.format(self.sheet_tab_name, row_meta['number']),
            'values': [
                prepend_data + [field] + row_data
            ]
        })

        row_meta['number'] += 1

    def push_assignment_row_data(self, rows_data, assignment, row_meta, field):
        rows_data.append({
            'range': '{}!A{}'.format(self.sheet_tab_name, row_meta['number']),
            'values': [
                [ '', '', field ] + assignment[field]
            ]
        })

        row_meta['number'] += 1

    def generate_rows_data_for_all_records(self, service):
        assignment_list = self.load_all_records(service)

        _rows_data = []
        _row_meta = {
            'number': 6,
            'assignment_prefix': None,
            'full_points': None
        }

        for assignment in assignment_list:
            _row_meta['assignment_prefix'] = assignment['prefix']
            _row_meta['full_points'] = assignment['full_points']
            
            row_submit_fields_display = ['grade', 'comment']
            r = self.retrieve_fields(assignment, row_submit_fields_display)
            for field_display in row_submit_fields_display:
                self.push_submit_field_row_data(_rows_data, _row_meta, r, field_display)
            
            row_assignment_fields_display = ['submits_not_exist', 'submits_not_in_sheet']
            for field_display in row_assignment_fields_display:
                self.push_assignment_row_data(_rows_data, assignment, _row_meta, field_display)
        
        return _rows_data

    def upload_all_records(self):
        rows_data = self.generate_rows_data_for_all_records(self.service)

        print('INFO: Uploading all records...')
        self.write_data_to_spreadsheet(self.service, rows_data)

if __name__ == '__main__':
    sheet_api = SheetAPI()
    sheet_api.upload_all_records()