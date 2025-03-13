import pygame
import os
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.img_player = pygame.image.load(os.path.join("assets", "images", "spaceship.png"))
        self.img_player = pygame.transform.scale(self.img_player, (53, 53))
        self.angle = -1
        self.rotation = 0
        self.shoot_timer = 0    #osigurava da igrač ne može stalno pucati.
    
        self.lives = 3

    def draw(self, screen):
       # pygame.draw.polygon(screen, pygame.Color("darkred"), self.triangle(), 5)    #prvotni prikaz broda - trokut
        rotated_ship = pygame.transform.rotate(self.img_player, -self.angle)    #Rotiramo sliku u suprotnom smjeru jer pygame rotira u smjeru kazaljke na satu
        centered_img = rotated_ship.get_rect(center=self.position)
        screen.blit(rotated_ship, self.position) #slika broda

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt      #omogućava odbrojavanje nezavisno od FPS-a.
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.angle -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_d]:
            self.angle += PLAYER_TURN_SPEED * dt
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shooting_offset = pygame.Vector2(0, -PLAYER_RADIUS).rotate(self.angle)
        shot = Shot(self.position.x + shooting_offset.x, self.position.y + shooting_offset.y)   #kreirati pucanj na poziciji igrača
        shot.velocity = pygame.Vector2(0, -1).rotate(self.angle) * PLAYER_SHOOT_SPEED     #postaviti brzinu metka

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.angle)
        self.position += forward * PLAYER_SPEED * dt
