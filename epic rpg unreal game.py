import sys
import os
import random
import pygame

pygame.init()

FPS = 60
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


shop_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
monsters_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
inv_group = pygame.sprite.Group()
decor_group = pygame.sprite.Group()
fight_group = pygame.sprite.Group()

skills_Archer = {'Меткий выстрел': (0, 35, 'you', 100, 0, 0), 'Метка': (0, 5, 'you', 3, 0, 2),
                 'Рефлексы охотника': (0, 30, 'hero', 0, 0, 5), 'Град выстрелов': (0, 50, 'all', 20, 0, 0),
                 'Целебные травы': (0, 20, 'hero', 0, 20, 0)}

skills_Archer_lvl = [(10, 15, 0, 0), (5, 5, 0, 2), (10, 0, 0, 1), (15, 10, 0, 0), (5, 0, 5, 0)]

skills_Warrior = {'Рубящий удар': (0, 35, 'you', 100, 0, 0), 'удар щитом': (0, 5, 'you', 3, 0, 2),
                  'Поднять Щиты': (0, 30, 'hero', 0, 0, 5), 'Град ударов': (0, 50, 'all', 20, 0, 0),
                  'Малая перевязка': (0, 20, 'hero', 0, 20, 0)}

skills_Warrior_lvl = [(10, 18, 0, 0), (5, 8, 0, 3), (10, 0, 0, 5), (15, 10, 0, 0), (5, 0, 1, 0)]


skills_Wizard = {'Fireball': (0, 35, 'you', 100, 0, 0), 'Огненая броня': (0, 5, 'you', 3, 0, 2),
                 'Чародейский интеллект': (0, 30, 'hero', 0, 0, 5), 'Молния': (0, 50, 'all', 20, 0, 0),
                 'Восполнение Сил': (0, 20, 'hero', 0, 20, 0)}

skills_Wizard_lvl = [(15, 21, 0, 0), (5, 1, 0, 1), (10, 0, 0, 2), (20, 20, 0, 0), (10, 0, 1, 0)]

start_weapon_archer = ('лук', 'нож')
start_armor_archer = ('потрёпаная одежда приключенца', 'шляпа робин гуда')

start_weapon_warrior = ('меч', 'щит')
start_armor_warrior = ('потрёпаная одежда приключенца', 'шлем')

start_weapon_wizard = ('палочка Гари Патера', 'книга-<краткий гайд по игре>')
start_armor_wizard = ('потрёпаная одежда приключенца', 'колпак (поворской) магический')

stat_armor = {'потрёпаная одежда приключенца': 1, 'шляпа робин гуда': 3, 'шлем': 5, 'колпак (поворской) магический': 1}

stat_weapon = {'лук': 3, 'нож': 7, 'меч': 10, 'щит': 1, 'палочка Гари Патера': 3, 'книга-<краткий гайд по игре>': 1}


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


class Hero:
    def __init__(self, class_hero):
        self.hp = 100
        self.mp = 100
        self.inv_hero = []
        self.ekip_hero = []  # заполнит после реализации классов персонажей
        self.class_hero = class_hero
        self.lvl_hero = None
        self.exp = 0
        if class_hero == 'warrior':
            self.weapon = start_weapon_warrior
            self.armor = start_armor_warrior
            self.skills = skills_Warrior
        elif class_hero == 'wizard':
            self.weapon = start_weapon_wizard
            self.armor = start_armor_wizard
            self.skills = skills_Wizard
        elif class_hero == 'archer':
            self.weapon = start_weapon_archer
            self.armor = start_armor_archer
            self.skills = skills_Archer

    def open_inv(self):
        return self.inv_hero

    def apend_inv_hero(self, lot):
        if len(self.inv_hero) <= 20:
            self.inv_hero.append(lot)
        else:
            pass  # тут должно быть сообщение о  заролнености инвентаря на николаю(мне) лень его писать

    def use_item(self, item_inv):
        if len(self.inv_hero) != 0 and item_inv < len(self.inv_hero):
            for u in self.inv_hero:
                if self.inv_hero[item_inv] == u:
                    b = u.baff
                    u.upd_out()
            baff_tec_tec_item = b
            del self.inv_hero[item_inv]
            if baff_tec_tec_item[0] == 'XP':
                self.hp += baff_tec_tec_item[1]

    def hit(self, hit):
        self.hp -= hit

    def heal(self, heal):
        self.hp += heal

    def info_stat(self):
        dam1 = stat_weapon[self.weapon[0]]
        dam2 = stat_weapon[self.weapon[1]]
        arm1 = stat_armor[self.armor[0]]
        arm2 = stat_armor[self.armor[0]]
        dam = dam1 + dam2
        arm = arm1 + arm2  # доделать оброщение 
        return self.hp, self.mp, self.exp


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
                if (event.pos[0] > 200) and (event.pos[0] < 401) and (event.pos[1] < 491) and (event.pos[1] > 300):
                    return 'warrior'
                elif (event.pos[0] > 456) and (event.pos[0] < 613) and (event.pos[1] < 491) and (event.pos[1] > 300):
                    return 'wizard'
                elif (event.pos[0] > 649) and (event.pos[0] < 804) and (event.pos[1] < 491) and (event.pos[1] > 300):
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
    m_x, m_y = random.randint(0, 4), random.randint(0, 10)
    if location != 0 and location != 1:
        if level[m_x][m_y] not in '@&#l':
            level[m_x][m_y] = '!'
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('road', x, y)
            elif level[y][x] == '@':
                Tile('road', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Wall(x, y)
            elif level[y][x] == '!':
                if location == 1:
                    Tile('road', x, y)
                elif location == 0:
                    Tile('empty', x, y)
                Monster(x, y)
            elif level[y][x] == 'l':
                Shop(x, y)
            elif level[y][x] == 'o':
                Decor(x, y)

    return new_player


start_screen()
player_class = class_select_screen()

tile_images = {
    'road': load_image('road.png'),
    'empty': load_image('grass1.png'),
    'player': load_image('animations\\{}_down_2.png'.format(player_class))
}


class Decor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(decor_group, all_sprites)
        self.image = load_image('vegetables.png')
        self.rect = self.image.get_rect().move(TILE_WIDTH * x, TILE_HEIGHT * y)


class Shop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(shop_group, all_sprites)
        self.image = load_image('lavka.png')
        self.rect = self.image.get_rect().move(TILE_WIDTH * x, TILE_HEIGHT * y)


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


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(monsters_group, all_sprites)
        self.image = load_image('monster.png')
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x, TILE_HEIGHT * y)


class Player(AnimatedSprite):
    def __init__(self, x, y):
        self.frames = []
        self.cur_frame = 0
        self.image = tile_images['player']
        pygame.sprite.Sprite.__init__(self, player_group)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * x + 15, TILE_HEIGHT * y + 5)

    def collide(self, other):
        if pygame.sprite.collide_rect(self, other):
            if other.rect.x > self.rect.x:
                self.rect.x -= 10

            if other.rect.x < self.rect.x:
                self.rect.x += 10

            if other.rect.y > self.rect.y:
                self.rect.y -= 10

            if other.rect.y < self.rect.y:
                self.rect.y += 10

    def update(self, frames):
        clock.tick(15)
        self.frames = frames

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class inv_eqip_upd(pygame.sprite.Sprite):
    def __init__(self, frames_name_save, baff):
        super().__init__(inv_group)
        self.baff = baff

        self.image = load_image(frames_name_save)
        self.rect = self.image.get_rect()

        self.rect.x = 4000
        self.rect.y = -4000

    def upd(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def upd_out(self):
        self.rect.x = 4000
        self.rect.y = -4000

    def baff(self):
        return self.baff


def use_inv(m_pos):
    tec_item = (m_pos[1] // 50)

    return tec_item


class Naga(pygame.sprite.Sprite):
    def __init__(self, atc):
        super().__init__(fight_group)
        self.hp_start = 100
        self.skill = [0, 0, -25, 0, 0, 0, 10, 0, 0, 0]
        self.at = atc

        self.image = load_image('monster.png')
        self.rect = self.image.get_rect()
        self.rect.x = 4000
        self.rect.y = -4000

    def upd(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def upd_out(self):
        self.rect.x = 4000
        self.rect.y = -4000

    def fight_stat(self):

        return self.hp_start, self.at, self.skill


class Fight_Go(pygame.sprite.Sprite):
    def __init__(self, class_hero):
        super().__init__(fight_group)
        self.image = load_image('fight v1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 4000
        self.rect.y = -4000
        self.hp_hero = None
        self.mp_hero = None
        self.class_hero = class_hero
        self.lvl_hero = None

        self.hp_monster = None
        self.skill_monster = None
        self.atc_monster = None

    def fight_new(self, hp_hero, mp_hero, hp_monster,  atc_monster, skill_monster, name_m, lvl):
        self.monster_name = name_m
        self.hp_hero = hp_hero
        self.mp_hero = mp_hero
        self.lvl_hero = lvl

        self.hp_monster = hp_monster
        self.skill_monster = skill_monster
        self.atc_monster = atc_monster

        self.rect.x = 0
        self.rect.y = 0

    def fight_step_monster(self):
        step = random.choice(self.skill_monster)

        if step == 0:
            self.hp_hero -= self.atc_monster
            print(self.monster_name, 'Наносит герою', self.atc_monster, 'урона')
            print('Здоровье героя', self.hp_hero)

        if step > 0:
            print(self.monster_name, 'использут умение: <Малое лечение>. +' + str(step), 'здоровья')
            self.hp_monster += step
            print('Здоровье', self.monster_name + ':' + str(self.hp_monster))

        if step < 0:
            self.hp_hero -= step
            print(self.monster_name, 'использет умение <укус>. Герой теряет' + str(step), 'здоровья')

    def win(self):
        pass  # это проверка на выигрыш


level = load_level('test_world1.txt')
player = generate_level(level)


Player_Hero = Hero(player_class)


# ВРЕМЯ ПРЕДМЕТОВ

XP_boots_25_1 = inv_eqip_upd('Xp_boost_+25_v2.png', ['XP', 25])
XP_boots_10_1 = inv_eqip_upd('Xp_boost_+10_v2.png', ['XP', 25])

# --------------START--------------
Player_Hero.apend_inv_hero(XP_boots_25_1)
Player_Hero.apend_inv_hero(XP_boots_10_1)
# ------------

fight_ckek = 0
fight_monster_name = None
fight_step = 'monster'
Fight = Fight_Go(player_class)
fight_ckek_stolk = 0

Naga_m = Naga(10)


pressed_left = False
pressed_right = False
pressed_up = False
pressed_down = False
running = True
while running:
    if fight_ckek == 1:
        if fight_ckek_stolk == 1:
            if fight_monster_name == 'Naga':

                Naga_m.upd(440, 20)
            if fight_step == 'monster':
                Fight.fight_step_monster()
                Fight.win()
                fight_step = 'Hero'

            elif fight_step == 'Hero':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x_mous, y_mouse = event.pos
                        print(x_mous, y_mouse)
                        if (x_mous >= 20) and (x_mous <= 270) and (y_mouse >= 650) and (y_mouse <= 765):
                            pass

        elif fight_monster_name == 'Naga' and fight_ckek_stolk == 0:
            print('Герой видит преред собой Naga, боя не избежать')
            player_tic_hp, player_tic_mp, player_lvl = Player_Hero.info_stat()
            player_lvl = player_lvl // 100 + 1
            monster_tic_hp, monster_tic_atc, monster_tic_skill = Naga_m.fight_stat()

            Fight.fight_new(player_tic_hp, player_tic_mp, monster_tic_hp, monster_tic_atc, monster_tic_skill,
                            fight_monster_name, player_lvl)
            Naga_m.upd(440, 20)

            fight_ckek_stolk = 1

    elif proverka_inv % 2 == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 975 and event.pos[1] <= 40:
                    proverka_inv += 1

                    inv_sprite.rect.x = 4000
                    inv_sprite.rect.y = -4000
                    inv_print = Player_Hero.open_inv()
                    for n in inv_print:
                        n.upd_out()

                else:
                    m = use_inv(event.pos)

                    Player_Hero.use_item(m)

                    inv_sprite.rect.x = 0
                    inv_sprite.rect.y = 0

                    bag_with_items = 0
                    inv_print = Player_Hero.open_inv()

                    for n in inv_print:
                        n.upd(0, bag_with_items * 50)

                        bag_with_items += 1

            elif event.type == pygame.KEYUP:  # check for key releases

                if event.key == pygame.K_i:
                    if proverka_inv % 2 == 0:
                        inv_sprite.rect.x = 4000
                        inv_sprite.rect.y = -4000
                        inv_print = Player_Hero.open_inv()

                        for n in inv_print:
                            n.upd_out()

                    proverka_inv += 1

    elif proverka_inv % 2 != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # check for key presses
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: # left arrow turns left
                    pressed_left = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: # right arrow turns right
                    pressed_right = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:  # up arrow goes up
                    pressed_up = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # down arrow goes down
                    pressed_down = True
            elif event.type == pygame.KEYUP:  # check for key releases
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.update([load_image('animations\\{}_left_2.png'.format(player_class))])  # left arrow turns left
                    pressed_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.update([load_image('animations\\{}_right_2.png'.format(player_class))])  # right arrow turns right
                    pressed_right = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.update([load_image('animations\\{}_up_2.png'.format(player_class))])  # up arrow goes up
                    pressed_up = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.update([load_image('animations\\{}_down_2.png'.format(player_class))])  # down arrow goes down
                    pressed_down = False
                elif event.key == pygame.K_i:

                    if proverka_inv % 2 != 0:

                        inv_sprite.rect.x = 0
                        inv_sprite.rect.y = 0

                        bag_with_items = 0
                        inv_print = Player_Hero.open_inv()

                        for n in inv_print:
                            n.upd(0, bag_with_items * 50)

                            bag_with_items += 1

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

        if player.rect.x > 980 and player.rect.y >= 305 and player.rect.y <= 375 and location == 0:
            location = 1
            level = load_level('levelex.txt')
            decor_group.empty()
            tiles_group.empty()
            walls_group.empty()
            shop_group.empty()
            monsters_group.empty()
            player_group.empty()
            player = generate_level(level)
        if player.rect.x > 980:
            player.rect.x -= 10
        if player.rect.x < 0:
            player.rect.x += 10

        if player.rect.x >= 975 and player.rect.y >= 305 and player.rect.y <= 375 and location == 1:
            location = 2
            level = load_level('city.txt')
            decor_group.empty()
            tiles_group.empty()
            shop_group.empty()
            walls_group.empty()
            monsters_group.empty()
            player_group.empty()
            player = generate_level(level)

        if player.rect.x < 7 and player.rect.y >= 305 and player.rect.y <= 375 and location == 1:
            location = 0
            level = load_level('test_world2.txt')
            decor_group.empty()
            tiles_group.empty()
            shop_group.empty()
            walls_group.empty()
            monsters_group.empty()
            player_group.empty()
            player = generate_level(level)

        if player.rect.x < 7 and player.rect.y >= 305 and player.rect.y <= 375 and location == 0:
            location = -1
            level = load_level('monsters_place.txt')
            decor_group.empty()
            tiles_group.empty()
            shop_group.empty()
            walls_group.empty()
            monsters_group.empty()
            player_group.empty()
            player = generate_level(level)

        if player.rect.x >= 975 and player.rect.y >= 305 and player.rect.y <= 375 and location == -1:
            location = 0
            level = load_level('test_world1.txt')
            decor_group.empty()
            tiles_group.empty()
            shop_group.empty()
            walls_group.empty()
            monsters_group.empty()
            player_group.empty()
            player = generate_level(level)

    screen.fill(pygame.Color('black'))
    tiles_group.draw(screen)

    shop_group.draw(screen)

    for monster in monsters_group:
        if pygame.sprite.collide_rect(player, monster):
            fight_ckek = 1
            fight_monster_name = 'Naga'

    for shop in shop_group:
        player.collide(shop)

    for wall in walls_group:
        player.collide(wall)

    for d in decor_group:
        player.collide(d)

    decor_group.draw(screen)
    monsters_group.draw(screen)
    walls_group.draw(screen)
    player_group.draw(screen)
    inv_group.draw(screen)
    fight_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

terminate()
