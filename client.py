import sys
import pygame
from network import Network
from player import Player
from game import Game


def main():
    game = Game()
    pygame.init()
    run = True
    n = Network()
    var = n.get_position()
    print(var)
    startPos, plants_pos = game.read_map_positions(var)
    for pos in plants_pos:
        game.make_plant_pos(pos)
    pygame.display.set_caption("Wyscig ciem")
    p = Player(int(startPos[0]), int(startPos[1]), 60, 60, (255, 255, 255))
    p2 = Player(0, 0, 60, 60, (255, 255, 255))
    clock = pygame.time.Clock()
    while run:
        #clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        player_rect = pygame.Rect(p.x, p.y, 60, 60)
        for i in game.plants:
            rect = pygame.Rect(game.plants[i][1], game.plants[i][2], 40, 40)
            collide = rect.colliderect(player_rect)
            if collide:
                game.eaten_plants.append(i)
        game.delete_objects(game.eaten_plants)
        player_position = game.make_pos((p.x, p.y))
        eaten_plants_str = ",".join([str(int) for key in game.eaten_plants])
        reply = game.read_positions(n.send(player_position + ";" + eaten_plants_str))
        game.eaten_plants.clear()
        p2Pos = reply[0]
        removed_objects = reply[1]
        game.delete_objects(removed_objects)
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()
        p.move()
        game.window(p, p2)
    pygame.quit()
    sys.exit()

main()
