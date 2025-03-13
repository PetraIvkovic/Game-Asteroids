import pygame
import random
import os
from assets import images
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        if radius > 50:
            self.image = pygame.image.load(os.path.join("assets", "images", "big-asteroid.png"))
        elif radius > 30:
            self.image = pygame.image.load(os.path.join("assets", "images", "mid-asteroid.png"))
        else:
            self.image = pygame.image.load(os.path.join("assets", "images", "small-asteroid.png"))

        self.image = pygame.transform.scale(self.image, (int(self.radius * 1.5), int(self.radius * 1.5)))
    
    def draw(self, screen):
        #pygame.draw.circle(screen, pygame.Color("black"), self.position, self.radius, 3)
        asteroid_rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, asteroid_rect)  #iscrtavanje slike

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()     #ukloni trenutni asteroid

        if self.radius <= ASTEROID_MIN_RADIUS:      #ako je asteroid mali, prestani s podjelom
            return

        random_angle = random.uniform(20, 50)   #generiraj slučajni kut za razdvajanje

        #rotiraj vektore brzine za dvije suprotne strane
        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS      #izračunaj novi radijus

        #stvori dva nova asteroida s novim radijusom i brzinom
        new_one_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        new_one_asteroid.velocity = a * 1.2

        new_two_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        new_two_asteroid.velocity = b * 1.2