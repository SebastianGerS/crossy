import pygame
import os

SCREEN_TITLE = 'CROSSY CROSS'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 100)
dir_path = os.path.dirname(os.path.realpath(__file__))

class GameObject:
    def __init__(self, sprite_path, width, height, x_pos, y_pos):
        image = pygame.image.load(sprite_path)
        self.sprite = pygame.transform.scale(image, (width, height))
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self, background):
        background.blit(self.sprite, (self.x_pos, self.y_pos))


class Character(GameObject):

    def __init__(self, name, sprite, width, height, x_pos, y_pos, speed):
        super().__init__(sprite, width, height, x_pos, y_pos)
        self.name = name
        self.speed = speed
    def level_speed(self, level):
        self.speed *= level


class PlayableCharacter(Character):
    def __init__(self, name, speed):
        super().__init__( name, dir_path +'/player.png', 50, 50, 375, 750, speed)

    def move(self, direction):
        if direction == 'UP':
            self.y_pos -= self.speed
        elif direction == 'DOWN':
            self.y_pos += self.speed
        elif direction == 'RIGHT':
            self.x_pos += self.speed
        elif direction == 'LEFT':
            self.x_pos -= self.speed

    def check_edges(self, screen_width, screen_height):
        if self.y_pos <= 5:
            self.y_pos = 5
        elif self.y_pos >= screen_height - self.height:
            self.y_pos = screen_height - self.height
        if self.x_pos <= 5:
            self.x_pos = 5
        elif self.x_pos >= screen_width - self.width:
             self.x_pos = screen_width - self.width

    def check_for_collitions(self, npc):
        collided = False
        if self.y_pos + self.height -1 > npc.y_pos and self.y_pos < npc.y_pos + npc.height-1:
            if self.x_pos + self.width -1 > npc.x_pos and self.x_pos  < npc.x_pos + npc.width-1:
                collided = True
        return collided

class NpcCharacter(Character):
    def __init__(self, name, x_pos, y_pos, speed):
        super().__init__( name, dir_path + '/enemy.png', 50, 50, x_pos, y_pos, speed)

    def move(self, game_screen_width):
        if self.x_pos <= 5:
            self.speed = abs(self.speed)
        elif self.x_pos >= game_screen_width - self.width -5:
            self.speed = -abs(self.speed)
        self.x_pos += self.speed

class Treasure(GameObject):
    def __init__(self):
        super().__init__(dir_path +'/treasure.png', 50, 50, 375, 50)


class Game:

    TICK_RATE = 60

    def __init__(self, background_path, title, width, height, difficulty):

        self.title = title
        self.width = width
        self.height = height

        background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(background, (width, height))

        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        self.player = PlayableCharacter('Sebbe', 20)
        self.treasure = Treasure()
        self.level = 1
        self.difficulty = difficulty

        self.npcs = []
    def generate_enemys(self):
        enemy_range = self.difficulty + self.level
        if enemy_range > 11:
            enemy_range = 11
        for x in range(enemy_range):

            name = 'enemy' + str(x)
            x_pos = 5
            y_pos = 600 - x * 100
            speed = x +1

            if y_pos <= 0:
                y_pos = 600 - x * 30

            if speed > 40:
                speed = 40

            enemy = NpcCharacter(name, x_pos, y_pos, speed)

            self.npcs.append(enemy)
    def run_game_loop(self):
        is_game_over = False
        did_win = False
        direction = ''
        self.player.x_pos = 375
        self.player.y_pos = 745
        self.player.speed += self.level -1
        self.npcs = []
        self.generate_enemys()
        for npc in self.npcs:
            npc.level_speed(self.level)

        while not is_game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYUP:
                     if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        direction = ''
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        direction = 'DOWN'
                    elif event.key == pygame.K_RIGHT:
                        direction = 'RIGHT'
                    elif event.key == pygame.K_LEFT:
                        direction = 'LEFT'
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.background, (0,0))

            self.player.move(direction)
            self.player.check_edges(self.width, self.height)
            for npc in self.npcs:
                npc.move(self.width)
                npc.draw(self.game_screen)

            self.player.draw(self.game_screen)
            self.treasure.draw(self.game_screen)
            for npc in self.npcs:
                if self.player.check_for_collitions(npc):
                    is_game_over = True
                    did_win = False
                    text = font.render('You Lose!',True, BLACK_COLOR)
                    self.game_screen.blit(text, (300,375))
                    pygame.display.update()
                    clock.tick(1)
                    break

            if self.player.check_for_collitions(self.treasure):
                is_game_over = True
                did_win = True
                text = font.render('You Win!',True, BLACK_COLOR)
                self.game_screen.blit(text, (400,400))
                pygame.display.update()
                clock.tick(1)

            pygame.display.update()
            clock.tick(self.TICK_RATE)
        if did_win:
            self.level += 1
            self.run_game_loop()
        else:
            return
pygame.init()

new_game = Game(dir_path + '/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, 2)
new_game.run_game_loop()

pygame.quit()
quit()