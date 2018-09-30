class GithubUsePersonalRepo():

    def __init__(self, sheet_api):
        self.sheet_api = sheet_api
        self.student_names_order = self.sheet_api.student_names_order

    def get_personal_submits_data(self, prefix, sheet_range):
        raw_api_columns, raw_api_rows = self.sheet_api.get_raw_data_spreadsheet_api(sheet_range)
        
        repo_name_list = raw_api_rows[0]
        github_account_list = raw_api_rows[1]
        student_name_list = raw_api_rows[2]
        submits_data = {}
        for i in range(len(repo_name_list)):
            submits_data.update({
                student_name_list[i]: {
                    'github_account': github_account_list[i],
                    'repo_name': repo_name_list[i]
                }
            })
        
        normalized_submits_data = []
        for student_name in self.student_names_order:
            try:
                submit_data = submits_data[student_name]
                normalized_submits_data.append({
                    'clone_url': 'https://github.com/{}/{}'.format(submit_data['github_account'], submit_data['repo_name']),
                    # 'updated_at': '', # have to use github api .. just don't look at it
                    
                    # normalizing repo_name
                    'repo_name': '{}-{}-{}'.format(prefix,submit_data['repo_name'],submit_data['github_account']),
                    
                    'github_account': submit_data['github_account'],
                    'student_name': student_name
                })
            except KeyError:
                pass

        return normalized_submits_data

if __name__ == '__main__':
    pass