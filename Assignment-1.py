import sys
import string
import matplotlib.pyplot as plt

gridControl = {}
gridAsd = {}



#returns a dictionary
#keys: names of the segments (A,B,C...)
#values: coordinates of the segments
def prepareGrid():
    width = int(sys.argv[3].split("x")[0])  # width of the image
    height = int(sys.argv[3].split("x")[1])  # height of the image
    gridSegmentation = sys.argv[4]
    numberOfColumns = int(gridSegmentation[2])
    numberOfRows = int(gridSegmentation[0])
    if ((numberOfColumns or numberOfRows) < 2) or ((numberOfColumns or numberOfRows) > 4):
        print("Your columns or row won't bigger than 4 or less than 2")
        sys.argv[4] = input("ReEnter your RowxColumns:")
        gridSegmentation = sys.argv[4]
        numberOfColumns = int(gridSegmentation[2])
        numberOfRows = int(gridSegmentation[0])

    segments = {}

    # prepare a dictionary in the format:
    # {'A': [0,0,0], 'B': [0,0,0], ...}
    # a letter from the alphabet for each segment of the image
    for k in range(numberOfColumns * numberOfRows):
        segments[string.ascii_uppercase[k]] = [[], [], [], []]

    r = 0
    c = 0
    # segments dictionary's values hold coordinates of each corner of the segment
    for k in range(numberOfColumns * numberOfRows):
        segments[string.ascii_uppercase[k]] = [
            [(width / numberOfColumns) * r, (height / numberOfRows) * c],  # upper left coordinate of the segment
            [(width / numberOfColumns) * (r + 1), (height / numberOfRows) * c],  # upper right coordinate of the segment
            [(width / numberOfColumns) * r, (height / numberOfRows) * (c + 1)],  # lower left coordinate of the segment
            [(width / numberOfColumns) * (r + 1), (height / numberOfRows) * (c + 1)] # lower right coordinate of the segment
        ]
        r += 1
        if r == numberOfColumns:
            r = 0
            c += 1

    return segments


def createDictionary():
    analyzeASDFile()
    analyzeControlFile()
    mainDict = {}
    #taking both dict. into one dict.
    for gridVal in prepareGrid().values():
        if getKeyFromValue(gridVal) not in mainDict:
            if getKeyFromValue(gridVal) not in (gridAsd or gridControl):
                if getKeyFromValue(gridVal) not in (gridAsd and gridControl) :
                    mainDict[getKeyFromValue(gridVal)] = {"ASD": [0, 0, 0]}, {"Control": [0, 0, 0]}
                elif getKeyFromValue(gridVal) not in gridControl:
                    mainDict[getKeyFromValue(gridVal)] = gridAsd[getKeyFromValue(gridVal)], {"Control": [0, 0, 0]}
                else:
                    mainDict[getKeyFromValue(gridVal)] = {"ASD": [0, 0, 0]}, gridControl[getKeyFromValue(gridVal)]
            else:
                mainDict[getKeyFromValue(gridVal)] = gridAsd[getKeyFromValue(gridVal)],gridControl[getKeyFromValue(gridVal)]

    #print (mainDict)
    return mainDict

#fix this function accordingly with the control function
def analyzeASDFile():
    try:
        asdFile = open(sys.argv[1], "r")
    except:
        #print("File could not be opened")
        exit(1)

    asdFileLines = asdFile.readlines()
    i = 0
    peopleCount = 0
    for line in asdFileLines:
        line = line.split(",")
        line[3] = line[3][:len(line[3]) - 1]
        #print(line)
        #remove the first line of the text at the beginning of the program
        if i == 0:
            i += 1
            continue;
        #print(int(line[0]))
        #this list stores unique segments checked by a particular person
        if int(line[0]) == 0:
            fixedPointsByThatPerson = []
        #iterate through the coordinates of each segment
        for gridVal in prepareGrid().values():
            #check if the read value from the file is in that segment
            if int(line[1]) > gridVal[0][0] and int(line[1]) < gridVal[1][0]:
                if int(line[2]) > gridVal[0][1] and int(line[2]) < gridVal[2][1]:
                    #check if that segment was added to the dictionary
                    if getKeyFromValue(gridVal) in gridAsd:
                        # check if the person was already added to the dictionary
                        if getKeyFromValue(gridVal) not in fixedPointsByThatPerson:
                            gridAsd[getKeyFromValue(gridVal)]["ASD"][0] += 1
                            fixedPointsByThatPerson.append(getKeyFromValue(gridVal))
                        gridAsd[getKeyFromValue(gridVal)]["ASD"][1] += int(line[3])
                        gridAsd[getKeyFromValue(gridVal)]["ASD"][2] += 1
                        #print(gridAsd)
                    else:
                        gridAsd[getKeyFromValue(gridVal)] = {"ASD": [0, 0, 0]}
                        gridAsd[getKeyFromValue(gridVal)]["ASD"][1] += int(line[3])
                        gridAsd[getKeyFromValue(gridVal)]["ASD"][2] += 1
                        # check if the person already checked that segment
                        if getKeyFromValue(gridVal) not in fixedPointsByThatPerson:
                            gridAsd[getKeyFromValue(gridVal)]["ASD"][0] += 1
                            fixedPointsByThatPerson.append(getKeyFromValue(gridVal))
                        #print(gridAsd)
    #print(gridAsd)
    asdFile.close()


def analyzeControlFile():
    try:
        controlFile = open(sys.argv[2], "r")
    except:
        #print("File could not be opened")
        exit(1)

    controlFileLines = controlFile.readlines()
    i = 0
    peopleCount = 0
    for line in controlFileLines:
        # total number of people data is +3, fix that
        line = line.split(",")
        line[3] = line[3][:len(line[3]) - 1]
        #print(line)
        if i == 0:
            i += 1
            continue;
        #print(int(line[0]))
        #this list stores unique segments checked by a particular person
        if int(line[0]) == 0:
            fixedPointsByThatPerson = []

        # iterate through the coordinates of each segment
        for gridVal in prepareGrid().values():
            # check if the read value from the file is in that segment
            if int(line[1]) > gridVal[0][0] and int(line[1]) < gridVal[1][0]:
                if int(line[2]) > gridVal[0][1] and int(line[2]) < gridVal[2][1]:
                    # check if that segment was added to the dictionary
                    if getKeyFromValue(gridVal) in gridControl:
                        # check if the person already checked that segment
                        if getKeyFromValue(gridVal) not in fixedPointsByThatPerson:
                            gridControl[getKeyFromValue(gridVal)]["Control"][0] += 1
                            fixedPointsByThatPerson.append(getKeyFromValue(gridVal))
                        gridControl[getKeyFromValue(gridVal)]["Control"][1] += int(line[3])
                        gridControl[getKeyFromValue(gridVal)]["Control"][2] += 1
                        #print(fixedPointsByThatPerson)
                        #print(gridControl)

                        #print(getKeyFromValue(gridVal))

                    else:
                        gridControl[getKeyFromValue(gridVal)] = {"Control": [0, 0, 0]}
                        gridControl[getKeyFromValue(gridVal)]["Control"][1] += int(line[3])
                        gridControl[getKeyFromValue(gridVal)]["Control"][2] += 1
                        # check if the person already checked that segment
                        if getKeyFromValue(gridVal) not in fixedPointsByThatPerson:
                            gridControl[getKeyFromValue(gridVal)]["Control"][0] += 1
                            fixedPointsByThatPerson.append(getKeyFromValue(gridVal))
                        #print(fixedPointsByThatPerson)
                        #print(gridControl)

                        #print(getKeyFromValue(gridVal))

    #print(gridControl)
    #print(peopleCount)
    controlFile.close()


def getKeyFromValue(gridVal):
    for key, value in prepareGrid().items():
        if gridVal == value:
            return key

def makeChart(resultList, metric, elementName):
    groups = ["People with Autism", "People Without Autism"]
    values = resultList
    plt.bar(groups, values)
    plt.xlabel('Groups')
    if metric == 1:
        plt.ylabel("Total Number of People")
    elif metric == 2:
        plt.ylabel("Total Time Viewed")
    elif metric == 3:
        plt.ylabel("Total Number of Fixations")

    plt.title("Comparison Between People With & Without Autism\nfor Element {}".format(elementName))
    plt.show()

def compareWithElement(dict):
    metric = int(input("Enter the metric (Hint: Type 1 for the total number of people or 2 for the total time viewed,\n"
                       "or 3 for the total number of fixations) : "))
    element = str(input("Element Name:"))
    arrayAsd = []
    arrayControl = []
    sumOfArrayAsd = 0
    sumOfArrayControl = 0

    if element in dict:
        exportTuples = dict[element][0]
        arrayAsd = exportTuples["ASD"]
        exportTuples = dict[element][1]
        arrayControl = exportTuples["Control"]
    else:
        print("Element not found!!")

    #print(arrayAsd)
    #print(arrayControl)

    if metric == 1:#option 1 for total number of people
            sumOfArrayAsd += arrayAsd[0]

            sumOfArrayControl += arrayControl[0]

    elif metric == 2:#option 2 for total time viewed
            sumOfArrayAsd += arrayAsd[1]

            sumOfArrayControl += arrayControl[1]

    elif metric == 3:#option 3 for total number of fixations
            sumOfArrayAsd += arrayAsd[2]

            sumOfArrayControl += arrayControl[2]

    totalList = [sumOfArrayAsd, sumOfArrayControl]
    print(totalList)

    return totalList, metric, element

def compareWithoutElement(dict):
    metric = int(input("Enter the metric (Hint: Type 1 for the total number of people or 2 for the total time viewed,\n"
                       "or 3 for the total number of fixations) : "))
    arrayAsd = []
    arrayControl = []
    sumOfArrayAsd = 0
    sumOfArrayControl = 0

    for gridVal in prepareGrid().values():
        if getKeyFromValue(gridVal) in dict:
            exportTuples = dict[getKeyFromValue(gridVal)][0]
            arrayAsd.append(exportTuples["ASD"])
            exportTuples = dict[getKeyFromValue(gridVal)][1]
            arrayControl.append(exportTuples["Control"])
        else:
            print("Element not found!!")

    print(arrayAsd)
    print(arrayControl)

    if metric == 1:  # option 1 for total number of people
        for items_temp in arrayAsd:
                sumOfArrayAsd += items_temp[0]

        for items_temp in arrayControl:
                sumOfArrayControl += items_temp[0]

    elif metric == 2:  # option 2 for total time viewed
        for items_temp in arrayAsd:
                sumOfArrayAsd += items_temp[1]

        for items_temp in arrayControl:
                sumOfArrayControl += items_temp[1]

    elif metric == 3:  # option 3 for total number of fixations
        for items_temp in arrayAsd:
                sumOfArrayAsd += items_temp[2]

        for items_temp in arrayControl:
                sumOfArrayControl += items_temp[2]

    totalList = [sumOfArrayAsd, sumOfArrayControl]
    print(totalList)

    return totalList, metric




def menu(dict):
    option = int(
        input("1. Compare the total number of people, the total time viewed, and the total number of fixations\n"
              " for people with and without autism for a particular element on an image\n"
              "2. Compare the total number of people, the total time viewed, and the total number of fixations for\n"
              " people with and without autism on an image\n"
              "3. Exit\nChoose:"))

    while option != 3:
        if option == 1:
            totalList, metric, element = compareWithElement(dict)
            makeChart(totalList, metric, element)
        elif option == 2:
            totalList,metric = compareWithoutElement(dict)
            makeChart(totalList, metric, "All Elements")
        else:
            print("You typed wrong input please type it again\n")


        option = int(
            input("1. Compare the total number of people, the total time viewed, and the total number of fixations\n"
                  " for people with and without autism for a particular element on an image\n"
                  "2. Compare the total number of people, the total time viewed, and the total number of fixations for\n"
                  " people with and without autism on an image\n"
                  "3. Exit\nChoose:"))

        if option == 3:
            exit()



if __name__ == '__main__':

    dict = {}
    segmentsDict = prepareGrid()
    #print("----------------------")
    ##print(segmentsDict)
    dict = createDictionary()
    #print(dict)
    menu(dict)

