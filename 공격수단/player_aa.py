import pygame
from effects.effect import Effect
import asyncio

class Player_aa(pygame.sprite.Sprite):
    def __init__(self, game, player, x, y):
      super().__init__()
      self.size = player.aa_size
      self.image_path = "./이미지경로"
      self.player = player
      self.ATK = player.ATK 
      self.x = x
      self.y = y
      self.game = game
        
      game.player_attack.add(self)
      game.all_sprites.add(self)


        #크기, 색 설정
      self.image = pygame.Surface([self.size , self.size * 4])
      self.image.fill(game.colors["WHITE"])
      self.rect = self.image.get_rect()
  
      self.rect.x = self.x
      self.rect.y = self.y
      

    def update(self):
      for i in range(self.player.aa_speed): 
        self.rect.y -= 10

    # 충돌 처리
      if pygame.sprite.spritecollide(self, self.game.enemy_sprites, False):
        fontObj = self.game.font_damage_notice
        textSurfaceObj = fontObj.render(f"{self.ATK}",True, self.game.colors["BLACK"], self.game.colors["WHITE"])
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.centerx = self.rect.x + 20
        textRectObj.centery = self.rect.y + 10
        self.game.screen.blit(textSurfaceObj, textRectObj)


    # 화면 밖으로 나가면 제거
      if self.rect.y < 0:
        Effect.apply_ATK_effect(self.player, 5)
        self.kill()
        

