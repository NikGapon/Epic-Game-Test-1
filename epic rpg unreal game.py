import sys
import os
import random
import pygame

pygame.init()

FPS = 50
WIDTH = 1024
HEIGHT = 768
STEP = 10
TILE_WIDTH = TILE_HEIGHT = 90
inv_open = 1
proverka_inv = 1

location = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
timer = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
monster = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
inv_group = pygame.sprite.Group()



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image: ', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

inv_sprite = pygame.sprite.Sprite()
inv_sprite.image = load_image("inv v3.png")
inv_sprite.rect = inv_sprite.image.get_rect()
inv_group.add(inv_sprite)
inv_sprite.rect.x = 4000
inv_sprite.rect.y = -4000

#XP_boots_25 = pygame.sprite.Sprite()
#XP_boots_25 = load_image('Xp_boost_+25.png')
#XP_boots_25.rect = XP_boots_25.image.get_rect()
#inv_group.add(XP_boots_25)
#XP_boots_25.rect = 4000
#XP_boots_25.rect = -4000



class Hero:
    def __init__(self, class_hero):

        self.inv_hero = []
        self.ekip_hero = []  # заполнит после реализации классов персонажей
        self.class_hero = class_hero
        self.lvl_hero = None



    def open_inv(self):
        return self.inv_hero

    def apend_inv_hero(self, lot):
        if len(self.inv_hero) <= 20:
            self.inv_hero.append(lot)
        else:
            pass  # тут должно быть сообщение о  заролнености инвентаря на николаю(мне) лень его писать





def class_select_screen():
    fon = pygame.transform.scale(load_image('menu_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    warrior = pygame.transform.scale(load_image('animations\\warrior_down_2.png'), (152, 190))
    wizard = pygame.transform.scale(load_image('animations\\wizard_down_2.png'), (169, 190))
    archer = pygame.transform.scale(load_image('animations\\archer_down_2.png'), (155, 190))
    screen.blit(wizard, (450, 300))
    screen.blit(warrior, (250, 300))
    screen.blit(archer, (650, 300))
    screen.blit(font.render("Select the class", 1, pygame.Color('yellow')), (250, 100))
    font = pygame.font.Font(None, 50)
    screen.blit(font.render("Warrior", 1, pygame.Color('brown')), (265, 500))
    screen.blit(font.render("Wizard", 1, pygame.Color('purple')), (475, 500))
    screen.blit(font.render("Archer", 1, pygame.Color('green')), (670, 500))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 200 and event.pos[0] < 401 and event.pos[1] < 491 and event.pos[1] > 300:
                    return 'warrior'
                elif event.pos[0] > 456 and event.pos[0] < 613 and event.pos[1] < 491 and event.pos[1] > 300:
                    return 'wizard'
                elif event.pos[0] > 649 and event.pos[0] < 804 and event.pos[1] < 491 and event.pos[1] > 300:
                    return 'archer'
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["Epic unreal rpg game", "",
                  "Press any key"]

    fon = pygame.transform.scale(load_image('menu_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)



def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as map_file:
        level_map = [list(line.strip()) for line in map_file]
    max_width = max(map(len, level_map))
    map(lambda x: x.ljust(max_width, '.'), level_map)
    return list(level_map)


def generate_level(level):
    new_player, x, y = None, None, None
    level[random.randint(0, 4)][random.randint(0, 10)] = '!'
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('road', x, y)
            elif level[y][x] == '@':
                if location == 1:
                    Tile('road', x, y)
                elif location == 0:
                    Tile('empty', x, y)
                new_player = Player(x, y - 0.1)
            elif level[y][x] == '&':
                Wall(x, y)
            elif level[y][x] == '!':
                Monster(x, y)


    return new_player


start_screen()
player_class = class_select_screen()

tile_images = {
    'road': load_image('road.png'),
    'empty': load_image('grass1.png'),
    'player': load_image('animations\\{}_down_2.png'.format(player_class))
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)

class Wall(Tile):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self, walls_group)
        self.image = load_image('wood.png')
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, x, y):
        super().__init__(all_sprites)
        self.frames = frames
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.move(x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(monster, all_sprites)
        self.image = load_image('monster.png')
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x + 15, TILE_HEIGHT * y + 5)




class Player(AnimatedSprite):
    def __init__(self, x, y):
        self.frames = []
        self.cur_frame = 0
        self.image = tile_images['player']
        pygame.sprite.Sprite.__init__(self, player_group)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x + 15, TILE_HEIGHT * y + 5)

    def collide(self, wall):
        if pygame.sprite.collide_rect(self, wall):
            pass

    def update(self, frames):
        clock.tick(15)
        self.frames = frames

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]



class inv_eqip_upd(pygame.sprite.Sprite):
    def __init__(self, frames_name_save):
        super().__init__(inv_group)
        #self.freme = pygame.sprite.Sprite()
        self.freme = load_image(frames_name_save)
        self.rect = self.freme.get_rect()
        #pygame.sprite.Sprite.__init__(self, inv_group)
        self.rect.x = 4000
        self.rect.y = -4000

    def upd(self, x, y):
        self.rect.x = x
        self.rect.y = y


level = load_level('test_world.txt')
player = generate_level(level)

total_level_width = len(level[0]) * 40
total_level_height = len(level) * 40

Player_Hero = Hero(player_class)


XP_boots_25 = inv_eqip_upd('Xp_boost_+25.png')

#--------------------------------
Player_Hero.apend_inv_hero(XP_boots_25)
#--------------------------------












pressed_left = False
pressed_right = False
pressed_up = False
pressed_down = False
running = True
while running:
    if proverka_inv % 2 == 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:  # check for key releases

                if event.key == pygame.K_i:
                    if proverka_inv % 2 == 0:
                        inv_sprite.rect.x = 4000
                        inv_sprite.rect.y = -4000
                    else:
                        inv_sprite.rect.x = 0
                        inv_sprite.rect.y = 0

                        inv_print = Player_Hero.open_inv()
                        for n in inv_print:
                            n.upd(100, 100)



                    proverka_inv += 1

    elif proverka_inv % 2 != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # check for key presses
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:# left arrow turns left
                    pressed_left = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: # right arrow turns right
                    pressed_right = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:  # up arrow goes up
                    pressed_up = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # down arrow goes down
                    pressed_down = True
            elif event.type == pygame.KEYUP:  # check for key releases
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.update([load_image('animations\\{}_left_2.png'.format(player_class))])# left arrow turns left
                    pressed_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.update([load_image('animations\\{}_right_2.png'.format(player_class))])# right arrow turns right
                    pressed_right = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.update([load_image('animations\\{}_up_2.png'.format(player_class))])# up arrow goes up
                    pressed_up = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.update([load_image('animations\\{}_down_2.png'.format(player_class))])# down arrow goes down
                    pressed_down = False
                elif event.key == pygame.K_i:

                    if proverka_inv % 2 == 0:
                        inv_sprite.rect.x = 4000
                        inv_sprite.rect.y = -4000
                    else:
                        inv_sprite.rect.x = 0
                        inv_sprite.rect.y = 0




                    proverka_inv += 1

        # In your game loop, check for key states:
        if pressed_left:
            player.update(
                [load_image('animations\\{}_left_1.png'.format(player_class)),
                 load_image('animations\\{}_left_2.png'.format(player_class)),
                 load_image('animations\\{}_left_3.png'.format(player_class)),
                 load_image('animations\\{}_left_2.png'.format(player_class))])
            player.rect.x -= STEP
        if pressed_right:
            player.update(
                [load_image('animations\\{}_right_1.png'.format(player_class)),
                 load_image('animations\\{}_right_2.png'.format(player_class)),
                 load_image('animations\\{}_right_3.png'.format(player_class)),
                 load_image('animations\\{}_right_2.png'.format(player_class))])
            player.rect.x += STEP
        if pressed_up:
            player.update(
                [load_image('animations\\{}_up_1.png'.format(player_class)),
                 load_image('animations\\{}_up_2.png'.format(player_class)),
                 load_image('animations\\{}_up_3.png'.format(player_class)),
                 load_image('animations\\{}_up_2.png'.format(player_class))])
            player.rect.y -= STEP
        if pressed_down:
            player.update(
                [load_image('animations\\{}_down_1.png'.format(player_class)),
                 load_image('animations\\{}_down_2.png'.format(player_class)),
                 load_image('animations\\{}_down_3.png'.format(player_class)),
                 load_image('animations\\{}_down_2.png'.format(player_class))])
            player.rect.y += STEP


        for wall in walls_group:
            player.collide(wall)
        if player.rect.x > 980 and location == 0:
            location = 1
            level = load_level('levelex.txt')
            tiles_group.empty()
            walls_group.empty()
            monster.empty()
            player_group.empty()
            player = generate_level(level)

        if player.rect.x < 0 and location == 1:
            location = 0

            level = load_level('test_world.txt')
            tiles_group.empty()
            walls_group.empty()
            monster.empty()
            player_group.empty()
            player = generate_level(level)
    screen.fill(pygame.Color('black'))
    tiles_group.draw(screen)
    walls_group.draw(screen)
    monster.draw(screen)
    player_group.draw(screen)
    inv_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

terminate()
