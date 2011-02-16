#!/usr/bin/python2.4
#
# Written 2007

# mod_python handler for vim commands

from mod_python import apache

vcg_path = '/home/demew/public_html/sandbox/python/'
vim_command_grabber = apache.import_module('vim_command_grabber',
                                           path=[vcg_path])

class GadgetModPy(object):
  
  def __init__(self):
    """ Instantiates a GadgetModPy object. """
    self.__gg = vim_command_grabber.GadgetGrabber()

  def GrabCommand(self):
    """ Grabs the command from the gadget grabber.

      Returns: tuple of two strings: (command, description).
    """
    return self.__gg.GrabTodaysCommand()

def index(req):
  gmp = GadgetModPy()
  s = """ \
        <html>
        <body>
        Today's Vim Command!<br />
        %s : %s
        </body>
        </html>
      """
  s %= gmp.GrabCommand()
  return s


