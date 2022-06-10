import sys
import pygame
from network import Network
from button import Button


pygame.init()
width = 1200
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fly_attack")
back_photo = pygame.image.load("menu_background.jpg")

button_img = pygame.image.load("back_bt.jpg")
button_img = pygame.transform.scale(button_img,(160,60))


font = pygame.font.SysFont("cambria",40)
menu_font = pygame.font.SysFont("cambria",52)
clientNumber = 0;

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

def play():

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
def menu():
    menu_text = menu_font.render("Wyścig ciem bukszpanowych", True, "white", "black")
    textRect = menu_text.get_rect()
    textRect.center =(600,200)
    menu_text.set_alpha(190)
    while True:
        win.blit(back_photo, (0, 0))
        win.blit(menu_text, textRect)
        mouse_pos = pygame.mouse.get_pos()

        play_bt = Button(button_img, (width*0.5, 350), "PLAY",font, "white", "White")
        quit_bt = Button(button_img, (width*0.5, 440), "QUIT",font,  "white", "White")

        for button in [play_bt, quit_bt]:
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_bt.checkForInput(mouse_pos):
                    play()
                if quit_bt.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu()
