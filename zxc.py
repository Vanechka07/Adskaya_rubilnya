import pygame
import sys
import os


pygame.init()
screen = pygame.display.set_mode((1600, 896))
pygame.display.set_caption('Adskaya Rubilnya')
clock = pygame.time.Clock()
FPS = 30


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('hello_background_adskaya.png'), (1600, 896))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


background = load_image('hell.png')
player = load_image('samurai.png')
walking_right = [
    load_image('samurai_right_move_1.png'),
    load_image('samurai_right_move_1.png'),
    load_image('samurai_right_move_1.png'),
    load_image('samurai_right_move_1.png'),
    load_image('samurai_right_move_2.png'),
    load_image('samurai_right_move_2.png'),
    load_image('samurai_right_move_2.png'),
    load_image('samurai_right_move_3.png'),
    load_image('samurai_right_move_3.png'),
    load_image('samurai_right_move_3.png'),
    load_image('samurai_right_move_3.png'),
    load_image('samurai_right_move_2.png'),
    load_image('samurai_right_move_2.png'),
    load_image('samurai_right_move_2.png')

]
walking_left = [
    load_image('samurai_left_move_1.png'),
    load_image('samurai_left_move_1.png'),
    load_image('samurai_left_move_1.png'),
    load_image('samurai_left_move_1.png'),
    load_image('samurai_left_move_2.png'),
    load_image('samurai_left_move_2.png'),
    load_image('samurai_left_move_2.png'),
    load_image('samurai_left_move_3.png'),
    load_image('samurai_left_move_3.png'),
    load_image('samurai_left_move_3.png'),
    load_image('samurai_left_move_3.png'),
    load_image('samurai_left_move_2.png'),
    load_image('samurai_left_move_2.png'),
    load_image('samurai_left_move_2.png')
]
hit_animation = [
    load_image('samurai_right_hit_1.png'),
    load_image('samurai_right_hit_1.png'),
    load_image('samurai_right_hit_1.png'),
    load_image('samurai_right_hit_2.png'),
    load_image('samurai_right_hit_2.png'),
    load_image('samurai_right_hit_2.png'),
    load_image('samurai_right_hit_3.png'),
    load_image('samurai_right_hit_3.png'),
    load_image('samurai_right_hit_3.png'),
    load_image('samurai_right_hit_4.png'),
    load_image('samurai_right_hit_4.png'),
    load_image('samurai_right_hit_4.png'),
]
player_move_anim_count = 0
player_hit_anim_count = 0
player_x = 0
player_speed = 32
player_y = 580

is_jump = False
jump_count = 9
start_screen()
running = True
while running:

    screen.blit(background, (0, -128))
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if not keys[pygame.K_d] and not keys[pygame.K_a] and not keys[pygame.K_e]:
        screen.blit(player, (player_x, player_y))
    elif keys[pygame.K_d] and player_x < 1600:
        player_x += player_speed
        screen.blit(walking_right[player_move_anim_count], (player_x, player_y))
    elif keys[pygame.K_a] and player_x > -192:
        player_x -= player_speed
        screen.blit(walking_left[player_move_anim_count], (player_x, player_y))
    # if mouse[pygame.MOUSEBUTTONDOWN] == 1 and is_jump:
    #     screen.blit(hit_animation[player_hit_anim_count], (player_x, player_y))
    if keys[pygame.K_e] and not keys[pygame.K_a] and not keys[pygame.K_d]:
        screen.blit(hit_animation[player_hit_anim_count], (player_x, player_y))

    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -9:
            if jump_count > 0:
                player_y -= (jump_count ** 2) / 2
            else:
                player_y += (jump_count ** 2) / 2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 9

    if player_move_anim_count == 13:
        player_move_anim_count = 0
    else:
        player_move_anim_count += 1

    if player_hit_anim_count == 11:
        player_hit_anim_count = 0
    else:
        player_hit_anim_count += 1

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(30)
