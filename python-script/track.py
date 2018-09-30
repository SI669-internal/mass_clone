import json
import datetime
from pathlib import Path

from script_settings import *

class Assignment():
    template_file_directory_path = Path(__file__).parent
    record_file_directory_path = DATA_FOLDER_PATH / 'records'

    due = None
    prefix = None
    submits = []

    def __init__(self, prefix, due='', full_points=''):
        self.prefix = prefix

        # retrieve from previous session or new 
        json_data = self.get_record_json_data()
        
        # override assignment attributes
        if due != '':
            json_data['due'] = due
        json_data['prefix'] = prefix
        if full_points != '':
            json_data['full_points'] = full_points

        # load into objects for runtime
        self.deserialize(json_data)

        # store object for next sesison
        self.save()

    def get_record_template_data(self):
        final_file_name = 'hw_record_template.json'
        template_file_path = self.template_file_directory_path / final_file_name
        with template_file_path.open(mode='r') as f:
            data = json.load(f)
        return data

    def get_record_file_path(self):
        final_file_name = f"record-{self.prefix}.json"
        return self.record_file_directory_path / final_file_name

    def get_record_json_data(self):
        json_data = None
        record_file_path = self.get_record_file_path()
        if record_file_path.exists():
            with record_file_path.open(mode='r') as f:
                json_data = json.load(f)
        else:
            json_data = self.get_record_template_data()
        
        return json_data
        
    def serialize(self):
        serialized_submits = []
        for submit in self.submits:
            serialized_submits.append(submit.serialize())
            # serialized_submits[ submit['student_name'] ] = submit.serialize()

        return {
            'prefix': self.prefix,
            'due': Serializer.serialize_time(self.due),
            'full_points': self.full_points,
            'submits': serialized_submits,
            'submits_count': len(self.submits)
        }
    
    def deserialize(self, json_data):
        self.prefix = json_data['prefix']
        self.due = Serializer.deserialize_time(json_data['due'])
        self.full_points = json_data['full_points']

        try_submits_json_data = json_data.get('submits', [])
        if try_submits_json_data != []:
            self.deserialize_submits(try_submits_json_data)
    
    def deserialize_submits(self, assignment_api_submit_data):
        for json_data in assignment_api_submit_data:
            submit = Submit(json_data=json_data)
            if submit.submitted_at and self.due:
                submit.late = submit.submitted_at > self.due
            else:
                submit.late = None

            # update existing entry
            is_replace = False
            for i, existing_submit in enumerate(self.submits):
                if json_data.get('student_name') == existing_submit.student_name:
                    self.submits[i] = submit
                    is_replace = True
            
            # if not exist, just add it
            if not is_replace:
                self.submits.append(submit)

    def save(self):
        record_file_path = self.get_record_file_path()
        with record_file_path.open(mode='w') as f:
            json.dump(self.serialize(), f, sort_keys=True, indent=4)
    
class Submit():

    def __init__(self, json_data=None):
        if json_data == None:
            self.clone_url = None
            self.submitted_at = None
            self.repo_name = None
            self.github_account = None
            self.student_name = None

            self.grade = None
            self.comment = None

            self.late = None
            self.late_delta = None
        else:
            self.deserialize(json_data)

    def deserialize(self, json_data):
        self.clone_url = json_data['clone_url']
        if 'submitted_at' in json_data:
            self.submitted_at = Serializer.deserialize_time(json_data.get('submitted_at', None))
        else:
            self.submitted_at = Serializer.deserialize_time(json_data.get('updated_at', None))

        self.repo_name = json_data['repo_name']
        self.github_account = json_data['github_account']
        self.student_name = json_data['student_name']

        self.grade = json_data.get('grade', None)
        self.comment = json_data.get('comment', None)

        self.late = json_data.get('late', None)
        self.late_delta = None

    def serialize(self):
        return {
            'clone_url': self.clone_url,
            'submitted_at': Serializer.serialize_time(self.submitted_at),
            'repo_name': self.repo_name,
            'late': self.late,
            'late_delta': None,  
            'github_account': self.github_account,
            'student_name': self.student_name,
            "grade": self.grade,
            "comment": self.comment
        }
    

class Serializer():

    def __init__(self):
        pass
    
    @staticmethod
    def deserialize_time(time_string):
        if not time_string:
            return None
        else:
            return datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
    
    @staticmethod
    def serialize_time(datetime_object):
        if not datetime_object:
            return None
        else:
            return datetime_object.strftime('%Y-%m-%dT%H:%M:%SZ')

if __name__ == "__main__":
    pass