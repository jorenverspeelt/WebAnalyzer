# -*- coding: utf-8 -*-
import os
from reader import Proposer
import sys


def readpath(path, output):
    userfiles = dict()
    for file in os.listdir(path):
        user = file.split("_")[0]
        if not user in userfiles.keys():
            userfiles[user] = []
        userfiles[user].append(file)
    with open(output, 'w+') as f:
        for user in userfiles.keys():
            if not len(userfiles[user]) == 0:
                    allrows = []
                    for file in userfiles[user]:
                        try:
                            iterrows = iter(open(path + "/"+file))
                            for row in iterrows:
                                if row.split(',')[1].replace("\"", "").strip() == "click":
                                    row = clean_file_row(row)
                                    print(row)
                                    # If an empty row (eg end of file) or JS link
                                    if not row and "javascript" not in row.lower():
                                        continue
                                    print(row)
                                    allrows.append(row)
                        except:  # If an import still fails, skip & keep count
                            print("Skipped file ", file)
                    datacut = round(len(allrows)/100*80)
                    proposer = Proposer(path, False)
                    for row in allrows[:datacut]:
                        try:
                            proposer.parseClick(row)
                        except:
                            print(file)
                            sys.exit()
                    totalscore = 0
                    for rowindex in range(0, len(allrows[datacut:])-1):
                        proposals = proposer.parse_action(allrows[rowindex], 5) 
                        if not proposals == None:
                            for i in range(0, len(proposals)):
                                if proposals[i] == allrows[rowindex+1].split(',')[3]:
                                    totalscore += len(proposals) - i
                                    break
                    totalscore /= (len(allrows) - datacut)    
                    f.write(user + " " + str(totalscore) + "\n" )     
            
def clean_file_row(input):
        """ Cleans the input string from double quotes, \n and whitespaces """
        input = input.rstrip()
        input = "".join(input.split())
        input = input.replace("\"", "")
        return input
        
        
readpath('./testdata/u1', './testingdata.txt')

 