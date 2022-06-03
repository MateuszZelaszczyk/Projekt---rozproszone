import sys
import pygame
width = 600
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0;

class  Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load("cma.jpg"),(80,80))
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self,win):
        pygame.draw.rect(win, self.color, self.rect)
        win.blit(self.image, self.rect)

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
        self.rect = (self.x, self.y, self.width, self.height)
def Window(win,player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()

def main():
    pygame.init()
    run = True
    p = Player(50,50,80,80,(255,255,255))
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        p.move()
        Window(win,p)
main()
