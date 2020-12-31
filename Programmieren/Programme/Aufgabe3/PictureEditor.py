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

import cv2

# Default size of the image
pixels_x = 500
pixels_y = 500

# Class to use the webcam
class MyVideoCapture:
   def __init__(self, video_source=0):
      # Open the video source
      self.vid = cv2.VideoCapture(video_source)
      self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, pixels_x)
      self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, pixels_y)
      if not self.vid.isOpened():
         raise ValueError("Unable to open video source", video_source)
      # Get video source width and height
      self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
      self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

   # Release the video source when the object is destroyed
   def __del__(self):
      if self.vid.isOpened():
         self.vid.release()

   def get_frame(self):
      if self.vid.isOpened():
         ret, frame = self.vid.read()
         if ret:
            # Return a boolean success flag and the current frame converted to BGR
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
         else:
            return (ret, None)
      else:
         return (ret, None)

# Class used to provide all the functions to manipulate the image
class ManipulateImage:
   def __init__(self):
      self.imgOrig = Image.new("1", (pixels_x,pixels_y))
      self.img = self.imgOrig
      self.cols, self.rows = self.imgOrig.size
      self.Sx = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]) #Sobel Matrix in x-Richtung
      self.Sy = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]]) #Sobel Matrix in y-Richtung
      self.result = np.zeros((3,3))

   # Function to open a new image
   def openImage(self, path_in):
      self.imgOrig = Image.open(path_in)
      self.img = self.imgOrig
      self.cols, self.rows = self.imgOrig.size

   # Function to update the image
   def updateImage(self, img):
      self.imgOrig = img
      self.img = img
      self.cols, self.rows = self.imgOrig.size

   # Function to reset the manipulated image to the default
   def resetImage(self):
      self.img = self.imgOrig

   # Binarizing the image with a threshold value
   def binarize(self, s):
      self.img = self.img.point(lambda x: 255 if x > s else 0)

   # Brigthening the image with a given value
   def brigther(self, p):
      self.img = self.img.point(lambda x: int(x + (p/100 * 255)))

   # Changing the gamma value of the image
   def gamma(self, g):
      if 0.0 <= g <= 10.0:
         self.img = self.img.point(lambda x: int(255* (x/255)**g))

   # Function to remove the noise of the image (improves edge detection)
   def removeNoise(self):
      self.img = self.img.filter(ImageFilter.BLUR)

   # Function to get a 3x3 subarray of the image needed for the edge detection
   # Returns 0 if the subarray is out of the image boundries
   def getSubArray(self, x, y, image, result):
      for i in np.arange(-1,2):
         for j in np.arange(-1,2):
            result[i+1][j+1] = image[y+i][x+j] if (x+j in range(0,image.shape[1])) and (y+i in range(0,image.shape[0])) else 0
      return result

   # Function to gather the edges of the image
   def edgeFilter(self):
      im = np.array(self.img.convert('L'))
      sobelGxGy = np.zeros_like(im)

      for y in np.arange(self.rows):
         for x in np.arange(self.cols):
            self.getSubArray(x,y,im, self.result)
            Gx = np.sum(np.multiply(self.result, self.Sx))
            Gy = np.sum(np.multiply(self.result, self.Sy))
            sobelGxGy[y][x] = np.sqrt(Gx**2 + Gy**2)
      self.img = Image.fromarray(sobelGxGy)

   # This function will also detect the edges in the images.
   # The function uses the advantage of linear separating the kernel and then using matrix multiplication.
   # The function is approx 1000 times faster than the combined for loops in the "slow" variant.
   def fastSobelEdgeFilter(self):
      im = np.array(self.img.convert('L')).astype(np.int16)
      sobelXStep = im[:,2:] - im[:,:-2]
      sobelX = sobelXStep[:-2] + sobelXStep[2:] + 2*sobelXStep[1:-1]
      sobelYStep = im[:,:-2] + im[:,2:] + 2*im[:,1:-1]
      sobelY = sobelYStep[2:] - sobelYStep[:-2]
      sobel = np.sqrt(np.square(sobelX, dtype=np.int64) + np.square(sobelY, dtype=np.int64))
      sobel_clip =  np.clip(sobel, 0, 255).astype(np.uint8)
      self.img = Image.fromarray(sobel_clip)

# TKinter app, MVVM approach (no data in the app itself, all data gets passed and processed in the data class MaipulateImage)
class App:
   # Default display of the app
   def __init__(self):
      self.root = tk.Tk()
      self.root.title("PictureEditor")

      self.delay = 20
      self.camEnable = tk.IntVar()
      self.sobelFilterEnable = tk.IntVar()

      self.manIp = ManipulateImage()
      self.vid = MyVideoCapture()

      self.filedialog = tk.Button(self.root, text="Open Image", command= self.openDialog)
      self.filedialog.grid(row=0, column=1)

      self.panel = tk.Canvas(self.root, width = self.vid.width, height = self.vid.height)
      self.panel.grid(row=0, column=0, rowspan=8)

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
      self.fastEdgeFilter = tk.Button(self.root, text="Filter edges (fast)", command=self.fastEdgeFilterFunc)
      self.fastEdgeFilter.grid(row=6, column=1)
      self.edgeFilter = tk.Button(self.root, text="Filter edges (slow (really slow))", command=self.edgeFilterFunc)
      self.edgeFilter.grid(row=7, column=1)

      self.webCamEnable = tk.Checkbutton(self.root, text="Enable Webcam stream", variable=self.camEnable, command=self.deactivateButtons)
      self.webCamEnable.grid(row=0, column=2)
      self.sobelEnable = tk.Checkbutton(self.root, text="Endable sobel edge filter on webcam stream", variable=self.sobelFilterEnable, state=tk.DISABLED)
      self.sobelEnable.grid(row=1, column=2)

      self.update()

      self.root.mainloop()

   # Callback functions
   def deactivateButtons(self):
      if(self.camEnable.get()):
         self.filedialog.config(state=tk.DISABLED)
         self.reset.config(state=tk.DISABLED)
         self.brightness.config(state=tk.DISABLED)
         self.gamma.config(state=tk.DISABLED)
         self.binarize.config(state=tk.DISABLED)
         self.removeNoise.config(state=tk.DISABLED)
         self.fastEdgeFilter.config(state=tk.DISABLED)
         self.edgeFilter.config(state=tk.DISABLED)
         self.sobelEnable.config(state=tk.NORMAL)
      else:
         self.filedialog.config(state=tk.NORMAL)
         self.reset.config(state=tk.NORMAL)
         self.brightness.config(state=tk.NORMAL)
         self.gamma.config(state=tk.NORMAL)
         self.binarize.config(state=tk.NORMAL)
         self.removeNoise.config(state=tk.NORMAL)
         self.fastEdgeFilter.config(state=tk.NORMAL)
         self.edgeFilter.config(state=tk.NORMAL)
         self.sobelEnable.config(state=tk.DISABLED)

   def resetScales(self):
      self.brightness.set('0')
      self.gamma.set('0')
      self.binarize.set('0')
   
   def edgeFilterFunc(self):
      self.manIp.edgeFilter()
      self.updatePicture()

   def fastEdgeFilterFunc(self):
      self.manIp.fastSobelEdgeFilter()
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
      self.resetScales()
      self.updatePicture()

   def openDialog(self):
      path = fd.askopenfilename(title = "Select image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
      if len(path) > 0:
         self.manIp.openImage(path)
         self.updatePicture()
      self.resetScales()

   def update(self):
      if(self.camEnable.get()):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()

         if ret:
            self.manIp.updateImage(Image.fromarray(frame))
            if(self.sobelFilterEnable.get()):
               self.manIp.fastSobelEdgeFilter()
            self.image = ImageTk.PhotoImage(image = self.manIp.img)
            self.panel.config(height=self.manIp.rows, width=self.manIp.cols)
            self.panel.create_image(0, 0, image = self.image, anchor = tk.NW)

      self.root.after(self.delay, self.update)

   def updatePicture(self):
      self.image = ImageTk.PhotoImage(self.manIp.img)
      self.panel.config(height=self.manIp.rows, width=self.manIp.cols)
      self.panel.create_image(0, 0, image = self.image, anchor = tk.NW)

# Mainloop
if __name__ == "__main__":
   app = App()
