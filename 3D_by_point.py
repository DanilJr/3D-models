from PIL import Image
import re


src_x = 800
src_y = 800
img = Image.new('RGB', (src_x , src_y), 'black')
pixels = img.load()
color = (255, 255, 255)

#loading obj file which has vertex coords
with open('model.obj', 'r') as f:
    lines = f.read().splitlines()
  
for line in lines:
    try:
        v, x, y, z = line.split()
    except:
        continue
    #uploading points that we are interested in  
    if v == 'v':
        x = int((float(x) + 10) * 35)
        y = src_y - int((float(y)+1) * 35)
        pixels[x, y] = color


img.show()