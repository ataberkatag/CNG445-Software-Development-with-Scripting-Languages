import sys
import os
import re
import matplotlib.pyplot as plt


def makeChart(resultList, metric, pageName, element="All Elements"):#makes chart based on metric
    groups = ["People with Autism", "People Without Autism"]
    values = resultList
    plt.bar(groups, values)
    plt.xlabel('Groups')
    #these if-else chain decides which option comes and written on a y label
    if metric == 1:
        plt.ylabel("Total Time Viewed")
    elif metric == 2:
        plt.ylabel("Total Number of Fixations")
    elif metric == 3:
        plt.ylabel("Total Number of Revisits")
    plt.title('Comparison Between People With & Without Autism\nfor {} on Page {}'.format(element,pageName))
    plt.show()


def compareWithoutElement(dict):#This func. takes dict. and compares the values with specific pagename
    metric = int(input("Enter the metric (Hint: Type 1 for The total time viewed or 2 for The total Fixaxions\n"
                       "or 3 for The total revisit) : "))
    pageName = str(input("Page Name: "))
    arrayAsd = []
    arrayControl = []
    sumOfArrayAsd = 0
    sumOfArrayControl = 0

    if pageName in dict:
        if "A" in dict[pageName]:
            arrayAsd.append(dict[pageName]["A"]["ASD"])
            arrayControl.append(dict[pageName]["A"]["CONTROL"])
        if "B" in dict[pageName]:
            arrayAsd.append(dict[pageName]["B"]["ASD"])
            arrayControl.append(dict[pageName]["B"]["CONTROL"])
        if "C" in dict[pageName]:
            arrayAsd.append(dict[pageName]["C"]["ASD"])
            arrayControl.append(dict[pageName]["C"]["CONTROL"])
        if "D" in dict[pageName]:
            arrayAsd.append(dict[pageName]["D"]["ASD"])
            arrayControl.append(dict[pageName]["D"]["CONTROL"])

    if metric == 1:#option 1 for total time viewed
        for items_temp in arrayAsd:
            for items in items_temp:
                sumOfArrayAsd += float(items[0])

        for items_temp in arrayControl:
            for items in items_temp:
                sumOfArrayControl += float(items[0])

    elif metric == 2:#option 2 for total fixations
        for items_temp in arrayAsd:
            for items in items_temp:
                sumOfArrayAsd += float(items[1])

        for items_temp in arrayControl:
            for items in items_temp:
                sumOfArrayControl += float(items[1])

    elif metric == 3:#option 3 for total revisist
        for items_temp in arrayAsd:
            for items in items_temp:
                sumOfArrayAsd += float(items[2])

        for items_temp in arrayControl:
            for items in items_temp:
                sumOfArrayControl += float(items[2])

    totalList = [sumOfArrayAsd, sumOfArrayControl]

    return totalList, metric, pageName


def compareWithElement(dict):#This func. takes dict. and compares the values with specific pagename and elementname
    metric = int(input("Enter the metric (Hint: Type 1 for the total time viewed or 2 for the total Fixaxions\n"
                       "or 3 for the total revisit) : "))
    element = str(input("Element Name: "))

    pageName = str(input("Page Name: "))
    arrayAsd = []
    arrayControl = []
    sumOfArrayAsd = 0
    sumOfArrayControl = 0

    if pageName in dict:
        if element in dict[pageName]:
            arrayAsd = dict[pageName][element]["ASD"]
            arrayControl = dict[pageName][element]["CONTROL"]
        else:
            print("Element not found!")
    else:
        print("Page name not found!")

    if metric == 1:#option 1 for total time viewed
        for items in arrayAsd:
            sumOfArrayAsd += float(items[0])

        for items in arrayControl:
            sumOfArrayControl += float(items[0])

    elif metric == 2:#option 2 for total fixations
        for items in arrayAsd:
            sumOfArrayAsd += float(items[1])

        for items in arrayControl:
            sumOfArrayControl += float(items[1])

    elif metric == 3:#option 3 for total revisist
        for items in arrayAsd:
            sumOfArrayAsd += float(items[2])

        for items in arrayControl:
            sumOfArrayControl += float(items[2])

    totalList = [sumOfArrayAsd, sumOfArrayControl]

    return totalList, metric, pageName, element

def fileProcess(dataFile):
    pageNames = {}
    elementNames = {}
    userGroups = {}
    dict = {}

    try:
        file = open(pathToDataFile, "r")  # Opening a file in read mod

        for lines in file:  # for loop which traverse inside the file line by line

            lines = lines.replace("\n", "")
            lineArray = lines.split(";")
            # In here we are saving the all keys in to the arrays
            pageName = lineArray[0]
            elementName = lineArray[1]
            userGroup = lineArray[4]
            # In here we are saving the all values in to the arrays
            timeViewed = lineArray[5]
            fixations = lineArray[6]
            revisits = lineArray[7]

            # ..

            if pageName not in dict:  # Creating a dictinory with stored pageName
                dict[pageName] = {}

            if elementName not in dict[pageName]:  # Creating a dictinory with stored elementName inside the pageName dict.
                dict[pageName][elementName] = {}

            if userGroup not in dict[pageName][elementName]:  # Creating a dictinory with stored userGroups inside the our dict.
                dict[pageName][elementName][userGroup] = []

            dict[pageName][elementName][userGroup].append([timeViewed, fixations, revisits])  # final append for usergroup's
            # values

    except IOError:
        print("File could not be opened!")
        exit(1)

    return dict

def menu(dict):
    option = int(
        input("1. Compare the total time viewed, the total number of fixations or the total number of revisits for\n"
              " people with and without autism for a particular element on a specific web page\n"
              "2. Compare the total time viewed, the total number of fixations or the total number of revisits for\n"
              " people with and without autism on a specific web page\n"
              "3. Exit\nChoose:"))

    while option != 3:#menu
        if option == 1:
            resultList, metric, pageNamee, element = compareWithElement(dict)#Taking results and metric option for Compare with
            makeChart(resultList, metric,pageNamee,element)                #Pagename and ElementName
        elif option == 2:
            resultList, metric, pageNamee = compareWithoutElement(dict)#Taking results and metric option for Compare
            makeChart(resultList, metric,pageNamee)                   #Without ElementName
        else:
            print("You typed wrong input please type it again\n")

        option = int(
            input(
                "1. Compare the total time viewed, the total number of fixations or the total number of revisits for\n"
                " people with and without autism for a particular element on a specific web page\n"
                "2. Compare the total time viewed, the total number of fixations or the total number of revisits for\n"
                " people with and without autism on a specific web page\n"
                "3. Exit\nChoose:"))

        if option == 3:
            exit()


#main function
if __name__ == '__main__':
    pathToDataFile = sys.argv[1]#Taking data from commandLine
    dict=fileProcess(pathToDataFile)
    menu(dict)

