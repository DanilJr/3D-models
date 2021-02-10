from PIL import Image
import random


src_x = 800
src_y = 800


class Screen():

    def __init__(self, hight, width):
        self.hight = hight
        self.width = width
        self.img = Image.new('RGB', (width, hight), 'black')
        self.canvas = self.img.load()
        self.z_buffer = [[0] * width for i in range(hight)]


    def point(self, *coords):
        return Point(self, *coords)


class Point:

    def __init__(self, screen, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.screen = screen

    #by z-buffer we are cheking how deep point is, if it closest to user we are pass it
    #otherwise we are creating another one 
    def show(self, color = None):
        screen = self.screen
        x = int(self.x)
        y = int(self.y)
        if self.z <= screen.z_buffer[x][y]:
            return None
        screen.z_buffer[x][y] = self.z
        screen.canvas[x, self.screen.hight - y] = color or (255, 255, 255)


    def copy(self):
        return Point(self.screen, self.x, self.y, self.z)


##unfinished proces of rendering textures
# class TexturePoint(Point):
#     def __init__(self, screen, x, y, z, u, v):
#         super(TexturePoint, self).__init__.(screen, x, y, z)
#         self.u = u
#         self.v = v
# points = [Point(20, 30), Point(120, 60), Point(70, 130)] 
# for p in points:
#     p.show()  


#zero-division check
#result or 0
def zero_div(a, b):
    return float(a)/b if b else 0


#drawing faces by points that joined by lines in triangles
def triangle(coords, color):
    a, b, c = sorted(coords, key=lambda p: p.y)
    p1 = a.copy()
    p2 = a.copy()
    delta_p1 = zero_div((b.x - a.x), (b.y - a.y))
    delta_p2 = zero_div((c.x - a.x), (c.y - a.y))
    delta_z1 = zero_div((c.z - a.z), (c.y - a.y))
    delta_z2 = zero_div((c.z - a.z), (c.y - a.y))
    for y in (b.y, c.y):
        while p1.y < y:
            if p1.x > p2.x:
                p3 = p2.copy()
                p4 = p1.copy()
            else:
                p3 = p1.copy()
                p4 = p2.copy()
            delta_z3 = zero_div((p4.z - p4.z), (p3.x - p3.x))
            while p3.x < p4.x:
                p3.show(tuple([int(p3.z * 128)] * 3))
                p3.x += 1
                p3.z += delta_z3
            p1.y += 1        
            p2.y += 1        
            p1.x += delta_p1        
            p2.x += delta_p2
            p1.z += delta_z1
            p2.z += delta_z2
        delta_p1 = zero_div((c.x - b.x), (c.y - b.y))            
        delta_z1 = zero_div((c.z - b.z), (c.y - b.y))            
        p1 = b.copy()


with open('Stone.obj', 'r') as f:
    lines = f.read().splitlines()
points = []
screen = Screen(src_x, src_y)   
for line in lines:
    try:
        v, x, y, z = line.split()
    except:
        continue  
    #vertexes  
    if v == 'v':
        x = int((float(x) + 9) * 45)
        y = int((float(y) + 1) * 45)
        z = float(z) + 1
        points.append(screen.point(x, y, z))
    #firsts numbers in f-strings are numbers of points that we are looking for
    if v == 'f':
        color = (random.randint(0, 255)) * 3
        triangle([points[int(i.split('/')[0])-1] for i in (x, y, z)], color)
 
        
screen.img.show()
