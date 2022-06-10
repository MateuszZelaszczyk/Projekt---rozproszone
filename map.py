import pygame
from random import randrange


class Map:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.objects = []
        self.create_map()

    def create_map(self):
        objects_number = randrange(50, 100)
        for i in range(objects_number):
            self.objects.append([randrange(self.width), randrange(self.height)])

    def delete_object(self, x, y):
        pass

    def get_object_as_str(self, game_object):
        return str(game_object[0]) + "," + str(game_object[1])

    def get_objects_coordinates_as_str(self):
        return ';'.join(map(lambda x: self.get_object_as_str(x), self.objects))
