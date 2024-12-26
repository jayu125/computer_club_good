import pygame
import random
import json
import math
import ctypes

class ScoreManager:
    def __init__(self):
        self.score = 0

    def add_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed, color):
        super().__init__()
        self.image = pygame.Surface((10, 5))  # 총알의 크기 설정
        self.image.fill(color)  # 총알의 색 설정
        self.original_image = self.image  # 원본 이미지를 보존
        self.rect = self.image.get_rect(center=(x, y))  # 총알의 위치 설정
        self.angle = angle  # 각도
        self.speed = speed
        self.velocity = pygame.Vector2(self.speed, 0).rotate(self.angle)  # 각도에 맞춰 속도 벡터 계산
        self.image = pygame.transform.rotate(self.original_image, -self.angle)  # 이미지 회전

    def update(self):
        # 총알을 이동시키는 코드
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # 화면 밖으로 나가면 총알 제거
        if self.rect.x < 0 or self.rect.x > 900 or self.rect.y < 0 or self.rect.y > 600:
            self.kill()

    def draw(self, screen):
        # 회전된 이미지를 화면에 그리기
        screen.blit(self.image, self.rect)



class HandleATK(pygame.sprite.Sprite):
    def __init__(self, game, target, duration, property = 1):
        super().__init__()
        self.create_time = pygame.time.get_ticks()
        self.duration = duration
        self.game = game
        self.target = target
        self.property = property
        target.ATK = target.ATK * property

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.create_time > self.duration and self.duration != 0:
            self.game.effects.remove(self)
            self.target.ATK = self.target.ATK / self.property


        
class HandleMoveSpeed(pygame.sprite.Sprite):
    def __init__(self, game, target, duration, property = 1):
        super().__init__()
        self.create_time = pygame.time.get_ticks()
        self.duration = duration
        self.game = game
        self.target = target
        self.property = property
        target.speed = target.speed * property

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.create_time > self.duration and self.duration != 0:
            self.game.effects.remove(self)
            self.target.speed = self.target.speed / self.property


class Item(BaseSprite):
    def __init__(self, x, y, color, RN):
        super().__init__(x, y, 25, 25, color)
        self.item_list = ["double_shot", "overclock", "protection"]
        self.type = self.item_list[RN]
    
    def draw(self, screen):
        super().draw(screen)




class Player(BaseSprite):
    def __init__(self, x, y, speed, color, hp, game):
        super().__init__(x, y, 50, 50, color)
        self.speed = speed
        self.hp = hp
        self.attack_key = pygame.K_SPACE  # 기본 공격 키
        self.attack_key_alt = pygame.K_j  # 대체 공격 키
        self.bullets = pygame.sprite.Group()
        self.game = game
        self.last_shot_time = 0  # 마지막으로 총알을 발사한 시간
        self.shoot_interval = 150  # 총알 발사 간격 (밀리초)
        self.last_damage_time = 0  # 마지막 데미지 받은 시간
        self.damage_cooldown = 50  # 데미지 쿨다운 (밀리초)
        # 삼각형을 그리기 위한 변수 (삼각형 좌표)
        self.triangle_width = 40  # 삼각형의 밑변 길이
        self.triangle_height = 60  # 삼각형의 높이
        self.max_hp = self.hp
        self.ATK = 1

        self.isDoubleShotON = False
    
    def move(self, keys, mouse_pos):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        # 화면 밖으로 나가지 않도록 제한
        self.rect.clamp_ip(pygame.Rect(10, 10, self.game.WIDTH - 20, self.game.HEIGHT - 20))

        # 플레이어가 마우스를 향하도록 각도 계산
        dx, dy = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        return angle

    def draw(self, screen):
        # 플레이어의 위치를 중심으로 마우스를 향하는 각도 계산
        angle = self.move(pygame.key.get_pressed(), pygame.mouse.get_pos())

        # 90도 회전시켜서 꼭짓점이 마우스를 향하도록 조정
        angle += 90

        # 삼각형의 중심 계산 (rect.centerx, rect.centery)
        center = self.rect.center

        # 삼각형의 각 꼭짓점 좌표 계산
        top_point = (self.rect.centerx, self.rect.top)  # 삼각형의 위쪽 꼭짓점
        left_point = (self.rect.centerx - self.triangle_width // 2, self.rect.bottom)
        right_point = (self.rect.centerx + self.triangle_width // 2, self.rect.bottom)

        # 삼각형의 회전 각도를 적용하기 위한 함수
        def rotate_point(center, point, angle):
            angle_rad = math.radians(angle)
            cos_angle = math.cos(angle_rad)
            sin_angle = math.sin(angle_rad)

            # 회전된 좌표 계산
            x = cos_angle * (point[0] - center[0]) - sin_angle * (point[1] - center[1]) + center[0]
            y = sin_angle * (point[0] - center[0]) + cos_angle * (point[1] - center[1]) + center[1]

            return (x, y)

        # 회전된 좌표를 계산 (중심을 기준으로 회전)
        top_point = rotate_point(center, top_point, angle)
        left_point = rotate_point(center, left_point, angle)
        right_point = rotate_point(center, right_point, angle)

        # 삼각형의 중심 계산
        triangle_center_x = (top_point[0] + left_point[0] + right_point[0]) / 3
        triangle_center_y = (top_point[1] + left_point[1] + right_point[1]) / 3

        # 회전된 삼각형 그리기
        pygame.draw.polygon(screen, self.color, [top_point, left_point, right_point])

        return (triangle_center_x, triangle_center_y)  # 삼각형의 중앙을 반환




    def shoot(self, mouse_pos):
        current_time = pygame.time.get_ticks()
        if (pygame.key.get_pressed()[self.attack_key] or pygame.key.get_pressed()[self.attack_key_alt]) and \
           current_time - self.last_shot_time >= self.shoot_interval:
            angle = self.move(pygame.key.get_pressed(), mouse_pos)
            bullet = Bullet(self.rect.centerx, self.rect.centery, angle, 30, (255, 255, 0))
            self.bullets.add(bullet)
            self.last_shot_time = current_time

    
    def draw_hp_ui(self, screen):
        hp_bar_width = 200
        hp_bar_height = 20
        bar_x = self.game.WIDTH // 2 - hp_bar_width // 2
        bar_y = self.game.HEIGHT - 50
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, hp_bar_width, hp_bar_height))  # 빨간 배경
        # 초록색 부분만 HP 비율에 맞게 그리기
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, hp_bar_width * (self.hp / self.max_hp), hp_bar_height))

        # HP 백분율 표시
        hp_percentage_text = self.game.font_select.render(f"HP:{self.hp}", True, self.game.colors["WHITE"])
        screen.blit(hp_percentage_text, (bar_x + hp_bar_width + 10, bar_y + (hp_bar_height - hp_percentage_text.get_height()) // 2))



class Enemy(BaseSprite):
    def __init__(self, x, y, speed, points, hp, game, ATK=1, color=(255, 0, 0)):
        super().__init__(x, y, 40, 40, color)
        self.color = color
        self.speed = speed
        self.points = points
        self.hp = hp
        self.max_hp = self.hp
        self.ATK = ATK # 적 공격력 계수
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.game = game
        self.last_attack_time = 0  # 마지막 공격 시간
        self.attack_interval = 800  # 공격 간격 (2초)
        self.bullets = pygame.sprite.Group()  # 적의 총알 그룹
        self.type = "basic"

    def move(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        # 랜덤하게 방향을 바꿈
        if random.random() < 0.01:  # 일정 확률로 방향 전환
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        # 화면 경계를 벗어나지 않도록 처리
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > self.game.WIDTH - 10:
            self.rect.right = self.game.WIDTH - 10
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.bottom > self.game.HEIGHT + 10:
            self.rect.bottom = self.game.HEIGHT + 10




    def attack(self, player_pos):
    # 플레이어 삼각형의 중앙을 사용
        player_triangle_center = player_pos

        # 일정 간격마다 공격
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_interval:
            # 플레이어와의 상대 위치 계산 (삼각형의 중앙 사용)
            dx, dy = player_triangle_center[0] - self.rect.centerx, player_triangle_center[1] - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))  # 각도 계산
            bullet = Bullet(self.rect.centerx, self.rect.centery, angle, 10, self.color)
            self.bullets.add(bullet)
            self.last_attack_time = current_time  # 마지막 공격 시간 갱신



    def update(self):
        self.move()

    def draw(self, screen):
        super().draw(screen)
        # 총알을 화면에 그리기
        for bullet in self.bullets:
            bullet.update()
            bullet.draw(screen)

    def draw_hp(self, screen):
        hp_bar_width = 40
        hp_bar_height = 5
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, hp_bar_width, hp_bar_height))  # 빨간 배경
        # 초록색 부분만 HP 비율에 맞게 그리기
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, hp_bar_width * (self.hp / self.max_hp), hp_bar_height))



class Buff_item_enemy(BaseSprite):
    def __init__(self, x, y, speed, points, hp, game, ATK=1, color=(255, 0, 0)):
        super().__init__(x, y, 40, 40, color)
        self.color = color
        self.speed = speed
        self.points = points
        self.hp = hp
        self.max_hp = self.hp
        self.ATK = ATK # 적 공격력 계수
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.game = game
        self.last_attack_time = 0  # 마지막 공격 시간
        self.attack_interval = 800  # 공격 간격 (2초)
        self.bullets = pygame.sprite.Group()  # 적의 총알 그룹
        self.type = "buff_item"

    def move(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        # 랜덤하게 방향을 바꿈
        if random.random() < 0.01:  # 일정 확률로 방향 전환
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        # 화면 경계를 벗어나지 않도록 처리
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > self.game.WIDTH - 10:
            self.rect.right = self.game.WIDTH - 10
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.bottom > self.game.HEIGHT + 10:
            self.rect.bottom = self.game.HEIGHT + 10




    def attack(self, player_pos):
    # 플레이어 삼각형의 중앙을 사용
        player_triangle_center = player_pos

        # 일정 간격마다 공격
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_interval:
            # 플레이어와의 상대 위치 계산 (삼각형의 중앙 사용)
            dx, dy = player_triangle_center[0] - self.rect.centerx, player_triangle_center[1] - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))  # 각도 계산
            bullet = Bullet(self.rect.centerx, self.rect.centery, angle, 10, self.color)
            self.bullets.add(bullet)
            self.last_attack_time = current_time  # 마지막 공격 시간 갱신



    def update(self):
        self.move()

    def draw(self, screen):
        super().draw(screen)
        # 총알을 화면에 그리기
        for bullet in self.bullets:
            bullet.update()
            bullet.draw(screen)

    def draw_hp(self, screen):
        hp_bar_width = 40
        hp_bar_height = 5
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, hp_bar_width, hp_bar_height))  # 빨간 배경
        # 초록색 부분만 HP 비율에 맞게 그리기
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, hp_bar_width * (self.hp / self.max_hp), hp_bar_height))



        





class StageManager:
    def __init__(self, game, stage_file):
        self.game = game
        with open(stage_file, 'r') as f:
            self.data = json.load(f)
        self.current_stage = 0

    def get_current_stage(self, score):
        for i, stage in enumerate(self.data["stages"]):
            if score >= stage["score_threshold"]:
                self.current_stage = i
            else:
                break
        return self.current_stage

    def spawn_enemies(self):
        # 현재 스코어에 따라 스테이지 업데이트
        self.current_stage = self.get_current_stage(self.game.score_manager.get_score())
        stage = self.data["stages"][self.current_stage]

        enemies = []
        for enemy_data in stage["enemies"]:
            for _ in range(enemy_data["count"]):
                if enemy_data["type"] == "basic":     #     x     y  속  점수  hp           공격력      색깔
                    enemies.append(Enemy(random.randint(0, 800), -50, 2, 10, 20, self.game))
                elif enemy_data["type"] == "fast":
                    enemies.append(Enemy(random.randint(0, 800), -50, 5, 20, 10, self.game, 2, color=(255, 255, 0)))
                elif enemy_data["type"] == "strong":
                    enemies.append(Enemy(random.randint(0, 800), -50, 1, 50, 40, self.game))
                elif enemy_data["type"] == "buff_item":
                    enemies.append(Buff_item_enemy(random.randint(0, 800), -50, 1, 50, 40, self.game, color=(209, 178, 255)))
        return enemies
    



class Game:
    def __init__(self):
        pygame.init()
        self.default_resolution = [900, 600]
        self.WIDTH = self.default_resolution[0]
        self.HEIGHT = self.default_resolution[1]

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("동아리 게임")

        self.colors = {
            "BLACK": (0, 0, 0),
            "WHITE": (255, 255, 255),
            "RED": (255, 0, 0),
            "GREEN": (0, 255, 0),
            "BLUE": (0, 0, 255),
            "BACKGROUND_COLOR": (30, 30, 30),
        }

        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.isGamePlaying = False
        self.isSelecting = True
        self.isFullscreen = False

        self.font_path = 'personal/컴공동아리/computer_club copy/폰트/Pretendard-Regular.otf'
        self.font_start = pygame.font.Font(self.font_path, 50)
        self.font_select = pygame.font.Font(self.font_path, 30)

        self.selected_spaceship = None
        self.score_manager = ScoreManager()
        self.stage_manager = StageManager(stage_file="/Users/jayu/프로젝트/personal/컴공동아리/computer_club copy/stages.json", game=self)
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

    def draw_spaceship_selection(self):
        self.screen.fill(self.colors["BLACK"])

        title_text = self.font_start.render("Select Your Spaceship", True, self.colors["WHITE"])
        self.screen.blit(title_text, (self.WIDTH / 2 - title_text.get_width() / 2, 50))

        spaceship_data = [
            {"color": self.colors["RED"], "hp": 5, "speed": 2, "x": self.WIDTH // 4},
            {"color": self.colors["GREEN"], "hp": 3, "speed": 3, "x": self.WIDTH // 2},
            {"color": self.colors["BLUE"], "hp": 7, "speed": 1, "x": 3 * self.WIDTH // 4}
        ]

        for data in spaceship_data:
            rect = pygame.Rect(data["x"] - 50, self.HEIGHT // 2 - 50, 100, 100)
            pygame.draw.rect(self.screen, data["color"], rect)

        instructions = self.font_select.render("1: HP 100 | 2: HP 30 | 3: HP 200", True, self.colors["WHITE"])
        self.screen.blit(instructions, (self.WIDTH / 2 - instructions.get_width() / 2, self.HEIGHT - 100))

        pygame.display.update()

    def select_spaceship(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.selected_spaceship = {"color": self.colors["RED"], "hp": 100, "speed": 2}
        elif keys[pygame.K_2]:
            self.selected_spaceship = {"color": self.colors["GREEN"], "hp": 30, "speed": 6}
        elif keys[pygame.K_3]:
            self.selected_spaceship = {"color": self.colors["BLUE"], "hp": 200, "speed": 1}

        if self.selected_spaceship:
            self.isSelecting = False
            self.player = Player(self.WIDTH // 2, self.HEIGHT - 100, self.selected_spaceship["speed"], self.selected_spaceship["color"], self.selected_spaceship["hp"], self)
            self.all_sprites.add(self.player)

    def select_modal(self, fst, sec, fstF, secF):
        selected = False

        while not selected:
            self.screen.fill(self.colors["BLACK"])
            title_text = self.font_start.render("press number key ( 1 or 2 ) to select", True, self.colors["WHITE"])
            self.screen.blit(title_text, (self.WIDTH / 2 - title_text.get_width() / 2, 50))
            first_text = self.font_start.render(fst, True, self.colors["WHITE"])
            self.screen.blit(first_text, (self.WIDTH / 2 - title_text.get_width() / 4, 200))
            second_text = self.font_start.render(sec, True, self.colors["WHITE"])
            self.screen.blit(second_text, (self.WIDTH / 2 - title_text.get_width() / 4 * 3, 200))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                fstF()
            elif keys[pygame.K_2]:
                secF()





    def game_over_screen(self):
        self.screen.fill(self.colors["BLACK"])
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, self.colors["WHITE"])
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, 100))

        score_text = font.render(f"Score: {self.score_manager.get_score()}", True, self.colors["WHITE"])
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, 200))

        pygame.display.update()

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 게임을 재시작하려면 'R'을 눌러야 한다.
                        self.isSelecting = True
                        self.score_manager.reset_score()
                        self.enemies.empty()
                        waiting_for_restart = False  # 'R' 키를 누르면 재시작을 위한 루프 종료
                    elif event.key == pygame.K_ESCAPE:  # ESC를 누르면 게임 종료
                        pygame.quit()
                        quit()

    
    def spawn_buff_item(self, enemy):
        RN = random.randrange(0, 2)
        self.items.add(Item(enemy.rect.center[0], enemy.rect.center[1], (209, 178, 255), RN=RN))

    def fstF(self):
        print("첫 번째")

    def secF(self):
        print("두 번째")


    def run(self):
        game_start_time = pygame.time.get_ticks()
        bool = True

        while True:

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if self.isSelecting:
                self.draw_spaceship_selection()
                self.select_spaceship()
            else:
                mouse_pos = pygame.mouse.get_pos()
                if not self.enemies:
                    self.enemies.add(self.stage_manager.spawn_enemies())

                keys = pygame.key.get_pressed()
                self.player.move(keys, mouse_pos)
                self.player.shoot(mouse_pos)

                for enemy in self.enemies:
                    enemy.update()
                    enemy.attack(self.player.rect.center)  # 적이 플레이어를 향해 공격

                    current_time = pygame.time.get_ticks()

                    if self.player.rect.colliderect(enemy.rect):
                        # 쿨다운 시간 확인
                        if current_time - self.player.last_damage_time >= self.player.damage_cooldown:
                            self.player.hp -= 1
                            self.player.last_damage_time = current_time  # 데미지 받은 시간 갱신

                    if self.player.hp <= 0:  # 플레이어 체력이 0이 되면 게임 종료
                            self.game_over_screen()
                            return

                for effect in self.effects:
                    effect.update()

                for item in self.items:
                    if self.player.rect.colliderect(item.rect):
                            # 아이템 효과 플레이어한테 부여하는 코드 짜야됨.
                            ["double_shot", "overclock", "protection"]
                            if item.type == "double_shot":
                                #여기다 더블 온오프 선택지 주기
                                    self.player.isDoubleShotON = True
                                
                            self.items.remove(item)

                self.screen.fill(self.colors["BACKGROUND_COLOR"])
                

                

                for enemy in self.enemies:
                    enemy.draw(self.screen)
                    enemy.draw_hp(self.screen)
                    enemy.attack(self.player.rect.center)
                    for bullet in self.player.bullets:
                        if bullet.rect.colliderect(enemy.rect):
                            enemy.hp -= self.player.ATK
                            if enemy.hp <= 0:
                                self.enemies.remove(enemy)
                                self.score_manager.add_score(enemy.points)
                                if enemy.type == "buff_item":
                                    self.spawn_buff_item(enemy)
                            bullet.kill()

                if not self.enemies:
                    self.enemies.add(self.stage_manager.spawn_enemies())

                for bullet in self.player.bullets:
                    bullet.update()
                    bullet.draw(self.screen)
                
                for item in self.items:
                    item.draw(self.screen)

                self.select_modal("1 선택지", "2선택지", self.fstF, self.secF)

                
                

                # 게임 내내 딱 한 번만 실행되는 부분
                current_time_for_effect = pygame.time.get_ticks()
                if current_time_for_effect - game_start_time >= 2000:
                    if bool:
                        self.effects.add(HandleATK(self, self.player, 0, 20))
                        # self.effects.add(HandleMoveSpeed(self, self.player, 0, 20))
                        print(self.effects)
                        bool = False


                for bullet in enemy.bullets:
                        if bullet.rect.colliderect(self.player.rect):
                            self.player.hp -= enemy.ATK
                            enemy.bullets.remove(bullet)

                self.player.draw(self.screen)
                self.player.draw_hp_ui(self.screen)
                
                # 현재 스코어 표시
                score_text = self.font_select.render(f"Score: {self.score_manager.get_score()}", True, self.colors["WHITE"])
                self.screen.blit(score_text, (score_text.get_width() - 20, self.HEIGHT - score_text.get_height()))

            pygame.display.update()
            self.clock.tick(self.FPS)

Game().run()
