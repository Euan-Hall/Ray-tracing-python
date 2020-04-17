import pygame
import random
import math


class Ray:
    def __init__(self, game_display, pos, angle):
        self.white = (200, 200, 200)
        self.gameDisplay = game_display
        self.pos = pos
        self.dir = [math.cos(angle), math.sin(angle)]  # p5.Vector.fromAngle(angle)



    def show(self):
        mult_pos = self.mult(self.dir, 10)
        new_pos = self.add(mult_pos, self.pos)
        pygame.draw.line(self.gameDisplay, self.white, self.pos, new_pos, 1)


    def lookAt(self, x, y):
        self.dir[0] = x - self.pos[0]
        self.dir[1] = y - self.pos[1]
        self.dir = self.norm(self.dir)

    def norm(self, obj):
        mag = math.sqrt(obj[0]**2 + obj[1]**2)
        return [obj[0]/mag, obj[1]/mag]

    def cast(self, wall):
        x1 = wall.x1 # Start
        y1 = wall.y1

        x2 = wall.x2 # End
        y2 = wall.y2

        x3 = self.pos[0] # Start
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0] # End
        y4 = self.pos[1] + self.dir[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        self.u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if (0 < t < 1) and (self.u > 0):
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return [x, y]
        else:
            return False

    def mult(self, obj, by):
        return [obj[0] * by, obj[1] * by]

    def add(self, obj1, obj2):
        return [obj1[0] + obj2[0], obj1[1] + obj2[1]]


class Boundary:
    def __init__(self, game_display, x1, y1, x2, y2):
        # Initiating pygame
        self.gameDisplay = game_display
        self.white = (255, 255, 255)


        # Initiating x/y values
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # Vectorss
        self.a = [x1, y1]
        self.b = [x2, y2]

    def draw(self):
        pygame.draw.line(self.gameDisplay, self.white, self.a, self.b, 5)


class Particle:
    def __init__(self, gd, c, w, h):
        self.gd = gd
        self.color = c
        self.pos = [w / 2, h / 2]
        self.rays = []
        for i in range(0, 365, 5):
            self.rays.append(Ray(self.gd, self.pos, (i * 3.1415/180)))

    def show(self, x, y):
        for ray in self.rays:
            self.pos = [x, y]
            ray.pos = [x, y]
            ray.show()

    def look(self, walls):
        for ray in self.rays:
            closest = None
            record = 9999999
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    d = ray.u
                    if d < record:
                        record = d
                        closest = pt

            if closest:
                x = int(closest[0])
                y = int(closest[1])
                pygame.draw.line(gameDisplay, self.color, self.pos, (x, y), 2)
                #pygame.draw.circle(gameDisplay, b.white, (x, y), 10)





pygame.init()
height = 800
width = 800
white = (255, 255, 255)
black = (0, 0, 0)
gameDisplay = pygame.display.set_mode((height, width))

walls = []
for i in range(0, 5):
    x1 = random.randint(0, 800)
    x2 = random.randint(0, 800)
    y1 = random.randint(0, 800)
    y2 = random.randint(0, 800)
    walls.append(Boundary(gameDisplay, x1, y1, x2, y2))

p = Particle(gameDisplay, white, width, height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            gameDisplay.fill(black)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for wall in walls:
                wall.draw()
            p.look(walls)
            p.show(mouse_x, mouse_y)

            #  r.lookAt(mouse_x, mouse_y)



    pygame.display.update()