import sys
from random import randrange
import pygame
from network import Network
map_width = 600
map_height = 700

win = pygame.display.set_mode((map_width, map_height))
pygame.display.set_caption("Client")
plant_image = pygame.transform.scale(pygame.image.load("plant.png"), (40, 40))
map1_image = pygame.transform.scale(
    pygame.image.load("map1.png"), (map_width, map_height))
map2_image = pygame.transform.scale(
    pygame.image.load("map2.png"), (map_width, map_height))
clientNumber = 0


class Player():
    def __init__(self, map, x, y, width, height, color):
        self.map = map
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.image = pygame.transform.scale(
            pygame.image.load("cma.jpg"), (60, 60))
        self.image2 = pygame.transform.scale(
            pygame.image.load("cma2.jpg"), (60, 60))
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win, number):
        pygame.draw.rect(win, self.color, self.rect)
        if(number == "1"):
            win.blit(self.image, self.rect)
        elif(number == "2"):
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
        other_map = 'm2' if self.map == 'm1' else 'm1'
        if self.x < 0 and self.y > map_height:
            self.map = other_map
            self.x = map_width - self.width
            self.y = self.height
        elif self.x > map_width:
            self.map = other_map
            self.x = 0 + self.width
            self.y = map_height - self.y
        elif self.x + self.width < 0:
            self.map = other_map
            self.x = map_width - self.width
            self.y = map_height - self.y
        elif self.y < 0:
            self.map = other_map
            self.x = map_width - self.x
            self.y = map_height
        elif self.y > map_height:
            self.map = other_map
            self.x = map_width - self.x
            self.y = 0 + self.height


def draw_plant(win, has_photo, coordinates):
    position = [coordinates[0], coordinates[1], 20, 20]
    pygame.draw.rect(win, (50, 200, 50), position)
    # if has_photo:
    #win.blit(plant_image, position)
    # else:
    # win.blit(position)
    # pass
    win.blit(plant_image, position)


def read_pos(strs):
    strs = strs.split(";")
    player_str = strs[0].split(",")
    player2_pos = player_str[0], int(player_str[1]), int(player_str[2])
    strs.pop(0)
    objects = []
    for str in strs:
        objects.append(read_map_object_pos(str))
    return player2_pos, objects


def read_map_object_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])


def window(win, player, player2, map_objects):
    win.fill((255, 255, 255))
    if player.map == 'm1':
        win.blit(map1_image, (0, 0))
    else:
        win.blit(map2_image, (0, 0))
    for map_object in map_objects:
        draw_plant(win, True if randrange(2) else False,
                   [map_object[0], map_object[1]])
    player.draw(win, "1")
    player2.draw(win, "2")

    pygame.display.update()


def main():
    pygame.init()
    run = True
    n = Network()
    replay = (n.getPos())
    startPos = replay.split(',')
    p = Player(str(startPos[0]), int(startPos[1]),
               int(startPos[2]), 60, 60, (255, 255, 255))
    p2 = Player(str(startPos[0]), 0, 0, 60, 60, (255, 255, 255))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        reply = read_pos(n.send(make_pos((p.map, p.x, p.y))))
        p2Pos = reply[0]
        objects_pos = reply[1]
        p2.map = p2Pos[0]
        p2.x = p2Pos[1]
        p2.y = p2Pos[2]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        p.move()
        window(win, p, p2, objects_pos)


main()
