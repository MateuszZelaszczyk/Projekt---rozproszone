import sys
import pygame
from network import Network
from player import Player
from game import Game
from button import Button

pygame.init()
pygame.font.init()

back_photo = pygame.image.load("menu_background.jpg")
button_img = pygame.image.load("back_bt.jpg")
button_img = pygame.transform.scale(button_img,(160,60))
font = pygame.font.SysFont("cambria",40)


def menu():
    game = Game()
    menu_text = font.render("Wyścig ciem bukszpanowych", True, (255,255,255), (0,0,0))
    textRect = menu_text.get_rect()
    textRect.center = (300, 200)
    menu_text.set_alpha(190)
    while True:
        game.win.blit(back_photo, (0, 0))
        game.win.blit(menu_text, textRect)
        mouse_pos = pygame.mouse.get_pos()

        play_bt = Button(button_img, (300, 350), "PLAY", font, (255,255,255), (255,255,255))
        quit_bt = Button(button_img, (300, 440), "QUIT", font, (255,255,255), (255,255,255))

        for button in [play_bt, quit_bt]:
            button.update(game.win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_bt.checkForInput(mouse_pos):
                    play(game)
                if quit_bt.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def play(game):
    #game = Game()
    run = True
    n = Network()
    response = n.get_position()
    print(response)
    startPos, plants_pos = game.read_map_positions(response)
    for pos in plants_pos:
        game.make_plant_pos(pos)
    pygame.display.set_caption("Wielki wyscig ciem")
    p = Player(str(startPos[0]), int(startPos[1]), int(startPos[2]), 60, 60, (255, 255, 255))
    p2 = Player(str(startPos[0]), 0, 0, 60, 60, (255, 255, 255))
    clock = pygame.time.Clock()
    while run:
        #clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        player_rect = pygame.Rect(p.x, p.y, 60, 60)
        for i in game.plants:
            rect = pygame.Rect(game.plants[i][2], game.plants[i][3], 40, 40)
            collide = rect.colliderect(player_rect)
            if collide:
                game.eaten_plants.append(i)
        game.delete_objects(game.eaten_plants)
        p.points += len(game.eaten_plants)
        player_position = game.make_pos((p.map, p.x, p.y))
        eaten_plants_str = ",".join([str(key) for key in game.eaten_plants])
        game.eaten_plants.clear()
        reply = n.send(player_position + ";" + eaten_plants_str)
        print('replay')
        print(reply)
        parsed_reply = game.read_positions(reply)
        removed_objects = parsed_reply[1]
        game.delete_objects(removed_objects)
        p2.map = parsed_reply[0][0]
        p2.x = parsed_reply[0][1]
        p2.y = parsed_reply[0][2]
        p2.update()
        p.move()
        game.window(p, p2)
    pygame.quit()
    sys.exit()

menu()
