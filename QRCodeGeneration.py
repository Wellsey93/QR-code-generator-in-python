import numpy as np
from Encoder import Encoder
class qrCode():
    """
    qr code is always in byte mode
    max number of characters for V1 = 17
    max number of characters for V2 = 32
    number of error correction codewords for V1 = 19
    number of error correction codewords for V2 = 34

    V1 qrcode is 21x21
    V2 qrcode is 25x25
    using L level error correction (V1) = 152 bits
    using L level error correction (V2) = 272 bits

    Move on to generating the error codewords
    """
    def __init__(self):
        self.encoder = Encoder()
        self.size = 0
        self.qrCodeVersion = ""
      
        ###position pattern creation
        self.posPatternLength = 7
        self.posPattern = np.zeros([self.posPatternLength, self.posPatternLength], dtype = int)

        for x in range(self.posPatternLength):
            self.posPattern[0][x] = 1
            self.posPattern[self.posPatternLength - 1][x] = 1
            self.posPattern[x][0] = 1
            self.posPattern[x][self.posPatternLength - 1] = 1
        for x in range(self.posPatternLength - 4):
            self.posPattern[self.posPatternLength - 3][x + 2] = 1
            self.posPattern[self.posPatternLength - 4][x + 2] = 1
            self.posPattern[self.posPatternLength - 5][x + 2] = 1
        #########################################

        ## timing pattern initialisation
        self.timingPattern = []
        self.timingPatternLength = 0
        ######

        #####alignment pattern creation
        self.alignmentPatternLength = 5
        self.alignmentPattern = np.zeros([self.alignmentPatternLength, self.alignmentPatternLength], dtype = int)

        self.alignmentPattern[len(self.alignmentPattern) // 2][len(self.alignmentPattern) // 2] = 1
        for x in range(self.alignmentPatternLength):
            self.alignmentPattern[0][x] = 1
            self.alignmentPattern[self.alignmentPatternLength - 1][x] = 1
            self.alignmentPattern[x][0] = 1
            self.alignmentPattern[x][self.alignmentPatternLength - 1] = 1
        ################################################

    def createMatrix(self, input):
        self.matrix = np.zeros([self.size, self.size], dtype = int)
        self.matrix[self.size - 8][8] = 1
        self.applyPatterns()
        self.encoder.setText(input)
        self.encoder.InputEncoder(self.qrCodeVersion)


    def getMatrix(self):
        return self.matrix

    def setSize(self, givenSize):
        self.size = givenSize

    def setQrCodeVersion(self, givenVersion):
        self.qrCodeVersion = givenVersion

    def timingPatternCreation(self):
        self.timingPatternLength = self.size - 16
        for x in range(self.timingPatternLength):
            if x % 2 == 0:
                self.timingPattern.append(1)
            else:
                self.timingPattern.append(0)

    def applyAlignmentPattern(self, xpos, ypos):
        for x in range(self.alignmentPatternLength):
            for y in range(self.alignmentPatternLength):
                self.matrix[x + ypos][y + xpos] = self.alignmentPattern[x][y]


    def applyPositionPattern(self, ypos, xpos):
        for x in range(self.posPatternLength):
            for y in range(self.posPatternLength):
                if x + ypos <= len(self.matrix) or y + xpos <= len(self.matrix):
                    self.matrix[x + ypos][y + xpos] = self.posPattern[x][y]

    def timingPatternVertical(self, ypos, xpos):
        for x in range(self.timingPatternLength):
            self.matrix[x + ypos][xpos] = self.timingPattern[x]

    
    def timingPatternHorizontal(self, ypos, xpos):
        for x in range(self.timingPatternLength):
            self.matrix[ypos][x + xpos] = self.timingPattern[x]

    def applyPatterns(self):
        self.applyPositionPattern(0, 0)
        self.applyPositionPattern(self.size - 7, 0)
        self.applyPositionPattern(0, self.size - 7)
        self.timingPatternCreation()
        self.timingPatternVertical(8, 6)
        self.timingPatternHorizontal(6, 8)

        if self.qrCodeVersion == "V2":
            placement = self.size - self.posPatternLength
            self.applyAlignmentPattern(placement - 2, placement - 2)
