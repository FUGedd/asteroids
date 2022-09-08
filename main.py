import datetime
import os
import random
import pygame.freetype
import pygame as pg
import sprites
from settings import *


def make_laser():
    fire_laser_sound.play()
    laser_group.add(sprites.Laser((ship.rect.centerx, ship.rect.top), laser_images))


def make_meteor():
    meteor_img = random.choice(meteor_images)
    meteor = sprites.Meteor((random.randint(0, SCREEN_WIDTH), -20), meteor_img)
    meteor_group.add(meteor)


def check_ship_collision():
    if pg.sprite.spritecollide(ship, meteor_group, True):
        hit_ship_sound.play()
        ship.get_damage(1)


def check_laser_collision():
    for laser in laser_group:
        if pg.sprite.spritecollide(laser, meteor_group, True):
            hit_meteor_sound.play()
            laser.kill()
            ship.score += 1


def draw_game():
    screen.blit(bg_img, (0, 0))
    ship.draw(screen)
    meteor_group.draw(screen)
    laser_group.draw(screen)
    powerup_group.draw(screen)
    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (85, 23), str(ship.hp), WHITE)
    laser_font.render_to(screen, (20, 58), 'laser:', WHITE)
    screen.blit(laser_ind, (120, 54))
    score_font.render_to(screen, (SCREEN_WIDTH - 180, 23), str(ship.score).zfill(5), WHITE)
    draw_time()


def draw_menu():
    screen.blit(bg_img, (0, 0))
    screen.blit(hp_img, (20, 20))
    screen.blit(x_img, (60, 28))
    score_font.render_to(screen, (85, 23), str(ship.hp), WHITE)
    score_font.render_to(screen, (SCREEN_WIDTH - 180, 23), str(ship.score).zfill(5), WHITE)
    button.draw(screen)
    button_red.draw(screen)
    screen.blit(game_over_surf,game_over_rect)
    draw_time()


def update_game():
    ship.update()
    meteor_group.update()
    powerup_group.update()
    laser_group.update()
    check_ship_collision()
    check_laser_collision()
    check_laser_ind()
    check_powerup_collision()


def stop_game():
    pg.mouse.set_visible(True)
    bg_music.fadeout(5000)
    meteor_group.empty()
    laser_group.empty()


def restart_game():
    pg.mouse.set_visible(False)
    new_game_sound.play()
    bg_music.play(-1)
    ship.rebuild()


def check_laser_ind():
    if len(laser_group) > 0:
        laser_ind.fill((255,0,0))
    else:
        laser_ind.fill((0,255,0))


def make_powerup():
    random_number = random.randint(1, 3)
    pos = (random.randint(0, SCREEN_WIDTH), -20)
    if random_number == 1:
        powerup = sprites.PowerUp(pos, powerup_images['shield'], 'shield')
        powerup_group.add(powerup)
    elif random_number == 2:
        powerup = sprites.PowerUp(pos, powerup_images['minik'], 'minik')
        powerup_group.add(powerup)


def check_powerup_collision():
    powerup = pg.sprite.spritecollideany(ship, powerup_group)
    if powerup is None:
        return
    if powerup.type == 'shield':
        ship.apply_shield()
        powerup.kill()
    elif powerup.type == 'minik':
        ship.heal()
        powerup.kill()


def draw_time():
    if game_state == 'PLAY':
        ship.play_time = datetime.datetime.now() - ship.start_game_time
    score_font.render_to(screen, (SCREEN_WIDTH - 185, 50), str(ship.play_time)[:-7], WHITE)


bg_img = pg.image.load('res/Backgrounds/darkPurple.png')
bg_img = pg.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
meteor_images = [pg.image.load(f'res/PNG/Meteors/{name}') for name in os.listdir('res/PNG/Meteors')]
laser_images = [pg.image.load(f'res/PNG/Lasers/laserRed{i}.png') for i in range(12, 17)]
ship_images = [pg.image.load(f'res/PNG/Damage/playerShip3_damage{i}.png') for i in range(1,4)]
ship_images.insert(0,pg.image.load('res/PNG/playerShip3_red.png'))
hp_img = pg.image.load('res/PNG/UI/playerLife3_red.png')
x_img = pg.image.load('res/PNG/UI/numeralX.png')
blue_button_img = pg.image.load('res/PNG/UI/buttonBlue.png')
red_button_img = pg.image.load('res/PNG/UI/buttonRed.png')
thruster_images = [pg.image.load(f'res/PNG/Effects/fire0{i}.png') for i in range(1, 8)]
laser_ind = pg.surface.Surface((25,25))
powerup_images = {'shield': pg.image.load('res/PNG/Power-ups/shield_silver.png'),
                  'minik': pg.image.load('res/PNG/Power-ups/pill_red.png')}
shield_images = [pg.image.load(f'res/PNG/Effects/shield{i}.png') for i in range(1,4)]

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Asteroids')

fire_laser_sound = pg.mixer.Sound('res/Bonus/sfx_laser1.ogg')
hit_meteor_sound = pg.mixer.Sound('res/Bonus/res_Bonus_meteor_hit.wav')
hit_ship_sound = pg.mixer.Sound('res/Bonus/res_Bonus_hit.wav')
game_over_sound = pg.mixer.Sound('res/Bonus/sfx_lose.ogg')
new_game_sound = pg.mixer.Sound('res/Bonus/sfx_twoTone.ogg')
bg_music = pg.mixer.Sound('res/Bonus/res_Bonus_space_ambiance.wav')

score_font = pg.freetype.Font('res/Bonus/kenvector_future.ttf', 32)
laser_font = pg.freetype.Font('res/Bonus/kenvector_future.ttf', 22)
text_font = pg.freetype.Font('res/Bonus/kenvector_future.ttf', 52)

button = sprites.Button(blue_button_img, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 'RESTART', text_font)
button_red = sprites.Button(red_button_img, (SCREEN_WIDTH / 2, SCREEN_HEIGHT /  1.5), 'QUIT', text_font)

game_over_surf, game_over_rect = text_font.render('GAME-OVER')
game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

space_speed = 0

game_state = 'PLAY'

ship = sprites.Spaceship((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100), ship_images, thruster_images, shield_images)
meteor_group = pg.sprite.Group()
powerup_group = pg.sprite.Group()
laser_group = pg.sprite.GroupSingle()

SPAWN_METEOR = pg.USEREVENT
pg.time.set_timer(SPAWN_METEOR, 300)
SPAWN_POWERUP = pg.USEREVENT + 2
pg.time.set_timer(SPAWN_POWERUP, 3000)

bg_music.play(-1)
running = True
pg.mouse.set_visible(False)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if game_state == 'PLAY':
            if event.type == SPAWN_METEOR:
               make_meteor()
            if event.type == pg.MOUSEBUTTONDOWN:
                if len(laser_group) == 0:
                    make_laser()
            if event.type == ship.DESTROY_EVENT:
                game_state = 'MENU'
                stop_game()
            if event.type == SPAWN_POWERUP:
                make_powerup()
        else:
            if event.type == pg.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos):
                game_state = 'PLAY'
                restart_game()
            if event.type == pg.MOUSEBUTTONDOWN and button_red.rect.collidepoint(event.pos):
                running = False

    if game_state == 'PLAY':
        draw_game()
        update_game()
    else:
        draw_menu()

    clock.tick(60)
    pg.display.flip()
