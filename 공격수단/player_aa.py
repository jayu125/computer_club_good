import pygame

class Player_aa(pygame.sprite.Sprite):
    def __init__(self, game, player, x, y):
      super().__init__()
      self.size = player.aa_size
      self.image_path = "./이미지경로"
      self.player = player
      self.ATK = player.ATK
      self.x = x
      self.y = y
        
      game.player_attack.add(self)
      game.all_sprites.add(self)


        #크기, 색 설정
      self.image = pygame.Surface([self.size , self.size * 3])
      self.image.fill(game.colors["WHITE"])
      self.rect = self.image.get_rect()
  
      self.rect.x = self.x
      self.rect.y = self.y

    def update(self):
      self.rect.y -= self.player.aa_speed
      if self.rect.y < 0: 
            self.kill()
