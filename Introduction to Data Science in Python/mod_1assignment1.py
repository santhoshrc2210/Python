#Part A
#Find a list of all of all of the names in the following string using regex.
import re
def names():
    simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
    Ruth and Peter, their parents, have 3 kids."""

    return re.findall("[A-Z]\w*", simple_string)
    raise NotImplementedError()
print(names())

#Part B
#The dataset file in assets/grades.txt contains a line separated list of people with their grade in a class. 
#Create a regex to generate a list of just those students who received a B in the course.
# format example: Ronald Mayr: A
import re
def grades():
    with open ("assets/grades.txt", "r") as file:
        grades = file.read()
        list_B_grades = []
        for item in re.finditer("(\w* \w*): ([A-Z])", grades):
            if item.group(2) == 'B':
                list_B_grades.append(item.group(1))
    return list_B_grades
    # YOUR CODE HERE
    raise NotImplementedError()
print(grades())

#Part C
#Consider the standard web log file in assets/logdata.txt. This file records the access a user makes when visiting a web page (like this one!). 
#Each line of the log has the following items:

#a host (e.g., '146.204.224.152')
#a user_name (e.g., 'feest6811' note: sometimes the user name is missing! In this case, use '-' as the value for the username.)
#the time a request was made (e.g., '21/Jun/2019:15:45:24 -0700')
#the post request type (e.g., 'POST /incentivize HTTP/1.1' note: not everything is a POST!)
#Your task is to convert this into a list of dictionaries, where each dictionary looks like the following:

#example_dict = {"host":"146.204.224.152", 
#                "user_name":"feest6811", 
#                "time":"21/Jun/2019:15:45:24 -0700",
#                "request":"POST /incentivize HTTP/1.1"}

#format example: 146.204.224.152 - feest6811 [21/Jun/2019:15:45:24 -0700] "POST /incentivize HTTP/1.1" 302 4622

import re
def logs():
    with open("assets/logdata.txt", "r") as file:
        logdata = file.read()
        log_frmt_list = []
        pattern="""
        (?P<host>.*\..*\..*\..*)  #some of the numbers are strings type
        (\s-\s)
        (?P<user_name>.*)          #some rows have user name as -
        (\s\[)
        (?P<time>.*)
        (\])
        (\s")
        (?P<request>.*)
        (")
        """
        #count = 0
        for item in re.finditer(pattern,logdata,re.VERBOSE):
            #count+=1
            #print(item.groupdict(), count)
            log_frmt_list.append(item.groupdict())
    return log_frmt_list                   
    # YOUR CODE HERE
    raise NotImplementedError()
#print(len(logs()))













