import pygame, ctypes

import pygame_gui.ui_manager
from player import Player
from 적.enemy import Enemy
from effects.effect import Effect
import asyncio
import pygame_gui

class Game:
    def __init__(self):
        # 기존 초기화 코드는 동일합니다.
        pygame.init()
        self.default_resolution = [900, 600]
        self.WIDTH = self.default_resolution[0]
        self.HEIGHT = self.default_resolution[1]

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.isFullscreen = False
        pygame.display.set_caption("동아리 게임")

        self.colors = {
            "BLACK": (0, 0, 0),
            "WHITE": (255, 255, 255),
            "RED": (255, 0, 0),
            "GREEN": (0, 255, 0),
            "PINK": (255, 192, 203),
            "BACKGROUND_COLOR": (30, 30, 30),
        }

        self.FPS = 60
        self.background_image = pygame.image.load('personal/컴공동아리/computer_club/image/space1.png')
        self.background_add_y_value = 0
        self.seconds = 0

        self.all_sprites = pygame.sprite.Group()
        self.player_attack = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_attack = pygame.sprite.Group()

        pygame.mixer.music.load('personal/컴공동아리/computer_club/음악/dreamy pad 5.mp3')
        pygame.mixer.music.play(-1)

        self.font_path = 'personal/컴공동아리/computer_club/폰트/Pretendard-ExtraBold.otf'
        self.font_score = pygame.font.Font(self.font_path, 30)
        self.font_hp = pygame.font.Font(self.font_path, 30)
        self.font_game_over = pygame.font.Font(self.font_path, 60)
        self.font_score_game_over = pygame.font.Font(self.font_path, 45)
        self.font_damage_notice = pygame.font.Font(self.font_path, 30)

        self.clock = pygame.time.Clock()
        self.isGamePlaying = False
        self.game_over = False

        self.player = Player(self)
        self.testEnemy = Enemy(self)

        # asyncio 이벤트 루프 생성
        self.asyncio_loop = asyncio.get_event_loop()

    def run(self):
        self.isGamePlaying = True
        isFullscreen = False
        time_delta = self.clock.tick(60)/1000
        pygui_manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect(20, 10, 100, 100), text="game start", manager=pygui_manager)


        while True:
            for event in pygame.event.get():
                pygui_manager.process_events(event)
                pygui_manager.update(time_delta)

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
                            screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
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
                pygui_manager.draw_ui(self.screen)

                # asyncio 이벤트 루프 실행
                self.asyncio_loop.call_soon(self.asyncio_loop.stop)
                self.asyncio_loop.run_forever()

            if self.game_over:
                print("게임오버창")
                Effect.apply_ATK_effect(self.player, 5)

Game().run()