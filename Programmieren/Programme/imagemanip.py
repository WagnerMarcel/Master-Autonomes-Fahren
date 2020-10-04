import sys
import PIL.Image as Image

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


path_in = sys.argv[3] if len(sys.argv) > 3 else 'foto.pgm'
path_out = sys.argv[4] if len(sys.argv) > 4 else 'out.pgm'

img = Image.open(path_in)
cols, rows = img.size

if "binarisieren" == sys.argv[1]:
   binarize(int(sys.argv[2]))
elif "gamma" == sys.argv[1]:
   gamma(float(sys.argv[2]))
elif "heller" == sys.argv[1]:
   brigther(int(sys.argv[2]))
else:
   pass

img.save(path_out)