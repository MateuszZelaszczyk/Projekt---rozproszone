import pygame
from random import randrange


class Game():
    def __init__(self):
        self.width = 600
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.plant_image = pygame.transform.scale(pygame.image.load("plant.png"), (40, 40))
        self.plant_image2 = pygame.transform.scale(pygame.image.load("plant2.png"), (40, 40))
        self.plants = dict()
        self.eaten_plants = []
        self.clientNumber = 0

    def make_plant_pos(self, plant_data):
        plant_data = plant_data.split(",")
        self.plants[int(plant_data[0])] = [True if randrange(2) else False, int(plant_data[1]), int(plant_data[2])]

    def draw_plant(self, win, plant_data):
        position = [plant_data[1], plant_data[2], 40, 40]
        pygame.draw.rect(win, (50, 200, 50), position)
        if plant_data[0]:
            win.blit(self.plant_image, position)
        else:
            win.blit(self.plant_image2, position)

    def read_map_positions(self, strs):
        strs = strs.split(";")
        player2_pos = self.read_pos(strs[0])
        strs.pop(0)
        return player2_pos, strs

    def read_positions(self, strs):
        strs = strs.split(";")
        player2_pos = self.read_pos(strs[0])
        strs.pop(0)
        data = strs[0].split(",")
        if data[0] != '':
            eaten_plants = [int(key) for key in data]
        else:
            eaten_plants = []
        return player2_pos, eaten_plants

    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    def window(self, player, player2):
        self.win.fill((34, 139, 34))
        for i in self.plants:
            self.draw_plant(self.win, self.plants[i])
        player.draw(self.win, "1")
        player2.draw(self.win, "2")
        pygame.display.update()

    def delete_objects(self, objects_keys):
        for key in objects_keys:
            try:
                self.plants.pop(key)
            except KeyError as e:
                pass