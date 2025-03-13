import pygame
import sys
import os
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    
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


    game_status = START     #postavljamo početno stanje igre na START


    while True:                                 #beskonačna petlja - igra se stalno izvrsava
        for event in pygame.event.get():        #pygame.event.get() - događaji poput klik miša, pritisak tipke, zatvaranje prozora
            if event.type == pygame.QUIT:       #konstanta koja označava taj dogadaj
                return

        updateable.update(dt)


        if game_status == START:        #Početni ekran
            player.lives = 3                            
            screen.fill(pygame.Color(0, 0, 0))
            start_text = font.render("Start New Game", True, (255,255,255))
            start_rect = start_text.get_rect(center=player.position)
            screen.blit(start_text, start_rect)
            pygame.display.flip()

            #Čekaj da igrač pristine enter kako bi započeo igru
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            game_status = PLAYING
                            waiting = False
        

        elif game_status == PLAYING:                #Glavni dio igre
            for asteroid in asteroids:              #Provjeri sudar asteroida s igračem
                if asteroid.collide(player):
                    player.lives -= 1
                    asteroid.kill()     #Ukloni asteroid nakon sudara
                    
                    warning_life = font.render("1 LIFE LOST!", True, pygame.Color(255, 16, 240))
                    warning_life_rect = warning_life.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                    screen.blit(warning_life, warning_life_rect)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                
                if player.lives <= 0:
                    player.kill()
                    game_status = GAME_OVER     #Umjesto sys.exit(), postavljamo status igre na GAME_OVER
    
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collide(shot):
                        shot.kill()
                        asteroid.split()

            screen.fill(pygame.Color(0, 0, 0))       #Očisti ekran

            background = pygame.image.load(os.path.join("assets", "images", "space_photo.jpg"))
            screen.blit(background, (0, 0))

            lives_text = font.render(f"LIFE: {player.lives}", True, pygame.Color(255,255,255))
            screen.blit(lives_text, (1, 4))

            for obj in drawable:                 #Nacrtaj objekte
                obj.draw(screen)

            pygame.display.flip()    #Osvježi ekran
            

        elif game_status == GAME_OVER:      #Ekran GAME_OVER
            screen.fill(pygame.Color(0, 0, 0))
            game_over_text = font.render("Game Over! Press Enter to Restart", True, (255,255,255))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(game_over_text, game_over_rect)
            pygame.display.flip()
            

            
            #Čekaj da igrač pritisne Enter za ponovno pokretanje igre
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            game_status = START                                     #Vraćamo igru na početno stanje
                            player.lives = 3                                        #Vraćamo broj života na početna 3
                            player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)    #Ponovno postavljanje početne pozicije igrača
                            waiting = False

        #Ograniči framerate na 60 FPS
        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()