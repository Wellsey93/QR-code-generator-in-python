import numpy as np
import reedsolo

class Encoder():

    def __init__(self):
        self.userInput = ""
        self.bytes = ""
        self.userInputSize = 0
        self.bitCharacters = 0
        

    def setText(self, userInput):
        self.userInput = userInput
        self.userInputSize = len(self.userInput) - 1

    def addPadBytes(self, charSize):
        paddingBytes = [" 11101100", " 00010001"]
        paddingIndex = 0

        while self.bitCharacters < charSize:
            self.bytes += paddingBytes[paddingIndex]
            paddingIndex = (paddingIndex + 1) % 2
            self.bitCharacters += 1


    def InputEncoder(self, QRCodeVersion):
        self.hexToBinary = {"0": "0000","1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110", "7": "0111",
                "8": "1000", "9": "1001", "a": "1010", "b": "1011", "c": "1100", "d": "1101", "e": "1110",
                "f": "1111"}  
        utfEncoding = str(self.userInput.encode("utf-8"))
        lengthOfText = np.binary_repr(self.userInputSize)

        ## adds trailing zeros to lengthOfText so it is 8 bits long
        while len(lengthOfText) < 8:
            lengthOfText = "0" + lengthOfText

        """
        For the creation of the variable binary (seen below)
        creates the initial binary string with 0100 = byte form.
        then an 8 bit string is included (lengthOfText) that displays the overall length of chars the input has 
        """

        self.bytes = f"0100 {lengthOfText} "
        for x in utfEncoding[2:-3]:
            hextochar = hex(ord(x))
            for y in hextochar[2:]:
                self.bytes += self.hexToBinary[y]
            self.bytes += " "
            self.bitCharacters += 1

        self.bytes += "0000"

        if QRCodeVersion == "V1":
            self.addPadBytes(17)
        
        if QRCodeVersion == "V2":
            self.addPadBytes(32)

        print(self.bytes)



    






