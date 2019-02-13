###### This code was used just for testing and debugging purposes ######

import pandas as pd
import sqlite3
import os

##################### MUST LOCATE THIS FUNCTION IN THE CORRECT CLASS
#
#def build_blank_record():
#    blank_head = pd.DataFrame(index=["Course", "Campus", "Nombre", "Semester", "Group"])
#    blank_grades = pd.DataFrame(columns=["ID","DNI","First Name","Last Name","Grade"])
#
#    writer = pd.ExcelWriter('example-record.xlsx', engine='xlsxwriter')
#    c.fetchall()
#    blank_head.to_excel(writer, sheet_name='Course1')
#    blank_grades.to_excel(writer, index=False, startrow=len(blank_head.index)+2, sheet_name='Course1')
#
#    writer.save()
##################### MUST LOCATE THIS FUNCTION IN THE CORRECT CLASS

conn = sqlite3.connect('school.db')
c = conn.cursor()

c.execute('SELECT * FROM admin_users')
c.fetchall()
c.execute('SELECT * FROM teachers')
c.fetchall()[3]

sql = ''' UPDATE grades SET grade = (SELECT t.grade
                                     FROM temp_grades AS t
                                     WHERE t.id == grades.student_id
                                     AND t.subject_id = grades.subject_id) '''

c.execute(sql)
c.fetchall()
conn.commit()

c.execute('PRAGMA table_info(temp_grades)')
c.fetchall()


c.execute('PRAGMA table_info(grades)')
c.fetchall()





grades = pd.read_sql('SELECT * FROM grades WHERE student_id = {}'.format(9), conn) # select specific student grades
subjects = pd.read_sql('SELECT * FROM subjects', conn) # select all subjects
students = pd.read_sql('SELECT * FROM students WHERE id = 9', conn) # select all students

print(students.to_string(index=False))

merged = pd.merge(grades, subjects, how='left', left_on='subject_id', right_on='id')
merged = pd.merge(merged, students, how='left', left_on='student_id', right_on='id')

merged.columns


print(merged[['semester', 'name', 'grade']].sort_values('semester').to_string(index=False))
