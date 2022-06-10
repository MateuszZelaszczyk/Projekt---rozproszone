import pygame


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
