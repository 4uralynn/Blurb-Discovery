#!/usr/bin/env python3

#This script will parse the files in a directory, looking for blurbs in sepecific language
#(currently/originally Russian) and will then create both a CSV and HTML file outlining the
#repeated blurbs of text within each document, how many files and lines each blurb is in,
#and which file the blurb is found in most often.
#This script expects that there is a directory named 'data' in the parent directory.
#If no argument is given, the script assumes the files to parse are in the 'data'
#directory. If an argument is given, the files in the given subdirectories will be parsed.

import os
import sys
import re
import subprocess
import csv
from csv_2_html import create
from alive_progress import alive_bar

#Function to open a file by type
def parse_dir(path, agent_list, linecount):
    success = 0
    linecount.append(0)
    for file in os.listdir(path):
        fullpath = os.path.join(path, file)
        csv_file = re.search(r"^.*\.csv$", file)
        pdf_file = re.search(r"\.pdf", file)
        if csv_file is not None:
            #print(file)
            linecount[0] += process_csv(file, fullpath, agent_list)
            success += 1
        yield 
    if success == 0:
        print("There are no files that can be processed.")
        sys.exit(1)
        return 1
    return 0

def process_csv(filename, path, agent_list):
    count = 0
    with open(path, 'r') as csvfile:
        for line in csvfile.readlines():
            count += 1
            results = re.findall(r"[\u0400-\u04FF ]*", line)
            for agent in results:
                if agent.strip() == "":
                    continue
                else:
                    if agent.lower().strip() not in agent_list:
                        agent_list[agent.lower().strip()] = {}
                    if agent.lower().strip() in agent_list:
                        if filename not in agent_list[agent.lower().strip()]:
                            agent_list[agent.lower().strip()][filename] = []
                        if filename in agent_list[agent.lower().strip()]:
                            agent_list[agent.lower().strip()][filename].append(count)
    csvfile.close()
    return count
                
def write_csv(agent_list):
    mostoccur = str

#    trans_limit = False

    with open('referenced.csv', "w", newline="") as newcsv:
        newcsv.write("Agency/Reference,Files,Lines,File with Highest Occurrences\n")
        for agent in agent_list:
            countfiles = 0
            countlines = 0
            mo_count = 0

#            final = agent
#            if not trans_limit:
#                final = blurb_translate(agent)
#                if final == agent:
#                    trans_limit = True

            newcsv.write(str(agent) + ",")      #for translation above algorthim, change 'agent' argument to 'final' 
            for filename in agent_list[agent]:
                countfiles += 1
                for index in agent_list[agent][filename]:
                    countlines += 1
                if mo_count < countlines:
                    mostoccur = filename
            newcsv.write(str(countfiles) + "," +  str(countlines) + "," + str(mostoccur) + "\n")
    newcsv.close()

#def blurb_translate(agent):

#    working = subprocess.check_output(["trans", "-brief", agent])
#    final = working.decode('UTF-8').strip()
#    if final == "":
#            return agent
#    else:
#        return final


def parsing_progress(targetpath, agent_list):
    linecount = []
    thing = len(os.listdir(targetpath))
    print("\nGoing through every file in the directory...\n")
    with alive_bar(thing) as bar:
        for nextfile in parse_dir(targetpath, agent_list, linecount):
            bar()
    print("\nPreparing CSV summary of blurbs from {} files, with {} lines in total.".format(str(thing), str(linecount[0])))
            
def sel_location():
    location = ""
    if len(sys.argv) < 2:
        pass
    else:
        location = sys.argv[1].strip("/")
    return location

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    targetpath = os.path.join(os.path.dirname(os.path.abspath("")), "data", sel_location())
    agent_list = {}
    parsing_progress(targetpath, agent_list)
    #print(agent_list.keys())
    #blurb_translate(agent_list)
    write_csv(agent_list)
    create('referenced.csv', 'referenced.html')
main()
