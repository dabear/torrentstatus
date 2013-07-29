#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module exports a single class BearLang

"""
__all__ = ["BearLang"]
__version__ = "0.9b1"
__copyright__ = "Copyright 2013, Bjørn Inge Berg"
__license__ = "WTFPL"
__version__ = "1.0.1"
__maintainer__ = "Bjørn Inge Berg"
__email__ = "bjorninge-bearlang@bjorninge.no"
__status__ = "Production"
import shlex
import re
import pprint
import sys
__SHOULD_DEBUG_PRINT = False


def list_get(alist, index):
    """Shorthand function for returning a value from a list by index.

    Args:
        alist (list): A list
        index (Integer): An index number that does or does not exist in `l`

    Returns:
        String. If index exists, return alist[index] else return empty string
    """
    try:
        return alist[index]
    except IndexError:
        return ""


def list_has_val(alist, val):
    """Shorthand function for checking if a list has a value

    Args:
        l (list): A list
        val (String): a value to search for in `l`

    Returns:
        Bool. Whether or not value exists in `l`
    """
    #print("checking if list({0}) has value({1})".format(l,val))
    try:
        alist.index(val) 
        return True
    except ValueError:
        return False


def dprint(*args):
    """Debug prints all args, if debugging is on, else do nothing

    Args:
        *args: arguments to print to console when debugging is on.


    Returns:
        None
    """ 
    if not __SHOULD_DEBUG_PRINT:
        return
    for arg in args:
        pprint.pprint(arg)


class BearLang(object):
    """This BearLang class enables executing a line of code formatted in
the BearLang language and to match variables defined in the code argument
against"""

    def __init__(self, code, args):
        self.tokens = None
        self.args = args
        self.code = code
        self.results = []
        self.allowed_functions = [x.lstrip("_") for x in dir(self)
                                  if x.startswith("_")
                                  and not x.startswith("__")]

        self.commandset = None

    def _endswith(self, *args):
        """Returns true if arg0 is equal to arg1"""
        if len(args) is not 2:
            raise ValueError("endswith expects exactly 2 parameters")
        return args[0].endswith(args[1])

    def _notendswith(self, *args):
        """Returns true if arg0 does not end with arg1"""
        return not self._endswith(*args)

    def _contains(self, *args):
        """Returns true if arg1 is in arg0"""
        if len(args) is not 2:
            raise ValueError("contains expects exactly 2 parameters")
        return args[1] in args[0]
    
    def _notcontains(self, *args):
        """Returns true if arg1 is not in arg0"""
        return not self._contains(*args)
    
    def _startswith(self, *args):
        """Returns true if arg0 starts with arg1"""
        if len(args) is not 2:
            raise ValueError("startswith expects exactly 2 parameters")
        return args[0].startswith(args[1])
    def _notstartswith(self, *args):
        """Returns true if arg0 does not start with arg1"""
        return not self._startswith(*args)
    
    def _equals(self, *args):
        """Returns true if arg0 is equal to arg1"""
        if len(args) is not 2:
            raise ValueError("equals expects exactly 2 parameters")
        return args[0] == args[1]
    
    def _notequals(self, *args):
        """Returns true if arg0 is not equal to arg1"""
        return not self._equals(*args)
    
    def _matches(self, *args):
        """Returns true if arg0 is a regex match with regex in arg1"""
        if len(args) is not 2:
            raise ValueError("matches expects exactly 2 parameters")
        
        regex = re.compile(args[1])
        dprint("compiled arg1({0}) into p:{1}".format(args[1], regex))
        return regex.match(args[0]) is not None        
    
    def _notmatches(self, *args):
        """Returns true if arg0 is not a regex match with regex in arg1"""
        return not self._matches(*args)
  
    def _and(self, *args):
        """Dummy function. Always returns true"""
        if len(args) is not 0:
            raise ValueError("&& expects exactly 0 parameters")
        return True
    
    def tokenize(self):
        """Creates tokens and populates self.tokens based on `code`
        in constructor"""
        self.tokens = shlex.shlex(self.code, posix=True)
        self.tokens.whitespace += ","
        self.tokens = list(self.tokens)
        
    def parse(self):
        """Parses tokens and creates an a set of executable commands"""
        if not self.tokens:
            self.tokenize()
        #dprint("\nstarted parsing, allowed_functions is:{0}".
        #format(self.allowed_functions ))
        i = 0
        parts = []
        command_open = False
        part = False
        ltokens = self.tokens
        
        open_tags = 0
        
        
        for token in ltokens:
        
            i += 1
            if (list_has_val(self.allowed_functions, token) and
                not command_open and list_get(ltokens, i) == "("):
                
                parts.append({ 'command':{ "name": token, "args": [] } } )
                part = parts[-1]
                command_open = True
                continue 
          
          
            if command_open and (token == "(" or token == ")" ):
                if token == "(":
                    open_tags  += 1
                if token == ")":
                    open_tags  -= 1
              
                if open_tags == 0:
                    dprint("command is closing")
                    command_open = False
            elif command_open:
                part["command"]["args"].append( token)
                dprint("part::")
                dprint(part["command"]["args"])
            
            elif (not command_open and token == "&" and
                list_get(ltokens, i) == "&"):
                parts.append({ 'command':{ "name": "and", "args": [] } })
                part = parts[-1]
        self.commandset = parts 
        return parts  

    def execute(self):
        """Executes commands in self.commandset
        
        Populates self.results with the execution state (True/False)
        for every command in commandset. Only execute commands
        until one value is False (short-circut) or untill the end otherwise.
        """
        dprint("starting executing")
        if not self.commandset:
            self.parse()
        if not self.commandset:
            raise ValueError("Could not execute command. Make sure grammar and"
                             "test function names are correct: {0}"
                             .format(self.code))
            
        results = self.results = [] 
        for command in self.commandset:
            args = command["command"]["args"]
            #dprint("args[0] is {0}, self.args is".format( list_get(args, 0)) )
            #dprint( self.args )
            if list_get(args, 0) and self.args.get(args[0]):
                substitute = self.args.get(args[0], "")
                dprint("arg0 of command {0} matches a predefined variable,"
                       "substituting its value: {1}"
                       .format(command["command"]["name"], substitute))
                args[0] = substitute
                
            dprint("Executing command '{0}' with args: {1}"
                   .format( command["command"]["name"], args) )
            
            method = getattr(self, "_" + command["command"]["name"] )
            result = method(*args)
            results.append(result)
            
            if not result:
                return False
        dprint("Exiting, self.commandset was:{0}, code was:{1}, tokens was: {2}"
               .format(self.commandset, self.code, self.tokens ))
        return True
    

def main():
    """This shows a simple usage scenario"""
    
    code = "startswith(tracker, 'http') && equals(torrenttype, 'multi') &&" + \
            "matches(tracker, '^(http?)://tracker.sometracker.com' )"
    args = {"torrentstatus": "6", "torrenttype": "multi",
            "tracker": "http://tracker.sometracker.com:2710/a/1234567/announce"}
    print("starting parsing. code was:")
    pprint.pprint(code)
    print("args was:")
    pprint.pprint(args)
    
    parser = BearLang(code, args)
    
    print("parsed command is:")
    pprint.pprint(parser.parse())
    
    is_ok = False
    try:
        is_ok = parser.execute()
    except ValueError as err:
        is_ok = False
        print("{0}".format(err))
    
    print("command successfull? {0}".format(is_ok))
    print("result from parsed command:")
    pprint.pprint(parser.results)


if __name__ == '__main__':
    if "-debug" in sys.argv or "--debug" in sys.argv:
        __SHOULD_DEBUG_PRINT = True
    main()
   
    

    
    
    











