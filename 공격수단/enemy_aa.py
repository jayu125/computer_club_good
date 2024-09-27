import pygame

class Enemy_aa(pygame.sprite.Sprite):
    def __init__(self, game, enemy, x, y):
      super().__init__()
      self.size = enemy.aa_size
      self.image_path = "./이미지경로"
      self.enemy = enemy
      self.ATK = enemy.ATK
      self.x = x
      self.y = y
        
      game.enemy_attack.add(self)
      game.all_sprites.add(self)


        #크기, 색 설정
      self.image = pygame.Surface([self.size , self.size * 3])
      self.image.fill(game.colors["RED"])
      self.rect = self.image.get_rect()
  
      self.rect.x = self.x
      self.rect.y = self.y

    def update(self):
      self.rect.y += self.enemy.aa_speed
      if self.rect.y < 0: 
            self.kill()
