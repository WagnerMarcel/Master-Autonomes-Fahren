# GUI for Simple Picture editor.
#  Simple Picture editor featuring a 
#     method to open a image,
#     binarize the image,
#     brigthen the image,
#     change the gamma on the image,
#     detect edges on the image.
#  Works with black/white and rgb pictures.
# Full reference: https://github.com/WagnerMarcel/Master-Autonomes-Fahren/tree/master/Programmieren/Programme/Aufgabe3/PictureEditor.py
# Author: Marcel Wagner
# Date: 08.11.2020

import tkinter as tk
import numpy as np
from tkinter import filedialog as fd
from PIL import ImageTk, ImageFilter, Image

pixels_x = 500
pixels_y = 500

#Todo's:
# - Edge Filter
# - Limit window size

class ManipulateImage:
   def __init__(self):
      self.imgOrig = Image.new("1", (pixels_x,pixels_y))
      self.img = self.imgOrig
      self.cols, self.rows = self.imgOrig.size
      self.Sx = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]) #Sobel Matrix in x-Richtung
      self.Sy = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]]) #Sobel Matrix in y-Richtung

   def openImage(self, path_in):
      self.imgOrig = Image.open(path_in)
      self.img = self.imgOrig
      self.cols, self.rows = self.imgOrig.size

   def resetImage(self):
      self.img = self.imgOrig

   def binarize(self, s):
      self.img = self.img.point(lambda x: 255 if x > s else 0)

   def brigther(self, p):
      self.img = self.img.point(lambda x: int(x + (p/100 * 255)))

   def gamma(self, g):
      if 0.0 <= g <= 10.0:
         self.img = self.img.point(lambda x: int(255* (x/255)**g))

   def removeNoise(self):
      self.img = self.img.filter(ImageFilter.BLUR)

   def getSubArray(self, x, y, image):
      result = np.zeros((3,3))
      for i in range(-1,2):
         for j in range(-1,2):
            result[i+1][j+1] = image[y+i][x+j] if (x+j in range(0,image.shape[1])) and (y+i in range(0,image.shape[0])) else 0
      return result

   def edgeFilter(self):
      im = np.array(self.img.convert('L'))
      sobelGxGy = np.zeros_like(im)
      
      for y in range(0, self.rows):
         for x in range(0, self.cols):
            subArray = self.getSubArray(x,y,im)
            Gx = np.sum(np.multiply(subArray, self.Sx))
            Gy = np.sum(np.multiply(subArray, self.Sy))
            sobelGxGy[y][x] = np.sqrt(Gx**2 + Gy**2)
      self.img = Image.fromarray(sobelGxGy)

class App:
   def __init__(self):
      self.root = tk.Tk()
      self.root.title("PictureEditor")
      self.manIp = ManipulateImage()
      self.filedialog = tk.Button(self.root, text="Open Image", command= self.openDialog)
      self.filedialog.grid(row=0, column=1)
      img = ImageTk.PhotoImage(self.manIp.img)
      self.panel = tk.Label(self.root, image = img)
      self.panel.grid(row=0, column=0, rowspan=7)
      self.reset = tk.Button(self.root, text="Reset Image", command=self.resetImage)
      self.reset.grid(row=1,column=1)
      self.brightness = tk.Scale(self.root, from_=-100, to=100, label="Brightness", orient=tk.HORIZONTAL)
      self.brightness.bind("<ButtonRelease-1>", self.brigtherFunc)
      self.brightness.grid(row=2, column=1)
      self.gamma = tk.Scale(self.root, from_=0, to=10.0, resolution=0.1, label="Gamma", orient=tk.HORIZONTAL)
      self.gamma.bind("<ButtonRelease-1>", self.gammaFunc)
      self.gamma.grid(row=3, column=1)
      self.binarize = tk.Scale(self.root, from_=0, to=255, label="Binarize", orient=tk.HORIZONTAL)
      self.binarize.bind("<ButtonRelease-1>", self.binarizeFunc)
      self.binarize.grid(row=4, column=1)
      self.removeNoise = tk.Button(self.root, text="Remove noise", command=self.removeNoiseFunc)
      self.removeNoise.grid(row=5, column=1)
      self.edgeFilter = tk.Button(self.root, text="Filter edges", command=self.edgeFilterFunc)
      self.edgeFilter.grid(row=6, column=1)
      self.root.mainloop()

   def resetScales(self):
      self.brightness.set('0')
      self.gamma.set('0')
      self.binarize.set('0')
   
   def edgeFilterFunc(self):
      self.manIp.edgeFilter()
      self.updatePicture()

   def removeNoiseFunc(self):
      self.manIp.removeNoise()
      self.updatePicture()

   def brigtherFunc(self, event):
      self.manIp.brigther(int(self.brightness.get()))
      self.updatePicture()

   def gammaFunc(self, event):
      self.manIp.gamma(float(self.gamma.get()))
      self.updatePicture()

   def binarizeFunc(self, event):
      self.manIp.binarize(int(self.binarize.get()))
      self.updatePicture()
   
   def resetImage(self):
      self.manIp.resetImage()
      self.updatePicture()

   def openDialog(self):
      path = fd.askopenfilename(title = "Select image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
      if len(path) > 0:
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
   