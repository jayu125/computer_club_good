import pygame
from 공격수단.player_aa import Player_aa

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        game.all_sprites.add(self)
        self.game = game
        self.width = 27
        self.height = 27
        

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(game.colors["WHITE"])
        self.rect = self.image.get_rect()
        self.rect.x = game.WIDTH//2
        self.rect.y = game.HEIGHT-30 
        self.aa_last_shoot=0

        #능력치
        self.HP = 3
        self.ATK = 1
        self.move_speed = 4
        self.aa_speed = 30
        self.aa_shoot_delay = 30  #연사속도 0.05초
        self.aa_size = 4 #기본값 2
        self.item = {
            "double_attack" : True
        }


    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.move_speed
            if self.rect.x<=0 :
                self.rect.x=0

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.move_speed
            if self.rect.x >=self.game.WIDTH - self.width:
                self.rect.x=self.game.WIDTH - self.width
                
        if keys[pygame.K_UP]:
            self.rect.y -= self.move_speed
            if self.rect.y<=self.game.HEIGHT // 2:
                self.rect.y=self.game.HEIGHT // 2

        if keys[pygame.K_DOWN]:
            self.rect.y += self.move_speed
            if self.rect.y >=self.game.HEIGHT - self.height:
                self.rect.y = self.game.HEIGHT - self.height

        if keys[pygame.K_SPACE]:
            if now - self.aa_last_shoot >= self.aa_shoot_delay:
                self.aa_last_shoot = now
                if not self.item["double_attack"]:
                    Player_aa(self.game, self, self.rect.centerx, self.rect.centery)
                else:
                    Player_aa(self.game, self, self.rect.x, self.rect.centery)
                    Player_aa(self.game, self, self.rect.x + self.width - self.aa_size, self.rect.centery)


            
        collition = pygame.sprite.spritecollide(self, self.game.enemy_attack, True)
        if collition:
            for sprite in collition:
                self.HP -= sprite.ATK
                print(self.HP)