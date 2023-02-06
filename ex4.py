import os
import sys

import pygame
import requests


def spn(ap, lon, lat, delta, l):
    api_s = ap
    params = {
        "ll": ",".join([str(lon), str(lat)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": l
    }
    return requests.get(api_s, params=params)


api_server = "http://static-maps.yandex.ru/1.x/"
lon = 37.530887
lat = 55.703118
delta = 0.002
l = 'map'

response = spn(api_server, lon, lat, delta, l)

if not response:
    print("Ошибка выполнения запроса:")

    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP and delta > 0:
                delta -= 0.001
            if event.key == pygame.K_PAGEDOWN and delta < 0.09:
                delta += 0.001
            if event.key == pygame.K_RIGHT:
                lon += 0.001
            if event.key == pygame.K_LEFT:
                lon -= 0.001
            if event.key == pygame.K_UP:
                lat += 0.001
            if event.key == pygame.K_DOWN:
                lat -= 0.001
            if event.key == pygame.K_2:
                l = 'sat'
            if event.key == pygame.K_1:
                l = 'map'
            if event.key == pygame.K_3:
                l = 'sat,skl'
            response = spn(api_server, lon, lat, delta, l)
            # Запишем полученное изображение в файл.
            map_file = "map.png"
            with open(map_file, "wb") as file:
                    file.write(response.content)
        pygame.init()
        screen = pygame.display.set_mode((600, 450))
        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)