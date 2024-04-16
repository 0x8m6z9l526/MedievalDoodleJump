from datetime import time
from pygame import K_LEFT, K_RIGHT, QUIT
import pygame
import random
import os
import sys
import subprocess


# Инициализация Pygame
pygame.init()
vec = pygame.math.Vector2

# Базовые параметры игры
HEIGHT = 650
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

# Уставновка времени тика
FramePerSec = pygame.time.Clock()

# Импорт музыкальных эффектов
fullname = os.path.join('data', 'pryshok.mp3')
sound1 = pygame.mixer.Sound(fullname)

pygame.mixer.music.load(os.path.join('data', 'soundtrack2.mp3'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

# Установка размеров экрана
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

USER_NAME = sys.argv[1]


# Функция выхода из программы
def terminate():
    pygame.quit()
    sys.exit()

def load_row_sprites(filename, sprite_width, sprite_height, row_index):
    image = pygame.image.load(filename).convert_alpha()
    row_sprites = []
    cols = image.get_width() // sprite_width
    start_y = row_index * sprite_height
    for col in range(cols):
        rect = pygame.Rect(col * sprite_width, start_y, sprite_width, sprite_height)
        row_sprites.append(image.subsurface(rect))
    return row_sprites



# Функция загрузки изображения
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# Создание картинок
bg = pygame.transform.scale(load_image('fon_dodle.png'), (WIDTH, HEIGHT))
bg_end = pygame.transform.scale(load_image('End_Fon.png'), (WIDTH, HEIGHT))
start_desk = pygame.transform.scale(load_image('StartName.png'), (WIDTH, HEIGHT))
stat_fon = pygame.transform.scale(load_image('StatFon.png'), (WIDTH, HEIGHT))
bg_end = pygame.transform.scale(load_image('End_Fon2.png'), (WIDTH, HEIGHT))
background_rect = bg.get_rect()

# Класс персонажа
class Player(pygame.sprite.Sprite):
    score = 0

    def __init__(self):
        super().__init__()
        self.idle_frames = load_row_sprites('data/character2.png', 50, 50, 0)
        self.right_frames = load_row_sprites('data/character2.png', 50, 50, 1)
        self.left_frames = load_row_sprites('data/character2.png', 50, 50, 2)
        self.jump_frames = load_row_sprites('data/character2.png', 50, 50, 3)

        self.current_frame = 0
        self.image = self.idle_frames[self.current_frame]
        self.surf = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.surf.get_rect()
        self.pos = vec(10, 360)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.moving_right = False
        self.moving_left = False

    # Функция передвижения
    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -0.3
            self.moving_left = True
            self.moving_right = False
        elif pressed_keys[pygame.K_RIGHT]:
            self.acc.x = 0.3
            self.moving_right = True
            self.moving_left = False
        else:
            self.moving_right = False
            self.moving_left = False

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Обработка выхода за границы экрана
        if self.pos.x > WIDTH:  # Если персонаж выходит за правую границу экрана
            self.pos.x = 0  # Переместить персонажа на левый край
        elif self.pos.x < 0:  # Если персонаж выходит за левую границу экрана
            self.pos.x = WIDTH  # Переместить персонажа на правый край

        self.rect.midbottom = self.pos


    # Функция прыжка
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -17
            self.current_jump_frame = 0

    # Функция отмены
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    # Функция обновления спрайта на новой позиции
    def update(self):
        # Обработка гравитации
        self.acc = vec(0, 0.5)

        # Проверка на столкновения с платформами
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel.y > 0:  # Спуск
                if self.pos.y < hits[0].rect.bottom:
                    # Проверяем, стоит ли начислять очки за платформу
                    if hits[0].point == True:
                        hits[0].point = False
                        Player.score += 1
                    # Корректировка позиции и скорости при приземлении
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    self.current_frame = 0  # Сброс анимации прыжка при приземлении

        # Перемещение игрока с учетом ввода с клавиатуры
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -0.5
            self.moving_left = True
            self.moving_right = False
        elif pressed_keys[pygame.K_RIGHT]:
            self.acc.x = 0.5
            self.moving_right = True
            self.moving_left = False
        else:
            self.moving_right = False
            self.moving_left = False

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        # Обновление анимации
        if self.jumping:
            if self.current_frame < len(self.jump_frames) - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0  # Повторение анимации или остановка на последнем кадре
            self.image = self.jump_frames[self.current_frame]
        elif self.moving_right:
            if self.current_frame < len(self.right_frames) - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.right_frames[self.current_frame]
        elif self.moving_left:
            if self.current_frame < len(self.left_frames) - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.left_frames[self.current_frame]
        else:
            if self.current_frame < len(self.idle_frames) - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.idle_frames[self.current_frame]

        self.surf = pygame.transform.scale(self.image, (50, 50))


# Установка шрифта
font_name = pygame.font.match_font('arial')
WHITE = (255, 255, 255)


# Функция для написания текста в дальнейшем
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Класс платформ
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = load_image("platform.png")
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 60),
                                               random.randint(0, HEIGHT - 30)))
        self.speed = random.randint(-1, 2)

        self.point = True
        self.moving = True

    # Функция движения платформ
    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH


# Функция проверки на касание платформ
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (
                    abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False


# Функция генерации платформ на экране
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = platform()
        C = True

        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)


PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((100, 100, 100))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

PT1.moving = False
PT1.point = False

for x in range(random.randint(4, 5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)


def show_game_over_screen():
    global USER_NAME
    if USER_NAME != '' and USER_NAME not in ("Введите имя", "Введите им", "Введите и", "Введите ", "Введите"):
        FullFile = os.path.join('data', 'records.txt')
        RecordsFile = open(FullFile, 'a')
        Forma = open(FullFile, mode="rt")
        FileText = Forma.readlines()
        RecordsFile.write(' {} - {}\n'.format(USER_NAME, Player.score))
        RecordsFile.close()

    displaysurface.blit(bg_end, background_rect)
    draw_text(displaysurface, "Ваш счёт составил: {}".format(Player.score), 18,
              WIDTH / 2, 225, WHITE)
    draw_text(displaysurface, "Нажмите R для рестарта", 18,
              WIDTH / 2, 370, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        FramePerSec.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False


def start_game():
    global USER_NAME
    while True:
        P1.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    P1.jump()
                    sound1.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    P1.cancel_jump()

        if P1.rect.top > HEIGHT:
            show_game_over_screen()
            return

        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

        plat_gen()
        displaysurface.blit(bg, (0, 0))
        f = pygame.font.SysFont("Verdana", 20)
        g = f.render(str(P1.score), True, (123, 255, 0))
        displaysurface.blit(g, (WIDTH / 2, 10))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        pygame.display.update()
        FramePerSec.tick(FPS)


if P1.rect.top > HEIGHT:
    show_game_over_screen()



# Запуск игры
if __name__ == "__main__":
    start_game()
