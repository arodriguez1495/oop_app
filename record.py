from datetime import datetime
import pandas as pd
import sqlite3

class Record:

    def __init__(self, teacher_id, time_stamp=datetime.now()):
      self.teacher_id = teacher_id
      self.time_stamp = time_stamp

      self.conn = sqlite3.connect('school.db')
      self.c = self.conn.cursor()

    def get_records(self, grouped=False, export=False, print_=False):
        if export:
            filename  = 'records-{:%d-%m-%Y_%H-%M-%S}.xlsx'.format(self.time_stamp) # Create name for exported record
            writer = pd.ExcelWriter(filename, engine='xlsxwriter') # excel writer object
            print('Guardado en', filename)
        # Read tables from database
        subjects = pd.read_sql('SELECT * FROM subjects WHERE teacher_id = "{}"'.format(self.teacher_id), self.conn) # select specific teacher subjects
        students = pd.read_sql('SELECT * FROM students', self.conn) # select all students

        if subjects.shape[0] < 1: print('No se encontraron asignaturas')
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
                    print('Informacion de la asignatura:\n')
                    print(row[["course", "campus", "name", "semester", "group_id"]].to_string(index=False)) # Report subject info
                    print()
                    print('Notas:\n')
                    print(complete_grades.to_string(index=False))
                    print()

        if export: writer.save()

        if print_:
            if platform.system() == 'Windows': os.startfile(filename, 'print')
            else: print('Esta funcionalidad solo esta disponible en Sistemas Operativos Windows')

        return print('registros OK\n')
