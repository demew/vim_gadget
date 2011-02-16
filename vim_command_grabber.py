#!/usr/bin/python2.4
#
# Written 2007

__author__ = 'demew@there.ath.cx (Addie Beseda)'

""" Connects to the VimCommands/VimDates table and grabs today's command. """


from datetime import date

from mod_python import apache
import MySQLdb

#import vim_gadget_manipulator
# We have to handle this differently thanks to modpython!
vcg_path = '/home/demew/public_html/sandbox/python/'
vim_gadget_manipulator = apache.import_module('vim_gadget_manipulator',
                                              path=[vcg_path])

class GadgetGrabber(object):

  def __init__(self):
    """ Instantiates a GadgetGrabber object. """
    self.__db = MySQLdb.connect(user='demew-read', passwd='xxxxxx', db='xxxxxx')
    self.__db_cursor = self.__db.cursor() # Execute on the cursor
    self.today = date.today()
    self.__gu = vim_gadget_manipulator.GadgetUpdater()  

  def GrabTodaysCommand(self):
    """ Grabs the command associated with today from the db.
  
    Returns:
      Tuple containing two strings: first representing command, second
        representing the command description.
    """     
    sql = """
      SELECT c.command, c.descrip
      FROM VimCommands c
        INNER JOIN VimDates d
        USING (cid)
      WHERE d.ddate='%s'
    """ % self.today
    self.__db_cursor.execute(sql)
    results = self.__db_cursor.fetchone()
    if results:
      return results
    else:
      # Update the db contents and then call this function again
      self.__gu.AssignDates()
      self.GrabTodaysCommand()
 

if __name__ == '__main__':
  # Run the gadget grabber
  gg = GadgetGrabber()
  # Grab today's command
  gg.GrabTodaysCommand()

