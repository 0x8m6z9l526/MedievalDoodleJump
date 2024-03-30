import pygame
from pygame.locals import *
import sys
import random
import time
import os
import subprocess


pygame.init()
vec = pygame.math.Vector2

# Вносим базовые параметры
HEIGHT = 450
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


# Функция выхода из программы
def terminate():
    pygame.quit()
    sys.exit()


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
background_rect = bg.get_rect()
bg_end = pygame.transform.scale(load_image('End_Fon.png'), (WIDTH, HEIGHT))
start_desk = pygame.transform.scale(load_image('StartName.png'), (WIDTH, HEIGHT))
stat_fon = pygame.transform.scale(load_image('StatFon.png'), (WIDTH, HEIGHT))

# Установка шрифта
font_name = pygame.font.match_font('arial')
WHITE = (255, 255, 255)


# Функция для написания текста
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

USER_NAME = None
global usedNames

# Функция запуска игрового поля
def start_game():
    FullFile = os.path.join('data', 'records.txt')
    Forma = open(FullFile, mode="rt")
    FileText = Forma.readlines()
    thelist_of_highrecords = []
    probel = 1
    usedNames = []
    for i in range(len(FileText)):
        usedNames.append(FileText[i].split(' ')[1])
    if USER_NAME not in usedNames:
        # Создаем новый процесс для запуска игрового поля
        subprocess.Popen(["python", "your_game_file.py", USER_NAME])
        pygame.mixer.music.pause()
    else:
        draw_text(displaysurface, "Никнейм занят!", 22,
                  WIDTH / 2, 400)




# Функция вызова стартового окна
def start_screen():
    global USER_NAME
    fon = pygame.transform.scale(load_image('Start_Fon.png'), (WIDTH, HEIGHT))
    displaysurface.blit(fon, (0, 0))
    name = "Введите имя"
    while True:
        font = pygame.font.SysFont("Verdana", 20)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(name) <= 13:
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    if name == "Введите имя":
                        name = ''
                    else:
                        name = name[0:-1]

            USER_NAME = name
            displaysurface.blit(start_desk, (0, 0))
            text_name = font.render(name, True, (255, 255, 255))
            displaysurface.blit(text_name, (130, 380))
            pygame.display.update()
            # Привязка кнопок
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and 148 <= pygame.mouse.get_pos()[0] <= 267 and 217 <= \
                    pygame.mouse.get_pos()[1] <= 271:
                start_game()  # Добавляем запуск игры при нажатии на кнопку "Старт"
            elif event.type == pygame.MOUSEBUTTONDOWN and 148 <= pygame.mouse.get_pos()[0] <= 267 and 0 <= \
                    pygame.mouse.get_pos()[1] <= 70:
                fon = pygame.transform.scale(load_image('Start_Fon.png'), (WIDTH, HEIGHT))
                displaysurface.blit(fon, (0, 0))
            elif event.type == pygame.MOUSEBUTTONDOWN and 148 <= pygame.mouse.get_pos()[0] <= 267 and 297 <= \
                    pygame.mouse.get_pos()[1] <= 353:
                pygame.mixer.music.play()
                RecordStatistic()

                name = ''
                text_name = font.render(name, True, (255, 255, 255))
                displaysurface.blit(text_name, (130, 380))
            pygame.display.flip()
            FramePerSec.tick(FPS)


def RecordStatistic():
    displaysurface.blit(stat_fon, background_rect)
    FullFile = os.path.join('data', 'records.txt')
    Forma = open(FullFile, mode="rt")
    FileText = Forma.readlines()
    thelist_of_highrecords = []
    probel = 1
    for i in FileText:
        FileTexts = i.split(' ')
        thelist_of_highrecords.append(int(str(FileTexts[3][:-1])))
        count = 1
        thelist_of_highrecords = sorted(thelist_of_highrecords)
        thelist_of_highrecords.reverse()
        theset_of_highrecords = set()
    for i in thelist_of_highrecords:
        theset_of_highrecords.add(i)
    thelist_of_highrecords = []
    for i in theset_of_highrecords:
        thelist_of_highrecords.append(i)
    thelist_of_highrecords.reverse()
    for i in thelist_of_highrecords:
        if count >= 6:
            break
        for x in FileText:
            FileTextu = x.split(' ')
            if i == int(FileTextu[3]):
                draw_text(displaysurface, '{} место - {}, счёт: {}'.format(count, FileTextu[1], str(FileTextu[3])), 18,
                          WIDTH / 2, 185 + probel * 30)
        probel += 1
        count += 1
    pygame.display.flip()
    FramePerSec.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and 148 <= pygame.mouse.get_pos()[0] <= 267 and 0 <= \
                pygame.mouse.get_pos()[1] <= 371:
            start_screen()


# Запуск стартового окна и игры
start_screen()