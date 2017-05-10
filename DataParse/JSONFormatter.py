import json
import csv
import ast


def formatData():
    """
        A script to read in all output and convert to JSON data for input
        into d3.js, which is printed to standard output. 
    """
    diction = {}
    # Academic:
    openFile('output/Academic/English.txt', "English", "Academic \n Writing", diction)
    openFile('output/Academic/French.txt', "French", "Academic \n Writing", diction)
    openFile('output/Academic/German.txt', "German", "Academic \n Writing", diction)
    openFile('output/Academic/Portuguese.txt', "Portuguese", "Academic \n Writing", diction)
    openFile('output/Academic/Russian.txt', "Russian", "Academic \n Writing", diction)
    openFile('output/Academic/Spanish.txt', "Spanish", "Academic \n Writing", diction)
    openFile('output/Academic/Chinese.txt', "Chinese", "Academic \n Writing", diction)
    openFile('output/Academic/UserData.txt', "User Data", "Academic \n Writing", diction)

    openFile('output/InternetChats/English.txt', "English", "Internet Chat", diction)
    openFile('output/InternetChats/French.txt', "French", "Internet Chat", diction)
    openFile('output/InternetChats/German.txt', "German", "Internet Chat", diction)
    openFile('output/InternetChats/Portuguese.txt', "Portuguese", "Internet Chat", diction)
    openFile('output/InternetChats/Russian.txt', "Russian", "Internet Chat", diction)
    openFile('output/InternetChats/Spanish.txt', "Spanish", "Internet Chat", diction)
    openFile('output/InternetChats/Chinese.txt', "Chinese", "Internet Chat", diction)
    openFile('output/InternetChats/UserData.txt', "User Data", "Internet Chat", diction)

    print(json.dumps(diction))

def openFile(fileIn, language, formality, diction):
    """
        A helper function to read in file and traverse contained dictionary keys.
    """
    with open(fileIn, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        diction[formality + ";\n" + language[0].upper() + language[1:] + " Speaker"] = {}
        for row in spamreader:
            diction[formality + ";\n" + language[0].upper() + language[1:] + " Speaker"][row[0]] = ast.literal_eval(row[1])

formatData()
