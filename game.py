import pygame
from random import randrange


class Game():
    def __init__(self):
        self.width = 600
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.plant_image = pygame.transform.scale(pygame.image.load("plant.png"), (40, 40))
        self.plant_image2 = pygame.transform.scale(pygame.image.load("plant2.png"), (40, 40))
        self.map1_image = pygame.transform.scale(pygame.image.load("map1.png"), (self.width, self.height))
        self.map2_image = pygame.transform.scale(pygame.image.load("map2.png"), (self.width, self.height))
        self.plants = dict()
        self.eaten_plants = []
        self.clientNumber = 0

    def make_plant_pos(self, plant_data):
        plant_data = plant_data.split(",")
        self.plants[int(plant_data[0])] = [True if randrange(2) else False, plant_data[1], int(plant_data[2]), int(plant_data[3])]

    def get_m1_plants(self):
        m1_keys = []
        for key in self.plants:
            if self.plants[key][1] == 'm1':
                m1_keys.append(key)
        return m1_keys

    def get_m2_plants(self):
        m2_keys = []
        for key in self.plants:
            if self.plants[key][1] == 'm2':
                m2_keys.append(key)
        return m2_keys

    def draw_plant(self, win, plant_data):
        position = [plant_data[2], plant_data[3], 40, 40]
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
        return str[0], int(str[1]), int(str[2])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])

    def window(self, player, player2):
        self.win.fill((34, 139, 34))
        if player.map == 'm1':
            self.win.blit(self.map1_image, (0, 0))
            local_plant_keys = self.get_m1_plants()
        else:
            self.win.blit(self.map2_image, (0, 0))
            local_plant_keys = self.get_m2_plants()
        for key in local_plant_keys:
            self.draw_plant(self.win, self.plants[key])
        if player.map == player2.map:
            player2.draw(self.win, "2")
        player.draw(self.win, "1")
        pygame.display.update()

    def delete_objects(self, objects_keys):
        for key in objects_keys:
            try:
                self.plants.pop(key)
            except KeyError as e:
                pass