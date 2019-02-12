class Admin(Teacher):

    def __init__(self, id, username, password, first_name, last_name):
            super().__init__(self, id, username, password, first_name, last_name)

    def manage_students(self, how, student_id):
        return

    def manage_subjects(self, how, subject_id):
        return

    def manage_groups(self, how, group_id):
        return

    def get_historical_records(self, students_id):
        return
