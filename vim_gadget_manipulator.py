#!/usr/bin/python2.4
#
# Written 2007

__author__ = 'demew@there.ath.cx (Addie Beseda)'

"""Abstracts interactions with the database containing vim commands.
   
   Knows what to do when you insert a new command into the database,
   and manipulates the data to fit my personal requirements.
"""


from datetime import date
from datetime import timedelta
import random
import sys

import MySQLdb


class GadgetUpdater(object):

  def __init__(self):
    """ Instantiates a GadgetUpdater object. """
    self.__db = MySQLdb.connect(user='demew', passwd='xxxxxx', db='xxxxxx')
    self.__db_cursor = self.__db.cursor() # Execute on the cursor
  
  def InsertCommand(self, cmd_text, cmd_descrip):
    """ Inserts a command into the VimCommands table.
  
    Args:
      cmd_text: string representing a vim command.
      cmd_descrip: string representing a description of what the command does.
    """     
    sql = """
      INSERT INTO VimCommands (command, descrip)
      VALUES ('%s', '%s')
    """ % (cmd_text, cmd_descrip)
    self.__db_cursor.execute(sql)
    # With a new command inserted, re-assign dates
    self.__AssignDates()

  def __AssignDates(self):
    """ Assigns a unique date to each command in the database. """
    # How many commands currently exist in the db?
    num_com = self.NumCommands()
    # Generate num_com unique dates starting with today.
    today = date.today()
    date_list = []
    for i in range(num_com):
      d = today + timedelta(days=i)
      date_list.append(d)
    random.shuffle(date_list)
    # Grab the commands that currently exist in the database
    sql = """
      SELECT cid
      FROM VimCommands
    """
    self.__db_cursor.execute(sql)
    results = self.__db_cursor.fetchall()
    cmd_date_pairs = []
    for i in range(num_com):
      cmd_date_pairs.append({'cid':str(results[i][0]), 
                             'ddate':str(date_list[i])})
    # Truncate old VimDates and add the new key-value pairs in
    sql = """
      TRUNCATE VimDates
    """
    self.__db_cursor.execute(sql)
    for date_pair in cmd_date_pairs:
      sql = """
        INSERT INTO VimDates (cid, ddate)
        VALUES('%s', '%s')
      """ % (date_pair['cid'], date_pair['ddate']) 
      self.__db_cursor.execute(sql)

  def AssignDates(self):
    self.__AssignDates()

  def NumCommands(self):
    """ Retrieves the number of commands currently in the db. 
    
    Returns:
      int representing the number of commands in the VimCommands table.

    """
    sql = """
      SELECT DISTINCT COUNT(cid) 
      FROM VimCommands
    """
    self.__db_cursor.execute(sql)
    result = self.__db_cursor.fetchone()
    return result[0]

  def LatestDate(self):
    """ Returns the command with the latest assigned date """
    sql = """
      SELECT ddate
      FROM VimDates
      ORDER BY ddate DESC
    """
    self.__db_cursor.execute(sql)
    result = self.__db_cursor.fetchone()
    return result[0]


if __name__ == '__main__':
  # Run the gadget updater
  gu = GadgetUpdater()
  # This is typically the case where we insert a new command
  args = sys.argv[1:]
  if args:
    if args[0] == 'insert' and len(args) == 3:
      command = args[1]
      descrip = args[2]
      try:
        gu.InsertCommand(command, descrip)
        print '%s : %s inserted successfully' % (command, descrip)       
      except Error:
        raise "Something went wrong with an insert"
    else:
      print ('Something is terribly wrong!  Your argument should have looked '
             'like vim_gadget_manipulator insert "command" "description"')
  else:
  # This is typically the case where we run from the cron
    today = date.today()
    if today >= gu.LatestDate():
      gu.AssignDates()

