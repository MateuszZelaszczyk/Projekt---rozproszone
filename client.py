import sys
import pygame
from network import Network
width = 600
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

class  Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load("cma.jpg"),(80,80))
        self.image2 = pygame.transform.scale(pygame.image.load("cma2.jpg"),(80,80))
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self,win, number):
        pygame.draw.rect(win, self.color, self.rect)
        if(number=="1"):
            win.blit(self.image, self.rect)
        elif(number=="2"):
            win.blit(self.image2, self.rect)
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -=self.vel
        if keys[pygame.K_RIGHT]:
            self.x +=self.vel
        if keys[pygame.K_UP]:
            self.y -=self.vel
        if keys[pygame.K_DOWN]:
            self.y +=self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

def read_pos(str):
    str=str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def window(win,player, player2):
    win.fill((255,255,255))
    player.draw(win,"1")
    player2.draw(win,"2")
    pygame.display.update()

def main():
    pygame.init()
    run = True
    n=Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0], startPos[1],80,80,(255,255,255))
    p2 = Player(0,0,80,80,(255,255,255))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        p.move()
        window(win,p,p2)
main()
