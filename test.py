import pandas as pd
import sqlite3

df = pd.read_excel('example-record.xlsx', skiprows=7)

df

df.columns

df = pd.read_excel('example-record.xlsx', header=None, index_col=0, usecols=[0,1], nrows=5, skiprows=0).T

df
df['course'][1]

conn = sqlite3.connect('school.db')
c = conn.cursor()


c.fetchall()[0][0]

sql = '''SELECT subject_id, name
         FROM subjects, grades
         LEFT JOIN grades ON id = subject_id
         WHERE student_id = ?'''

student_subjects = c.execute(sql, (1)).fetchall()
c.execute('SELECT * FROM grades WHERE student_id = 1').fetchall()
c.execute()
c.fetchall()

sql = 'SELECT * FROM subjects WHERE teacher_id = 3'
pd.read_sql(sql, conn)


g['sdf'] = 7
g
g = pd.read_sql('SELECT * FROM grades', conn)
s = pd.read_sql('SELECT * FROM subjects', conn)
merged = pd.merge(g, s, how='left', left_on='subject_id', right_on='id')
merged.shape
merged[merged['student_id']==1][['id','name']].drop_duplicates()
g


data = c.execute('SELECT id, grade FROM temp_grades')
data.fetchall()
sql = ''' UPDATE grades AS f
          SET grade = t.grade
          FROM temp_grades AS t
          WHERE f.subject_id = t.subject_id
          AND f.student_id = t.id'''

c.execute(sql)
