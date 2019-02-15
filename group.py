import pandas as pd
import sqlite3

class Group:

  def __init__(self, schedule=None, max_members=None):
      self.schedule = schedule
      self.max_members = max_members

      self.conn = sqlite3.connect('school.db')
      self.c = self.conn.cursor()

  def get_groups(self, group_id):
      # sql query
      sql = "SELECT * FROM groups WHERE id = {}".format(group_id)
      data = pd.read_sql(sql, self.conn)
      # Ouput info to terminal
      if data.shape[0] < 1: print("No existen grupos con ese id")
      else: print(data.to_string(index=False))
