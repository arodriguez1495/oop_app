import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import style
style.use("fivethirtyeight")

class Teacher:

    def __init__(self, id, username, password, first_name, last_name):
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

        # Open database connection and cursor
        self.conn = sqlite3.connect('school.db')
        self.c = self.conn.cursor()

    def get_student_info(self, student_id):
        student_dni = self.c.execute('SELECT dni FROM students WHERE id = {}'.format(student_id)).fetchall()[0]
        print('Student DNI: ', student_dni)
        student_subjects = self.c.execute('SELECT id, name FROM subjects WHERE student_id = {}'.format(student_id)).fetchall()
        print('Student Subjects:\n', student_subjects)
        return print('------------END-------------')

    def get_statistics(self, group_id, subject_id):
        grades = pd.read_sql('SELECT * FROM grades WHERE ')
        ### FUNCTION STILL ON WORK ###

# def get_records(self):
#     '''The teacher receives the blank minutes of the subjects he is
#        responsible for.'''
#
#     # Read tables from database
#     subjects = pd.read_sql('SELECT * FROM subjects WHERE teacher_id = "{}"'.format(id), self.conn) # select specific teacher subjects
#     students = pd.read_sql('SELECT * FROM students', self.conn) # select all students
#
#     # Create or open an excel file
#     writer = pd.ExcelWriter('records_{%d-%m-%Y}.xlsx'.format(datetime.now()), engine='xlsxwriter')
#
#     for i, row in subjects.iterrows():
#         # Report header
#         row[["course", "campus", "name", "semester", "group_id"]].to_excel(writer, header=False, sheet_name=row['name'])
#
#         # Report grades
#         grades = pd.read_sql('SELECT * FROM grades WHERE subject_id = {}'.format(row['id']), self.conn) # select specific subjects grades
#
#         complete_grades = pd.merge(grades, students, how='left', left_on='student_id', right_on='id') # Add student id and dni columns
#         complete_grades = complete_grades[["id","dni","first_name","last_name","grade"]] # select columns that are going to be in the report
#         complete_grades.to_excel(writer, index=False, startrow=7, sheet_name=row['name']) # make the report in excel
#
#     writer.save() # save changes in the excel file
#     return 'records exported in records_{%d-%m-%Y}.xlsx file'

    def get_records(self):
        '''The teacher receives the blank minutes of the subjects he is
           responsible for.'''

        # Read tables from database
        subjects = pd.read_sql('SELECT * FROM subjects WHERE teacher_id = "{}"'.format(id), self.conn) # select specific teacher subjects
        students = pd.read_sql('SELECT * FROM students', self.conn) # select all students

        for i, row in subjects.iterrows():
            # Report subject info
            print(row[["course", "campus", "name", "semester", "group_id"]])
            # Report grades
            grades = pd.read_sql('SELECT * FROM grades WHERE subject_id = {}'.format(row['id']), self.conn) # select specific subjects grades
            complete_grades = pd.merge(grades, students, how='left', left_on='student_id', right_on='id') # Add student id and dni columns
            complete_grades = complete_grades[["id","dni","first_name","last_name","grade"]] # select columns that are going to be in the report
            print(complete_grades)

        return

    def get_records():
        return

    def set_grades():
        return
    def add_student():
        return

    def remove_student():
        return

    def export_records():
        return

    def import_records():
        return

    def print_records():
        return

a = Teacher(id=2423, username='rer', password='re', first_name='rere', last_name='rere')
type(a) == Teacher
