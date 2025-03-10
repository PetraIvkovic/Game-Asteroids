import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updateable, drawable)
    Shot.containers = (shots, updateable, drawable)
    AsteroidField.containers = updateable
    asteroid_field = AsteroidField()

    Player.containers = (updateable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0


    while True:                             #beskonačna petlja - igra se stalno izvrsava
        for event in pygame.event.get():    #pygame.event.get() - događaji poput klik miša, pritisak tipke, zatvaranje prozora
            if event.type == pygame.QUIT:   #konstanta koja označava taj dogadaj
                return

        updateable.update(dt)

        for asteroid in asteroids:
            if asteroid.collide(player):
                print("Game over!")
                sys.exit()                  # prvotno je bio pygame.event.post(pygame.event.Event(pygame.QUIT)) i return

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collide(shot):
                    shot.kill()
                    asteroid.split()

        screen.fill(pygame.Color("black"))  #prvo očisti ekran

        for obj in drawable:                #nacrtaj objekte
            obj.draw(screen)

        pygame.display.flip()               #osvježi ekran

        dt = clock.tick(60) / 1000.0        #ograniči framerate na 60 FPS


if __name__ == "__main__":
    main()