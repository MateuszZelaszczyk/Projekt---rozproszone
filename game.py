import pygame
import sys
from random import randrange


class Game:
    def __init__(self):
        self.width = 600
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.plant_image = pygame.transform.scale(pygame.image.load("plant.png"), (40, 40))
        self.plant_image2 = pygame.transform.scale(pygame.image.load("plant2.png"), (40, 40))
        self.map1_image = pygame.transform.scale(pygame.image.load("map1.png"), (self.width, self.height))
        self.map2_image = pygame.transform.scale(pygame.image.load("map2.png"), (self.width, self.height))
        self.back_photo = pygame.image.load("menu_background.jpg")
        self.font = pygame.font.SysFont("cambria",25)
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

    def window(self, player, player2, timer_counter):
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
        self.draw_timer(timer_counter)
        self.score_draw(player)
        pygame.display.update()

    def delete_objects(self, objects_keys):
        for key in objects_keys:
            try:
                self.plants.pop(key)
            except KeyError as e:
                pass
    
    def draw_timer(self, timer_counter):
        minutes = timer_counter // 60
        seconds = timer_counter % 60
        timer_text = str(minutes).rjust(2, '0') + ':' + str(seconds).rjust(2, '0') if timer_counter > 0 else '00:00'
        surface = pygame.Surface((120, 80))
        surface.set_alpha(128)
        surface.fill((0, 0, 0))
        self.win.blit(surface, (self.width - 120, 0))
        self.win.blit(self.font.render(timer_text, True, (255,255,255)), (self.width - 90, 27))
    
    def display_game_over_screen(self, player1, player2):
        game_over_text = self.font.render("Gra zakończona", True, (255,255,255), (0,0,0))
        textRect = game_over_text.get_rect()
        textRect.center = (300, 200)
        game_over_text.set_alpha(190)
        p1_score_text = self.font.render(f"You scored: {player1.points}", True, (255,255,255), (0,0,0))
        p1_score_rect = p1_score_text.get_rect()
        p1_score_rect.center = (300, 300)
        p1_score_text.set_alpha(190)
        p2_score_text = self.font.render(f"Your opponent scored: {player2.points}", True, (255,255,255), (0,0,0))
        p2_score_rect = p2_score_text.get_rect()
        p2_score_rect.center = (300, 400)
        p2_score_text.set_alpha(190)
        while True:
            self.win.blit(self.back_photo, (0, 0))
            self.win.blit(game_over_text, textRect)
            self.win.blit(p1_score_text, p1_score_rect)
            self.win.blit(p2_score_text, p2_score_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    def score_draw(self, player):
        score_text = self.font.render(f"Score: {player.points}", True,(255,255,255), (0,0,0))
        score_text_rect = score_text.get_rect()
        score_text.set_alpha(180)
        self.win.blit(score_text, score_text_rect)
