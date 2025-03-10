import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, pygame.Color("white"), self.position, self.radius, 2)

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