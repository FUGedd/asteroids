import random
import datetime
import pygame as p
import  random as r
from settings import *


class Spaceship:
    def __init__(self, pos: tuple, images: list, thruster_images, shield_images):
        self.images = images
        self.image = images[0]
        self.thruster_images = thruster_images
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.start_pos = pos
        self.hp = 4
        self.score = 0
        self.DESTROY_EVENT = p.USEREVENT + 1
        self.frame = 0
        self.thruster_animation_len = len(self.thruster_images)
        self.shield_power = 0
        self.shield_images = shield_images
        self.shield_rect = shield_images[0].get_rect()
        self.start_game_time = datetime.datetime.now()
        self.play_time = datetime.datetime.now() - datetime.datetime.now()

    def draw(self, target_surf: p.Surface):
        if self.hp > 0:
            target_surf.blit(self.image, self.rect)
            if self.hp < 4:
                target_surf.blit(self.images[-self.hp], self.rect)
        self.draw_thruster(target_surf)
        self.draw_shield(target_surf)

    def move(self):
        keys = p.key.get_pressed()
        if keys[p.K_a]:
            self.rect.x -= 5
        if keys[p.K_d]:
            self.rect.x += 5
        if keys[p.K_s]:
            self.rect.y += 5
        if keys[p.K_w]:
            self.rect.y -= 5

    def restrain(self):
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        self.move()
        self.restrain()

    def get_damage(self, damage):
        if self.shield_power > 0:
            self.shield_power -= damage
        else:
            self.hp -= damage
            if self.hp == 0:
                p.event.post(p.event.Event(self.DESTROY_EVENT))

    def rebuild(self):
        self.hp = 4
        self.score = 0
        self.rect.center = self.start_pos
        self.start_game_time = datetime.datetime.now()

    def draw_thruster(self, target_surf):
        self.frame += 0.5
        if int(self.frame) == self.thruster_animation_len:
            self.frame = 0
        img = self.thruster_images[int(self.frame)]

        l_pos = (self.rect.centerx - 35, self.rect.bottom - 18)
        r_pos = (self.rect.centerx + 21, self.rect.bottom - 18)
        target_surf.blit(img, l_pos)
        target_surf.blit(img, r_pos)

    def apply_shield(self):
        self.shield_power = 3

    def draw_shield(self, target_surf):
        if self.shield_power > 0:
            self.shield_rect.center = self.rect.center
            if self.shield_power != 1:
                self.shield_rect.move_ip((-5, -5))
            target_surf.blit(self.shield_images[self.shield_power - 1], self.shield_rect)

    def heal(self):
        self.hp += 1


class Meteor(p.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center = pos)
        self.speed_x = r.randint(-3,3)
        self.speed_y = r.randint(3,9)
        self.angle = 0
        self.original_image = img
        self.rotate_speed = random.randint(-3, 3)

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()#удаляет спрайт из всех группы

    def rotate(self):
        self.angle += self.rotate_speed
        self.image = p.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)


class Laser(p.sprite.Sprite):
    def __init__(self, pos, images):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.speed_y = -10
        self.animation_len = len(self.images)
        self.frame = 0

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
        self.frame += 0.25
        if int(self.frame) == self.animation_len:
            self.frame = 0
        self.image = self.images[int(self.frame)]


class Button:

    def __init__(self, image, pos, text, font, size = (450,80)):
        self.image = image
        self.image = p.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center = pos)

        self.text_surf,self.text_rect = font.render(text,size = 42)
        self.text_rect.center = self.rect.center

    def draw(self, target_surf):
        target_surf.blit(self.image,self.rect)
        target_surf.blit(self.text_surf,self.text_rect)


class PowerUp(p.sprite.Sprite):

    def __init__(self, pos, image, type_):
        super().__init__()
        self.image = image
        self.type = type_
        self.rect = self.image.get_rect(center = pos)
        self.speed_y = random.randint(1, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
