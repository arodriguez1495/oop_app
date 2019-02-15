import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import platform
from datetime import datetime
from matplotlib import style
import warnings
warnings.filterwarnings('ignore')
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

    def set_grades(self, subject_id, student_id, grade):
        sql = ''' UPDATE grades
                  SET grade = ?
                  WHERE subject_id = ?
                  AND student_id = ?'''

        self.c.execute(sql, (grade, subject_id, student_id))
        self.conn.commit()
        return print('nota actualizada')

    def add_student(self, subject_id, student_id):
        sql = '''INSERT INTO grades(student_id, subject_id)
                 VALUES (?, ?)'''
        self.c.execute(sql, (student_id, subject_id))
        self.conn.commit()
        return print('estudiante añadido a la asignatura')

    def remove_student(self, subject_id, student_id):
        sql = ''' DELETE FROM grades
                  WHERE subject_id = ?
                  AND student_id = ? '''
        self.c.execute(sql, (subject_id, student_id))
        self.conn.commit()
        return print('estudiante removido del acta')

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
        return print('notas actualizadas via archivo local')

    def get_student_info(self, student_id):
        student_dni = self.c.execute('SELECT dni FROM students WHERE id = {}'.format(student_id)).fetchall()[0][0]
        print('DNI del Alumno: ', student_dni, end='\n')

        g = pd.read_sql('SELECT * FROM grades', self.conn)
        s = pd.read_sql('SELECT * FROM subjects', self.conn)
        merged = pd.merge(g, s, how='left', left_on='subject_id', right_on='id')
        student_subjects = merged[merged['student_id']==student_id][['id','name']].drop_duplicates()
        if student_subjects.shape[0] < 1: print('No está matriculado en ninguna asignatura')
        else: print('Lista de Asignaturas: \n', student_subjects.to_string(index=False))

        return print('información del alumno OK')

    def get_statistics(self, group_id, subject_id):
        grades = pd.read_sql('SELECT * FROM grades WHERE subject_id = {}'.format(subject_id), self.conn)

        first_stats = pd.DataFrame()
        first_stats['Nota'] = grades['grade'].value_counts()
        first_stats['% sobre los presentes'] = grades['grade'].value_counts() / grades[~grades['grade'].isna()].shape[0]
        first_stats['% sobre el total'] = grades['grade'].value_counts() / grades.shape[0]

        if first_stats.shape[0] < 1: print('No hay notas disponibles para calcular estadísticas')
        else:
            print(first_stats.to_string(index=False))
            print('Promedio: ',round(grades['grade'].mean(),2))
            ranges = list(range(0, 21, 2))
            grades.groupby(pd.cut(grades['grade'], ranges)).count().plot.bar(y='grade')
            plt.show()

        return print('estadisticas OK')

    def get_students_subjects(self):
        s = pd.read_sql('SELECT * FROM intermediario', self.conn)
        for student_id in s['student_id'].unique():
            print('ID del Alumno:', student_id)
            print('ID de las Asignaturas: ', s[s['student_id'] == student_id]['subject_id'].values.tolist())
        return print('asignaturas del estudiante OK')
