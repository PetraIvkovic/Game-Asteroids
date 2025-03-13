import pygame
import os
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)     # koristiš predefinirani radijus za shot
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen):
        #pygame.draw.circle(screen, pygame.Color("red"), (int(self.position.x), int(self.position.y)), self.radius, 2)
        self.shot_pic = pygame.image.load(os.path.join("assets", "images", "bullet.png"))
        self.shot_pic = pygame.transform.scale(self.shot_pic, (13, 8))
        shot_center = self.shot_pic.get_rect(center=self.position)
        screen.blit(self.shot_pic, shot_center)

    def update(self, dt):
        self.position += self.velocity * dt