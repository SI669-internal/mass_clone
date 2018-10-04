from utilities import *
import csv

def get_student_roster():
    roster_data_path = DATA_FOLDER_PATH / 'roster.csv'
    with roster_data_path.open(mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        pairs = None
        for row in csv_reader:
            if line_count == 0:
                pairs = row
            line_count += 1
    
    pairs.popitem(last=False)

    students = {}
    for github_account, student_name in pairs.items():
        students[github_account] = {
            'student_name': student_name
        }

    return students

if __name__ == "__main__":
    roster = get_student_roster()
    print(f"We have {len(roster)} students in roster.")