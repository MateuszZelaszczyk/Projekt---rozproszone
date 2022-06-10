import sys
from random import randrange
import pygame
from network import Network

width = 600
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
plant_image = pygame.transform.scale(pygame.image.load("plant.png"), (40, 40))
plant_image2 = pygame.transform.scale(pygame.image.load("plant2.png"), (40, 40))
plants = dict()
clientNumber = 0


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load("cma.jpg"), (60, 60))
        self.image2 = pygame.transform.scale(pygame.image.load("cma2.jpg"), (60, 60))
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win, number):
        pygame.draw.rect(win, self.color, self.rect)
        if number == "1":
            win.blit(self.image, self.rect)
        elif number == "2":
            win.blit(self.image2, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def draw_plant(win, plant_data):
    position = [plant_data[1], plant_data[2], 40, 40]
    pygame.draw.rect(win, (50, 200, 50), position)
    if plant_data[0]:
        win.blit(plant_image, position)
    else:
        win.blit(plant_image2, position)


def read_map_positions(strs):
    strs = strs.split(";")
    player2_pos = read_pos(strs[0])
    strs.pop(0)
    return player2_pos, strs


def read_positions(strs):
    strs = strs.split(";")
    player2_pos = read_pos(strs[0])
    strs.pop(0)
    objects = str.split(",")
    return player2_pos, objects


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_plant_pos(str):
    str = str.split(",")
    plants[int(str[0])] = [True if randrange(2) else False, int(str[1]), int(str[2])]


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def window(win, player, player2):
    win.fill((34, 139, 34))
    for i in plants:
        draw_plant(win, plants[i])
    player.draw(win, "1")
    player2.draw(win, "2")
    pygame.display.update()


def delete_objects(objects_keys):
    for key in objects_keys:
        try:
            plants.pop(key)
        except KeyError as e:
            pass


def main():
    pygame.init()
    run = True
    n = Network()
    startPos, plants_pos = read_map_positions(n.get_position())
    for str in plants_pos:
        make_plant_pos(str)
    p = Player(int(startPos[0]), int(startPos[1]), 60, 60, (255, 255, 255))
    p2 = Player(0, 0, 60, 60, (255, 255, 255))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        reply = read_positions(n.send(make_pos((p.x, p.y))))
        p2Pos = reply[0]
        removed_objects = reply[1]
        delete_objects(removed_objects)
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        p.move()
        window(win, p, p2)


main()
