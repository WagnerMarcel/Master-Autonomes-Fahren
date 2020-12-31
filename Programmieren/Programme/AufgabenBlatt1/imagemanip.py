import sys
import PIL.Image as Image
import numpy as np

def binarize(s):
   for i in range(0,cols):
      for j in range(0,rows):
         value = 255 if img.getpixel((i, j)) > s else 0
         img.putpixel((i,j), value)


def brigther(p):
   if -100 <= p <= 100:
      for i in range(0,cols):
         for j in range(0,rows):
            value = int(img.getpixel((i, j)) + (p/100 * 255))
            img.putpixel((i,j), value)

def gamma(g):
   if 0.0 <= g <= 10.0:
       for i in range(0,cols):
         for j in range(0,rows):
            value = int(255 * (img.getpixel((i, j))/255)**g)
            img.putpixel((i,j), value)

Sx = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]) #Sobel Matrix in x-Richtung
Sy = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]]) #Sobel Matrix in y-Richtung

def getSubArray(x,y, image):
   result = np.zeros((3,3))
   if y-1 < 0 and y+1 < image.shape[0]:
      if x-1 >= 0 and x+1 < image.shape[1]:
         result = image[0:y+1][x-1:x+1]
      elif x-1 < 0 and x+1 < image.shape[1]:
         result = image[0:y+1][0:x+1]
      elif x-1 >= 0 and x+1 >= image.shape[1]:
         result = image[0:y+1][x-1:image.shape[1]-1]
   elif y-1 >= 0 and y+1 >= image.shape[0]:
      if x-1 >= 0 and x+1 < image.shape[1]:
         result = image[y-1:image.shape[0]-1][x-1:x+1]
      elif x-1 < 0 and x+1 < image.shape[1]:
         result = image[y-1:image.shape[0]-1][0:x+1]
      elif x-1 >= 0 and x+1 >= image.shape[1]:
         result = image[y-1:image.shape[0]-1][x-1:image.shape[1]-1]
   elif y-1 >= 0 and y+1 < image.shape[0] and x-1 >= 0 and x+1 < image.shape[1]:
      result = image[y-1:y+1][x-1:x+1]
   for i in range(-1,2):
      for j in range(-1,2):
         result[i+1][j+1] = image[y+i][x+j] if (x+j in range(0,image.shape[1])) and (y+i in range(0,image.shape[0])) else 0
   return result

def edgeFilter():
   im = np.array(img.convert('L'))
   #im = img
   sobelGxGy = np.zeros_like(im)
   sobelGx = np.zeros_like(im)
   sobelGy = np.zeros_like(im)
   
   for y in range(0,rows):
      for x in range(0, cols):
         subArray = getSubArray(x,y,im)
         Gx = np.sum(np.multiply(subArray, Sx))
         Gy = np.sum(np.multiply(subArray, Sy))
         sobelGx[y][x] = Gx
         sobelGy[y][x] = Gy
         sobelGxGy[y][x] = np.sqrt(Gx**2 + Gy**2)
   imageGx = Image.fromarray(sobelGx)
   imageGy = Image.fromarray(sobelGy)
   imageGxGy = Image.fromarray(sobelGxGy)
   imageGxGy.show()
   imageGx.show()
   imageGy.show()

def fastEdgeFilter():
   im = np.array(img.convert('L')).astype(np.int16)
   sobelXStep = im[:,2:] - im[:,:-2]
   sobelX = sobelXStep[:-2] + sobelXStep[2:] + 2*sobelXStep[1:-1]
   sobelYStep = im[:,:-2] + im[:,2:] + 2*im[:,1:-1]
   sobelY = sobelYStep[2:] - sobelYStep[:-2]
   sobel = np.sqrt(np.square(sobelX, dtype=np.int64) + np.square(sobelY, dtype=np.int64))
   sobel_clip =  np.clip(sobel, 0, 255).astype(np.uint8)
   imageSobelX = Image.fromarray(sobelX)
   imageSobelY = Image.fromarray(sobelY)
   imageSobel = Image.fromarray(sobel_clip)
   imageSobelX.show(title="SobelX")
   imageSobelY.show(title="SobelY")
   imageSobel.show(title="Sobel")

path_in = sys.argv[3] if len(sys.argv) > 3 else '/Users/Marcel/Documents/Master-Autonomes-Fahren/Programmieren/Programme/AufgabenBlatt1/Camera_obscura.jpg'
path_out = sys.argv[4] if len(sys.argv) > 4 else 'out.pgm'

img = Image.open(path_in)
#img = np.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 1], [3, 4, 5, 1, 2]])
#print(img.shape)
cols, rows  = img.size

#edgeFilter()
fastEdgeFilter()

# if "binarisieren" == sys.argv[1]:
#    binarize(int(sys.argv[2]))
# elif "gamma" == sys.argv[1]:
#    gamma(float(sys.argv[2]))
# elif "heller" == sys.argv[1]:
#    brigther(int(sys.argv[2]))
# elif "edge" == sys.argv[1]:
#    edgeFilter()
# else:
#    pass

img.save(path_out)