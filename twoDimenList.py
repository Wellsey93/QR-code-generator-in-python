import numpy as np

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
        self.size = 0
        self.text = ""
        self.textSize = 0
        self.qrCodeVersion = ""
        self.qrCodeVersionDict = {"V1": 152, "V2": 272}
        self.hexToBinary = {"0": "0000","1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110", "7": "0111",
                             "8": "1000", "9": "1001", "a": "1010", "b": "1011", "c": "1100", "d": "1101", "e": "1110",
                             "f": "1111"}        

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

    def createMatrix(self):
        self.matrix = np.zeros([self.size, self.size], dtype = int)
        self.matrix[self.size - 8][8] = 1

    def getMatrix(self):
        return self.matrix

    def setSize(self, givenSize):
        self.size = givenSize

    def setText(self, givenText):
        self.text = givenText

    def getText(self):
        return self.text
    
    def setTextSize(self):
        self.textSize = len(self.text) - 1
        print("text size:")
        print(self.textSize)

    def setQrCodeVersion(self, givenVersion):
        self.qrCodeVersion = givenVersion

    def createCharacterCount(self):
        return np.binary_repr(self.textSize)


    def textBitConverion(self):
        utfEncoding = str(self.text.encode("utf-8"))
        lengthOfText = self.createCharacterCount()
        bitCharacters = 0
        ## adds trailing zeros to lengthOfText so it is 8 bits long
        while len(lengthOfText) < 8:
            lengthOfText = "0" + lengthOfText
        """
        For the creation of the variable binary (seen below)

        creates the initial binary string with 0100 = byte form.

        then an 8 bit string is included (lengthOfText) that displays the overall length of chars the input has 
        """
        binary = f"0100 {lengthOfText} "
        for x in utfEncoding[2:-3]:
            hextochar = hex(ord(x))
            for y in hextochar[2:]:
                binary += self.hexToBinary[y]
            binary += " "
            bitCharacters += 1

        binary += "0000"
        
        if self.qrCodeVersion == "V1":
            while bitCharacters < 17:
                binary += " 00000000"
                bitCharacters += 1
        elif self.qrCodeVersion == "V2":
            while bitCharacters < 32:
                binary += " 00000000"
                bitCharacters += 1
        else:
            raise Exception("qr code version not defined")

        self.setText(binary)

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
        self.timingPatternVertical(8, 6)
        self.timingPatternHorizontal(6, 8)

        if self.qrCodeVersion == "V2":
            placement = self.size - self.posPatternLength
            self.applyAlignmentPattern(placement - 2, placement - 2)
