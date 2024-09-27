import pygame, ctypes
from player import Player
from 적.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.default_resolution = [900, 600]
        self.WIDTH = self.default_resolution[0]
        self.HEIGHT = self.default_resolution[1]
        
       
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.isFullscreen = False
        pygame.display.set_caption("동아리 게임")

        self.colors = {
            "BLACK" : (0, 0, 0),
            "WHITE" : (255, 255, 255),
            "RED" : (255, 0, 0),
            "GREEN" : (0, 255, 0),
            "PINK" : (255, 192, 203),
            "BACKGROUND_COLOR" : (30, 30, 30),
        }

        self.FPS = 60
        self.background_image = pygame.image.load('./image/space1.png')  # 배경 이미지 하나만 로드
        self.background_add_y_value = 0
        
        self.all_sprites = pygame.sprite.Group()
        self.player_attack = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_attack = pygame.sprite.Group()
        
        

        # 배경 음악 추가
        pygame.mixer.music.load('./음악/dreamy pad 5.mp3')
        pygame.mixer.music.play(-1)  # 배경 음악 무한 반복

        # 폰트 설정
        self.font_path = './폰트/PressStart2P-Regular.ttf'
        self.font_score = pygame.font.Font(self.font_path, 30)
        self.font_hp = pygame.font.Font(self.font_path, 30)
        self.font_game_over = pygame.font.Font(self.font_path, 60)
        self.font_score_game_over = pygame.font.Font(self.font_path, 45)

        
        self.clock = pygame.time.Clock()
        self.isGamePlaying = False
        self.game_over = False

        # 기본 세팅
        
        self.player = Player(self)
        self.testEnemy = Enemy(self)




    def draw_background(self, default_y, add_y): 
        empty_space_width = (self.WIDTH - (self.HEIGHT * ( 3 / 2 ))) / 2

        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH / 2 - empty_space_width, self.HEIGHT / 2))
        background_list = [pygame.transform.flip(self.background_image, False, False),
                                pygame.transform.flip(self.background_image, True, False),
                                pygame.transform.flip(self.background_image, True, True),
                                pygame.transform.flip(self.background_image, False, True)]
                                
        background_image_position = [
            (self.WIDTH / 2, 0 + default_y + add_y),
            (empty_space_width, 0 + default_y + add_y),
            (empty_space_width, self.HEIGHT / 2 + default_y + add_y),
            (self.WIDTH / 2, self.HEIGHT / 2 +
            default_y + add_y)
        ]

        for i in range(4):
            self.screen.blit(background_list[i], background_image_position[i])

    
    def run(self):
        self.isGamePlaying = True
        isFullscreen = False
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if isFullscreen:
                            isFullscreen = False
                            self.WIDTH = self.default_resolution[0]
                            self.HEIGHT = self.default_resolution[1]
                            pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                        else:
                            isFullscreen = True
                            user32 = ctypes.windll.user32
                            screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
                            self.WIDTH = screensize[0]
                            self.HEIGHT = screensize[1]
                            pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)

                        
            if self.isGamePlaying:
                
                self.screen.fill((0, 0, 0))
                if self.game_over:
                    self.isGamePlaying = False


                self.draw_background(0, self.background_add_y_value)
                self.draw_background(-self.HEIGHT, self.background_add_y_value)
                self.background_add_y_value += 4
                if self.background_add_y_value >= self.HEIGHT:
                    self.background_add_y_value = 0

                if self.player.HP <= 0:
                    self.game_over = True

                
                


                self.all_sprites.update()
                self.all_sprites.draw(self.screen)
                pygame.display.update() 
                self.clock.tick(self.FPS)


            
            if self.game_over:
                print("게임오버창")


Game().run()