
#REDUNDANT CODE, USED IN THE BEGINNNING OF THE DEVELOPMENT


# import numpy as np

# def positionPattern(largeList, xpos, ypos):
#     length = 7 
#     posPattern = np.zeros([length, length], dtype = int)

#     for x in range(length):
#         posPattern[0][x] = 1
#         posPattern[length - 1][x] = 1
#         posPattern[x][0] = 1
#         posPattern[x][length - 1] = 1

#     for x in range(length - 4):
#         posPattern[length - 3][x + 2] = 1
#         posPattern[length - 4][x + 2] = 1
#         posPattern[length - 5][x + 2] = 1

#     for x in range(length):
#         for y in range(length):
#             if x + ypos <= len(largeList) or y + xpos <= len(largeList):
#                 largeList[x + ypos][y + xpos] = posPattern[x][y]
        

# def timingPattern(largeList, xpos, ypos, patternLength, direction):
#     tPattern = []
#     for x in range(patternLength):
#         if x % 2 == 0:
#             tPattern.append(1)
#         else:
#             tPattern.append(0)

#     if direction == "vertical":
#         for x in range(patternLength):
#             largeList[x + ypos][xpos] = tPattern[x]

#     elif direction == "horizontal":
#         for x in range(patternLength):
#             largeList[ypos][x + xpos] = tPattern[x]

# def analyseInput(givenInput):
#     for x in givenInput:
#         pass


# def alignmentPattern():
#     pass



# def formatString(errorCorrection, bitMask):
#     pass

# def versionOneCode(largeList, size):
#     largeList[size - 8][8] = 1
#     positionPattern(largeList, 0, 0)
#     positionPattern(largeList, size - 7, 0)
#     positionPattern(largeList, 0, size - 7)
#     timingPattern(largeList, 6, 8, 5, "vertical")
#     timingPattern(largeList, 8, 6, 5, "horizontal")
#     print(largeList)
