# ---------------------------------
# Name: Egemen Engin
# ----------------------------------
import sys


def fillSteps(arrayOfMap, stepsStr, startingX, startingY):
    # -------------------------------
    # It changes array according to steps and it puts every point into list.
    # This is for ENGRAVE part because fit checker which check logo is in the boundaries will be used in engrave part.
    # -------------------------------
    tempFit = 1
    for step in stepsStr:

        if step == 'U':
            if (startingX - 1) < 0:
                tempFit = 0
                break
            startingX -= 1
            arrayOfMap[startingX][startingY] = "|"
            startingX -= 1

        elif step == 'D':
            if (startingX + 1) > 20:
                tempFit = 0
                break
            startingX += 1
            arrayOfMap[startingX][startingY] = "|"
            startingX += 1
        elif step == 'R':
            if (startingY + 1) > 20:
                tempFit = 0
                break
            startingY += 1
            arrayOfMap[startingX][startingY] = "-"
            startingY += 1
        elif step == 'L':
            if (startingY - 1) < 0:
                tempFit = 0
                break
            startingY -= 1
            arrayOfMap[startingX][startingY] = "-"
            startingY -= 1

    return tempFit


def fillStepsForSAME(arrayOfMap, stepsStr, startingX, startingY, listOfPoints):
    # -------------------------------
    # It changes array according to steps and it puts every point into list.
    # This is for SAME part because list of points are needed in there.
    # -------------------------------

    for step in stepsStr:
        listOfPoints.append((startingX, startingY))
        if step == 'U':

            startingX -= 1
            arrayOfMap[startingX][startingY] = "|"
            startingX -= 1

        elif step == 'D':

            startingX += 1
            arrayOfMap[startingX][startingY] = "|"
            startingX += 1
        elif step == 'R':

            startingY += 1
            arrayOfMap[startingX][startingY] = "-"
            startingY += 1
        elif step == 'L':

            startingY -= 1
            arrayOfMap[startingX][startingY] = "-"
            startingY -= 1
    listOfPoints.append((startingX, startingY))


def printMap(isFitted, arrayOfMap):
    # -------------------------------
    # It prints an array.
    # -------------------------------
    if isFitted:
        for row in range(totalRow):
            for column in range(totalColumn):
                sys.stdout.write(arrayOfMap[row][column])

            sys.stdout.write("\n")
    else:
        sys.stdout.write("LOGO OUT OF BOUNDS. TRY DIFFERENT COORDINATES TO START\n")


def clearArray(array, numberOfRow, numberOfColumns):
    # -------------------------------
    # It clear engraved array or it fills empty array with spaces and dots.
    # -------------------------------
    checker1 = 0
    checker2 = 0

    for row in range(numberOfRow):
        if checker1 == 0:
            for column in range(numberOfColumns):
                if checker2 == 0:
                    array[row][column] = "."
                    checker2 = 1
                else:
                    array[row][column] = " "
                    checker2 = 0
            checker1 = 1
        else:
            for column in range(numberOfColumns):
                array[row][column] = " "
            checker1 = 0
            checker2 = 0


def spinner(inputStr):
    # -------------------------------
    # It spin the inputStr 90 degree.
    # -------------------------------

    tempStr = ""
    for c in inputStr:
        if (c == "U"):
            tempStr = tempStr + "R"
        if (c == "D"):
            tempStr = tempStr + "L"
        if (c == "R"):
            tempStr = tempStr + "D"
        if (c == "L"):
            tempStr = tempStr + "U"
    return tempStr


def arrToString(arr, totRow, totColumn):
    # -------------------------------
    # It turn array to string.
    # -------------------------------
    strOfArr = ""
    for row in range(totRow):
        for column in range(totColumn):
            strOfArr = strOfArr + (arr[row][column])
        strOfArr = strOfArr + "\n"
    return strOfArr


if __name__ == '__main__':
    totalRow = 21
    totalColumn = 21

    allLogosDic = {}
    arr = [[" " for i in range(totalRow)] for j in range(totalColumn)]
    arr2 = [[" " for i in range(totalRow * 2)] for j in
            range(totalColumn * 2)]  # It is double of first array because in same part logos may not be engraved
    # and we do not know where this logo will fit in
    # so middle of the double array could hold  all possible logos.

    clearArray(arr, totalRow, totalColumn)  # clearArray is used to fill arrays with dots and spaces instead of clearing
    clearArray(arr2, totalRow * 2, totalColumn * 2)

    for line in sys.stdin:

        if 'exit' == line.strip():  # if input is equal to "exit"
            break
        else:
            operation = line.split(" ")
            # LOGO PART
            if operation[0].strip() == "LOGO":

                newLogoName = operation[1].strip()
                movements = operation[2].strip()
                if newLogoName in allLogosDic:
                    sys.stdout.write("This logo name has already been taken. Try another name.\n")
                    continue
                allLogosDic[newLogoName] = [movements, 10,
                                            10]  # add new key with logoName and  save movements into that.
                sys.stdout.write(newLogoName + " defined\n")


            # ENGRAVE PART
            elif operation[0].strip() == "ENGRAVE":
                logoName = operation[1].strip()
                if int(operation[2]) > 11 or int(operation[3]) > 11:  # it checks input coordinates in boundaries
                    sys.stdout.write("ERROR: THIS COORDINATES OUT OF BOUNDS\n")
                    continue
                if logoName not in allLogosDic:  # it checks is there any logo defined with logoName
                    sys.stdout.write("There is no logo whose name is " + logoName + ".\n")
                    continue
                x = int(operation[2].strip()) * 2 - 2  # to find right index in the 2d array
                y = int(operation[3].strip()) * 2 - 2  # to find right index in the 2d array

                allLogosDic[logoName][1] = x
                allLogosDic[logoName][2] = y
                steps = allLogosDic[logoName][0]  # every step of logo whose name is logoName

                isFitted = fillSteps(arr, steps, x, y)

                printMap(isFitted, arr)  # it prints engraved array or error message according to isFitted
                clearArray(arr, totalRow, totalColumn)  # it clears engraved array.

            # SAME PART
            elif operation[0].strip() == "SAME":

                isFitted2 = 1

                # Find logos informations.
                firstLogo = operation[1].strip()

                secondLogo = operation[2].strip()

                if firstLogo not in allLogosDic or secondLogo not in allLogosDic:  # check if there is logo with name is firstLogo or not
                    sys.stdout.write("One or both of the logo name is not defined!\n")

                else:
                    firstLogoMovements = allLogosDic[firstLogo][0]
                    firstLogoStartingX = allLogosDic[firstLogo][1]
                    firstLogoStartingY = allLogosDic[firstLogo][2]
                    arrayOfFirstLogoPoints = []

                    secondLogoMovements = allLogosDic[secondLogo][0]
                    secondLogoStartingX = allLogosDic[secondLogo][1]
                    secondLogoStartingY = allLogosDic[secondLogo][2]

                    fillStepsForSAME(arr2, firstLogoMovements, firstLogoStartingX * 2, firstLogoStartingY * 2,
                                     arrayOfFirstLogoPoints)
                    firstLogoOutput = arrToString(arr2, totalRow * 2,
                                                  totalColumn * 2)  # logo1 engraved array holds in string and it uses large array to avoid errors
                    # which may happen because it is not engraved.

                    clearArray(arr2, totalRow * 2, totalColumn * 2)  # clear large array to reuse

                    tempList = []
                    sameChecker = 0
                    tempString = secondLogoMovements
                    # At every point where the first logo passed,
                    # it draws the normal and rotated versions one by one of the second logo  and equals it to the string.
                    # If firstLogoOutput string and secondLogoOutput string is equal, it breaks and it prints "Yes".
                    # If they are not, it goes until end of the loops and print "No"
                    for point in arrayOfFirstLogoPoints:
                        tempString = secondLogoMovements
                        if sameChecker == 0:
                            i = 0
                            for i in range(4):
                                fillStepsForSAME(arr2, tempString, point[0], point[1], tempList)
                                secondLogoOutput = arrToString(arr2, totalRow * 2, totalColumn * 2)

                                if firstLogoOutput == secondLogoOutput:
                                    sameChecker = 1
                                    break
                                clearArray(arr2, totalRow * 2, totalColumn * 2)
                                tempString = spinner(tempString)
                        else:
                            break
                    if sameChecker == 1:
                        sys.stdout.write("Yes\n")
                    else:
                        sys.stdout.write("No\n")
                    clearArray(arr2, totalRow * 2, totalColumn * 2)

            else:
                sys.stdout.write("ERROR: Invalid operation.\n")


