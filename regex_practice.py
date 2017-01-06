import re

def start_regex_check(): 
  cmd_input = raw_input("Check the if the following text contains 'start' and/or 'restart': ")
  start_match = re.search("start", cmd_input)
  if start_match:
    print "'" + cmd_input + "' " + "contains 'start'!"
    start_and_restart_match = re.match("^(re)?start$", cmd_input)
    if start_and_restart_match:
      print "'" + cmd_input + "' " + "matches 'start' or 'restart'!"
      exact_start_match = re.match("^start$", cmd_input)
      if exact_start_match:
        print "'" + cmd_input + "' " + "matches 'start' exactly!"
      else:
        print "'" + cmd_input + "' " + "matches 'restart' exactly!"
  else:
    print "'" + cmd_input + "' " + "does not contain 'start'!"


start_regex_check()
