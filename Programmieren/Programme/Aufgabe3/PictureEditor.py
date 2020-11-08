# GUI for Simple Picture editor.

import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

pixels_x = 500
pixels_y = 500

class ManipulateImage:
   def __init__(self):
      self.imgOrig = Image.new("1", (pixels_x,pixels_y))
      self.img = self.imgOrig
      self.cols, self.rows = self.imgOrig.size

   def openImage(self, path_in):
      self.imgOrig = Image.open(path_in)
      self.img = self.imgOrig
      self.cols, self.rows = self.imgOrig.size

   def binarize(self, s):
      for i in range(0,self.cols):
         for j in range(0,self.rows):
            value = 255 if self.imgOrig.getpixel((i, j)) > s else 0
            self.img.putpixel((i,j), value)

   def brigther(self, p):
      p = int(p)
      if -100 <= p <= 100:
         for i in range(0,self.cols):
            for j in range(0,self.rows):
               value = int(self.imgOrig.getpixel((i, j)) + (p/100 * 255))
               self.img.putpixel((i,j), value)

   def gamma(self, g):
      if 0.0 <= g <= 10.0:
         for i in range(0,self.cols):
            for j in range(0,self.rows):
               value = int(255 * (self.imgOrig.getpixel((i, j))/255)**g)
               self.img.putpixel((i,j), value)

class App:
   def __init__(self):
      self.root = tk.Tk()
      self.manIp = ManipulateImage()
      self.filedialog = tk.Button(self.root, text="Open Image", command= self.openDialog)
      self.filedialog.grid(row=0, column=1)
      img = ImageTk.PhotoImage(self.manIp.img)
      self.panel = tk.Label(self.root, image = img)
      self.panel.grid(row=0, column=0, rowspan=5)
      self.brightness = tk.Scale(self.root, from_=-100, to=100, label="Brightness", orient=tk.HORIZONTAL)
      self.brightness.bind("<ButtonRelease-1>", self.brigtherFunc)
      self.brightness.grid(row=1, column=1)
      self.gamma = tk.Scale(self.root, from_=0, to=10.0, label="Gamma", resolution=0.1, orient=tk.HORIZONTAL)
      self.gamma.bind("<ButtonRelease-1>", self.gammaFunc)
      self.gamma.grid(row=2, column=1)
      self.binarize = tk.Scale(self.root, from_=0, to=255, label="Binarize", orient=tk.HORIZONTAL)
      self.binarize.bind("<ButtonRelease-1>", self.binarizeFunc)
      self.binarize.grid(row=3, column=1)
      self.root.mainloop()

   def resetScales(self):
      self.brightness.set('0')
      self.gamma.set('0')
      self.binarize.set('0')

   def brigtherFunc(self, event):
      self.manIp.brigther(int(self.brightness.get()))
      self.updatePicture()

   def gammaFunc(self, event):
      self.manIp.gamma(float(self.gamma.get()))
      self.updatePicture()

   def binarizeFunc(self, event):
      self.manIp.binarize(int(self.binarize.get()))
      self.updatePicture()

   def openDialog(self):
      path = fd.askopenfilename()
      self.manIp.openImage(path)
      img = ImageTk.PhotoImage(self.manIp.img)
      self.panel.configure(image=img)
      self.panel.image=img
      self.resetScales()

   def updatePicture(self):
      img = ImageTk.PhotoImage(self.manIp.img)
      self.panel.configure(image=img)
      self.panel.image=img

if __name__ == "__main__":
   app = App()
   