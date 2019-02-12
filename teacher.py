import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
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

    def get_records(self, grouped=False, export=False, print=False):
        '''The teacher receives the blank minutes of the subjects he is
           responsible for.'''

        if export:
            filename  = '{}-records-{:%d-%m-%Y--%h-%m-%s}.xlsx'.format(self.username,datetime.now())
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            print('Saved at', filename)
        # Read tables from database
        subjects = pd.read_sql('SELECT * FROM subjects WHERE teacher_id = "{}"'.format(self.id), self.conn) # select specific teacher subjects
        students = pd.read_sql('SELECT * FROM students', self.conn) # select all students

        if subjects.shape[0] < 1: print('No subject found')
        else:
            for i, row in subjects.iterrows():
                # Report grades
                grades = pd.read_sql('SELECT * FROM grades WHERE subject_id = {}'.format(row['id']), self.conn) # select specific subjects grades
                complete_grades = pd.merge(grades, students, how='left', left_on='student_id', right_on='id') # Add student id and dni columns
                complete_grades = complete_grades[["id","dni","first_name","last_name","grade"]] # select columns that are going to be in the report

                if export:
                    row[["course", "campus", "name", "semester", "group_id"]].to_excel(writer, header=False, sheet_name=row['name']) # Report subject info
                    complete_grades.to_excel(writer, index=False, startrow=7, sheet_name=row['name']) # make the report in excel
                else:
                    print('Subject Information:\n')
                    print(row[["course", "campus", "name", "semester", "group_id"]]) # Report subject info
                    print()
                    print('Grades:\n')
                    print(complete_grades)
                    print()

        if export: writer.save()

        if print:
            if platform.system() == 'Windows': os.startfile(filename, 'print')
            else: print('This functionallity its only available in Windows OS')

        return print('records printed\n')

    def set_grades(self, subject_id, student_id, grade):
        sql = ''' UPDATE grades
                  SET grade = ?
                  WHERE subject_id = ?
                  AND student_id = ?'''

        self.c.execute(sql, (grade, subject_id, student_id))
        self.conn.commit()
        return print('grade updated')

    def add_student(self, subject_id, student_id):
        sql = '''INSERT INTO grades(student_id, subject_id)
                 VALUES (?, ?)'''
        self.c.execute(sql, (student_id, subject_id))
        self.c.commit()
        return print('student added to subject')

    def remove_student(self, subject_id, student_id):
        sql = ''' DELETE FROM grades
                  WHERE subject_id = ?
                  AND student_id = ? '''
        self.c.execute(sql, (subject_id, student_id))
        self.c.commit()
        return print('student removed from record')

    def import_records(self, path_to_file, grouped=False):
        header = pd.read_excel(path_to_file, header=None, index_col=0, usecols=[0,1], nrows=5, skiprows=0).T
        self.c.execute('SELECT id FROM subjects WHERE name = "{}"'.format(header.iloc[0,2]))
        subject_id = self.c.fetchall()[0][0]

        grades = pd.read_excel(path_to_file, skiprows=7)
        grades['subject_id'] = subject_id
        grades.to_sql('temp_grades', self.conn, if_exists='replace')

        sql = ''' UPDATE grades SET grade = (SELECT t.grade
                                             FROM temp_grades AS t
                                             WHERE t.id == grades.student_id
                                             AND t.subject_id = grades.subject_id) '''

        self.c.execute(sql)
        self.conn.commit()
        return print('grades updated via file')

    def print_records(self, grouped=False):
        if platform.system() == 'Windows': os.startfile('~/Downloads/arts_grades.xlsx', 'print')
        else: print('This functionallity its only available in Windows OS')
        return

    def get_student_info(self, student_id):
        student_dni = self.c.execute('SELECT dni FROM students WHERE id = {}'.format(student_id)).fetchall()[0][0]
        print('Student DNI: ', student_dni, end='\n')

        g = pd.read_sql('SELECT * FROM grades', self.conn)
        s = pd.read_sql('SELECT * FROM subjects', self.conn)
        merged = pd.merge(g, s, how='left', left_on='subject_id', right_on='id')
        student_subjects = merged[merged['student_id']==1][['id','name']].drop_duplicates()
        print('List of subjects: ')
        print('Subject      Subject\n', student_subjects.to_string(index=False))

        return print('Student information printed')

    def get_statistics(self, group_id, subject_id):
        grades = pd.read_sql('SELECT * FROM grades WHERE subject_id = {}'.format(subject_id), self.conn)

        first_stats = pd.DataFrame()
        first_stats['Number'] = grades['grade'].value_counts()
        first_stats['% over presents'] = grades['grade'].value_counts() / grades[~grades['grade'].isna()].shape[0]
        first_stats['% over total'] = grades['grade'].value_counts() / grades[~grades['grade'].isna()].shape[0]
        print(first_stats)

        print('Promedio: ', grades['grade'].mean())

        ranges = list(range(0, 21, 2))
        grades.groupby(pd.cut(grades['grade'], ranges)).count().plot.bar(y='grade')
        plt.show()

        return print('statistics showed')
