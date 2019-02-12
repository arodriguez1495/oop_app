import pandas as pd
import sqlite3

conn = sqlite3.connect('school.db')
c = conn.cursor()

sql = ''' UPDATE grades AS g
          SET g.grade = t.grade
          WHERE g.subject_id IN (SELECT t.subject_id FROM temp_grades AS t)
          AND g.student_id IN (SELECT t.id FROM temp_grades AS t) '''

data = c.execute(sql)
data.fetchall()

c.execute('PRAGMA table_info(temp_grades)')
c.fetchall()
