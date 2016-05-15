# -*- coding: utf-8 -*-
import os
from reader import Proposer
import pandas as pd


def readpath(path, output, outputtype):
    userfiles = pd.Series()
    for file in os.listdir(path):
        user = file.split("_")[0]
        if user not in userfiles.keys():
            userfiles[user] = []
        userfiles[user].append(file)
        userfiles.sort_values(inplace=True)
    with open(output, outputtype) as f:
        for user in userfiles.keys():
            if len(userfiles[user]) == 0:
                continue
            allrows = []
            for file in userfiles[user]:
                try:
                    iterrows = iter(open(path + "/"+file))
                    for row in iterrows:
                        if row.split(',')[1].replace("\"", "").strip() == "click":
                            row = clean_file_row(row)
                            # If an empty row (eg end of file) or JS link
                            if not row and "javascript" not in row.lower():
                                continue
                            allrows.append(row)
                except:  # If an import still fails, skip & keep count
                    print("Skipped file ", file)
            # Cut 80% of the data
            datacut = round(len(allrows)/100*80)
            proposer = Proposer(path, False)
            for row in allrows[:datacut]:
                try:
                    proposer.parse_action(row)
                except:
                    print(file)
            # Use the last 20% of data to score the results based on the given
            # predictions towards the actual next website
            totalscore = 0
            for rowindex in range(0, len(allrows[datacut:])-1):
                proposals = proposer.parse_action(allrows[rowindex], False, 5)
                if proposals is not None:
                    for i in range(0, len(proposals)):
                        if proposals[i] == allrows[rowindex+1].split(',')[3]:
                            totalscore += (len(proposals) - i)
                            break
            totalscore /= (len(allrows) - datacut)
            f.write(user + " " + str(totalscore) + " " + str(len(allrows[datacut:])-1) + "\n" )     


def clean_file_row(input):
    """ Cleans the input string from double quotes, \n and whitespaces """
    input = input.rstrip()
    input = "".join(input.split())
    input = input.replace("\"", "")
    return input


def test_together():  
    """ This function will loop through all files and test the
    correctness of the proposer """
    readpath('./data', './results/alldata.txt', 'w+')


def test_seperately():
    """ This function will loop through the different users and test the
    correctness of the proposer """
    users = []
    for i in range(1, 28):
        users.append("u"+str(i))
    for user in users:
        readpath('./testdata/'+user, './results/seperate.txt', 'a')


test_together()  # Tests all files together
test_seperately()  # Test seperately per user
