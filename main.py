import tkinter as tk
from QRCodeGeneration import qrCode

class Win(tk.Frame):

    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self)
        self.qrCode = qrCode()
        self.master.title("Qr Code Generator")
        self.windowSize = 400
        self.pack(fill=tk.BOTH, expand=1)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.textBox = tk.Text(self.canvas, height=1, width=32, font=("Arial", 16), wrap=None)
        self.textButton = tk.Button(self.canvas, height=2, width=2, text="submit",font=("Arial", 10), command=lambda: self.submitText())
        self.Text()

    def submitText(self):
        input = self.textBox.get("1.0", tk.END)
        print(input)
        if input == "\n" or len(input) > 33:
            pass
        else:   
            if len(input) < 17:
                ## qrcode becomes version 1
                self.qrCode.setSize(21)
                self.qrCode.setQrCodeVersion("V1")
            else:
                ## qrcode becomes version 2
                self.qrCode.setSize(25)
                self.qrCode.setQrCodeVersion("V2")


            self.qrCode.createMatrix(input)
            self.textBox.destroy()
            self.textButton.destroy()
            self.displayCode()


    def Text(self):
        self.textBox.pack()
        self.textButton.pack()

    def displayCode(self):
        whiteCol = "white"
        blackCol = "black"
        rectangleX = 10
        rectangleY = 10
        width = 10
        height = 10
        for x in self.qrCode.getMatrix():
            for y in x:
                if y == 0:  
                    self.canvas.create_rectangle(rectangleX, rectangleY, rectangleX + width, rectangleY + height, outline=blackCol, fill=whiteCol)
                    rectangleX += 10
                if y == 1:
                    self.canvas.create_rectangle(rectangleX, rectangleY, rectangleX + width, rectangleY + height, outline=blackCol, fill=blackCol)
                    rectangleX += 10
            rectangleY += 10  
            rectangleX = 10


    def getWindowSize(self):
        return self.windowSize

def main():

    root = tk.Tk()
    ex = Win()
    root.geometry(str(ex.getWindowSize()) + "x" + str(ex.getWindowSize()))
    root.mainloop()


if __name__ == '__main__':
    main()
