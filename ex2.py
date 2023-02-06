import os
import sys

import pygame
import requests


def spn(delt, c):
    d = f"{delt + c}"
    print(delt)
    return d


api_server = "http://static-maps.yandex.ru/1.x/"
lon = "37.530887"
lat = "55.703118"
kk = 0
delta = spn(0.009, kk)
delta_new = delta
print(delta_new)

params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}
response = requests.get(api_server, params=params)


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
            if event.key == pygame.K_UP and float(delta_new) > 0:
                kk = -0.001
                delta_new = spn(float(delta_new), kk)
                params = {
                    "ll": ",".join([lon, lat]),
                    "spn": ",".join([delta_new, delta_new]),
                    "l": "map"
                }
                response = requests.get(api_server, params=params)
                if not response:
                    print("Ошибка выполнения запроса:")

                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)

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
            if event.key == pygame.K_DOWN and float(delta_new) < 0.09:
                kk = 0.001
                if delta_new != -1:
                    delta_new = spn(float(delta_new), kk)
                    params = {
                        "ll": ",".join([lon, lat]),
                        "spn": ",".join([delta_new, delta_new]),
                        "l": "map"
                    }
                    response = requests.get(api_server, params=params)

                    if not response:
                        print("Ошибка выполнения запроса:")
                        print("Http статус:", response.status_code, "(", response.reason, ")")
                        sys.exit(1)

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