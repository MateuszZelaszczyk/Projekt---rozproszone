import pygame
from random import randrange


class Map:
    def __init__(self, width, height):
        self.height = height-30
        self.width = width-30
        self.objects = dict()
        self.create_map()

    def create_map(self):
        objects_number = randrange(270, 300)
        for i in range(objects_number):
            self.objects[i] = ['m1', randrange(0, self.width, 30), randrange(0, self.height, 30)]
        for i in range(objects_number):
            self.objects[objects_number+i] = ['m2', randrange(0, self.width, 30), randrange(0, self.height, 30)]

    def get_object_as_str(self, key):
        return str(key) + "," + str(self.objects[key][0]) + "," + str(self.objects[key][1]) + "," + str(self.objects[key][2])

    def get_objects_coordinates_as_str(self):
        return ';'.join(map(lambda key: self.get_object_as_str(key), self.objects))

    def delete_objects(self, objects_keys):
        for key in objects_keys:
            try:
                self.objects.pop(key)
            except KeyError as e:
                pass

