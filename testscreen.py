import pygame
from player import Player
from 적.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.default_resolution = [900, 600]
        self.WIDTH = self.default_resolution[0]
        self.HEIGHT = self.default_resolution[1]
        self.all_sprites = pygame.sprite.Group()
        self.player_attack = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_attack = pygame.sprite.Group()
       
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.isFullscreen = False
        pygame.display.set_caption("동아리 게임")

    
        self.FPS = 60
        
        self.colors = {
            "BLACK" : (0, 0, 0),
            "WHITE" : (255, 255, 255),
            "RED" : (255, 0, 0),
            "GREEN" : (0, 255, 0),
            "PINK" : (255, 192, 203),
            "BACKGROUND_COLOR" : (30, 30, 30),
        }
        
        
        self.clock = pygame.time.Clock()
        
        self.player = Player(self)
        self.testEnemy = Enemy(self)



    def run(self):
     
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
               
                        
                
            self.screen.fill((245, 239, 235))
    

            
            


            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            pygame.display.update() 
            self.clock.tick(self.FPS)


        


Game().run()