import pygame, random
from fractions import Fraction
from 공격수단.enemy_aa import Enemy_aa


class Enemy(pygame.sprite.Sprite):
  def __init__(self, game):
      super().__init__()    
      self.game = game
      self.color = game.colors
      self.width = 25
      self.height = 25
      game.enemy_sprites.add(self)
      game.all_sprites.add(self)
      self.image = pygame.Surface([self.width, self.height])
      self.image.fill(self.color["RED"])
      self.rect = self.image.get_rect()
      self.last_shoot = 0
      self.isAppearing = True
      self.last_move = 0

    # -----------------control----------------------
      self.life = 1
      self.shoot_delay = random.uniform(16, 18) * 100
      self.movement_speed = random.uniform(0.2, 2.5)
      self.move_delay = 6000  #밀리세컨드 단위
      self.ATK = 1

      self.aa_class = Enemy_aa
      self.aa_color = self.color["RED"]
      self.aa_shoot_delay = 1000
      self.aa_size = 6
      self.aa_speed = 10

      self.appearance = {
         "from" : {"x" : game.WIDTH + 40, "y" : game.HEIGHT / 2 - 120},
         "to" : {"x" : game.WIDTH / 2, "y" : game.HEIGHT / 2 },
         }
    #   --------------------------------------------
      self.rect.x = self.appearance["from"]["x"]
      self.rect.y = self.appearance["from"]["y"]

  def update(self):

    if self.isAppearing:
    #    등장 애니메이션 재생
        self.rect.x += self.get_slope_with_from_and_to()["x"] 
        self.rect.y += self.get_slope_with_from_and_to()["y"] 
        if self.rect.x == self.appearance["to"]["x"] and self.rect.y == self.appearance["to"]["y"]:
            self.isAppearing = False
    else:
    #    플레이어와 대치 시작
        now = pygame.time.get_ticks()
        if now -  self.last_move >= self.move_delay:
            
            dry = random.choice([1, -1])
            drx = random.choice([1, -1])
            
            self.rect.x += self.movement_speed * drx
            self.rect.y += self.movement_speed * dry

            self.last_move = now


        # 총알 발사
        now = pygame.time.get_ticks()
        if now - self.last_shoot >= self.shoot_delay:
            self.last_shoot = now
            # 총알 생성
            aa = self.aa_class(self.game, self, self.rect.centerx, self.rect.centery)

        # 플레이어의 총알에 맞으면 죽음
        if pygame.sprite.spritecollide(self, self.game.player_attack, True):
            self.life -= 1
            if self.life <= 0:
                # self.game.score += 1
                print("dead")
                
                # self.kill()
                


  def get_slope_with_from_and_to(self):
    x_increase = self.appearance["to"]["x"] - self.appearance["from"]["x"]
    y_increase = self.appearance["to"]["y"] - self.appearance["from"]["y"]
    frac = Fraction(int(x_increase), int(y_increase))
    return {"x" : frac.numerator, "y" : frac.denominator}
        

        # 좌표평면에서 (x1, y1) 과 (x2, y2) 를 지나는 직선의 기울기 x2 - x1 / y2 - y1