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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
timer = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
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

inv_sprite.image = load_image("inv v1.png")

inv_sprite.rect = inv_sprite.image.get_rect()

inv_group.add(inv_sprite)

inv_sprite.rect.x = 4000
inv_sprite.rect.y = -4000

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('menu_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
        level_map = [line.strip() for line in map_file]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(load_image('player_stay_down.png'), x, y)
    return new_player


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass1.png'),
    'player': load_image('player_stay_down.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)


class Inv(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.proverka = 1
        self.start_y = -4000
        self.start_x = 4000
        self.x = 0
        self.y = 0

    def upd(self):
        self.proverka += 1
        if self.proverka % 2 == 0:
            inv_sprite.rect.x = self.start_x
            inv_sprite.rect.y = self.start_y
        else:
            inv_sprite.rect.x = self.x
            inv_sprite.rect.y = self.y





class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(AnimatedSprite):
    def __init__(self, sheet,  x, y):
        self.frames = []
        pygame.sprite.Sprite.__init__(self, player_group)
        self.image = sheet
        self.rect = self.image.get_rect()
        self.rect.move(TILE_WIDTH * x + 15,
                       TILE_HEIGHT * y + 5)
        if self.rect.w != TILE_WIDTH:
            self.cur_frame = 0
            self.cut_sheet(sheet, 4, 1)
            self.image = self.frames[self.cur_frame]



class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.state = pygame.Rect(0, 0, len(level[0] * 60), len(level) * 60)

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
level = load_level('test_world.txt')
player = generate_level(level)

total_level_width = len(level[0]) * 40
total_level_height = len(level) * 40

pressed_left = False
pressed_right = False
pressed_up = False
pressed_down = False
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # left arrow turns left
                pressed_left = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: # right arrow turns right
                pressed_right = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:  # up arrow goes up
                pressed_up = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # down arrow goes down

                pressed_down = True
        elif event.type == pygame.KEYUP:  # check for key releases

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # left arrow turns left
                pressed_left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # right arrow turns right
                pressed_right = False
            elif event.key == pygame.K_UP or event.key == pygame.K_w:  # up arrow goes up
                pressed_up = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # down arrow goes down
                pressed_down = False

            elif event.type == pygame.K_i:
                Inv().upd()

    # In your game loop, check for key states:
    if pressed_left:
        player.rect.x -= STEP
    if pressed_right:
        player.rect.x += STEP
    if pressed_up:
        player.rect.y -= STEP
    if pressed_down:

        player.rect.y += STEP

    screen.fill(pygame.Color('black'))

    tiles_group.draw(screen)
    player_group.draw(screen)
    inv_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()