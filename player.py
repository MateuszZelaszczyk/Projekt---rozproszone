import pygame


class Player:
    def __init__(self, map, x, y, width, height, color):
        self.map = map
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.image = pygame.transform.scale(pygame.image.load("cma.jpg"), (60, 60))
        self.image2 = pygame.transform.scale(pygame.image.load("cma2.jpg"), (60, 60))
        self.rect = (x, y, width, height)
        self.vel = 3
        self.points = 0

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
        map_height = 700
        map_width = 600
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
