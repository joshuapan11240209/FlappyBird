import random
import sys

from pygame import Surface
from pygame.surface import SurfaceType
from typing import Union

import pygame
# 導入物件

# Import images and sounds
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
# 用alpha使得鳥的表面可以在背景上運行

pipe_surface = pygame.image.load('assets/pipe-green.png')
bg_surface = pygame.image.load('assets/background-night.png').convert()
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
# 導入圖片

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
# 導入音檔


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 850))
    # 放置地板的圖片及位置

    screen.blit(floor_surface, (floor_x_pos + 580, 850))
#     使地板寬度為580


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    # 隨機生成水管的位置

    bottom_pipe = pipe_surface.get_rect(midtop=(600, random_pipe_pos))
    # 從x座標600的地方生成水管，並生成再隨機位置

    top_pipe = pipe_surface.get_rect(midbottom=(600, random_pipe_pos - 300))
    # 從x座標600的地方生成水管，在bottom_pipe之上，並確保兩者之間有距離300

    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    #     將所有管子向左移

    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        #     放置水管圖片及位置

        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            # 將上方水管翻轉，x座標不需要翻轉所以用False
            screen.blit(flip_pipe, pipe)


def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx == -600:
            pipes.remove(pipe)
    return pipes


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            # 確認鳥是否碰到水管

            death_sound.play()
            return False
    #     碰撞後遊戲為False

    if bird_rect.top <= -100 or bird_rect.bottom >= 850:
        # 確認鳥是否飛太高或太低

        return False
    # 碰撞後遊戲為False

    return True
# 都無的話遊戲為True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    # 設置旋轉角度

    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    # 建一個新的鳥時，取用前一個鳥的矩形的中心點

    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        # 當在主遊戲時，顯示這些
        score_surface = game_font.render(str(int(score)), True, (0, 0, 0))
        # 設置分數的字體、顏色，且分數顯示為整數，(R, G,B )

        score_rect = score_surface.get_rect(center=(290, 110))
        # 設置分數擺放的中心點

        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        # 當在遊戲結束時，顯示這些
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        # f之後為字串

        score_rect = score_surface.get_rect(center=(290, 110))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(290, 800))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    #     使最高分數可以顯示

    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=520)
# 用特定方式打開pygame.mixer，(頻率，文件大小，頻道，緩衝區)
pygame.init()
# 啟動pygame

screen = pygame.display.set_mode((580, 1024))
# 設置視窗大小

clock = pygame.time.Clock()
# 設置幀速率

game_font = pygame.font.Font('04B_19.ttf', 50)
# 導入文字並設置文字大小

# Game Variables
gravity = 0.2
# 設置重力

bird_movement = 0
# 鳥的移動從0開始

game_active = True
# 遊戲開始進行的情況為True

score = 0
high_score = 0
# 分數計算從0開始

bg_surface = pygame.transform.scale2x(bg_surface)
# 調整導入圖片的大小

floor_surface = pygame.image.load('assets/base.png').convert()
# 導入圖片

floor_surface = pygame.transform.scale2x(floor_surface)
# 調整圖片大小

floor_x_pos = 0

bird_frames = [bird_downflap, bird_midflap, bird_upflap]
# 將三個表面放入一個列表

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(200, 512))
# 在一個新的表面上設置一個矩形，而這個表面會在(200,512)上

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
# 每200毫秒增加拍擊次數

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100,512))


pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
# 設置一個事件，這個事件是生成水管

pygame.time.set_timer(SPAWNPIPE, 1700)
# 每1700毫秒會生成水管

pipe_height = [400, 600, 800]
# 設置水管的高度

game_over_rect = game_over_surface.get_rect(center=(290, 512))
# 將game_over設置在矩形中心

score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # 退出while的循環，但沒有完全結束

            sys.exit()
        #     完全的關閉視窗
        #     為了讓視窗能夠方便關閉，例如說:我們按頂部的按鈕能夠關掉視窗

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                # 設置空白鍵來觸發鳥的跳躍

                bird_movement = 0
                bird_movement -= 9
                # 每次彈跳向上9

                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                # 當遊戲為False，我們按下空白鍵，產生以下狀況

                game_active = True
                pipe_list.clear()
                # 清空水管

                bird_rect.center = (200, 576)
                # 將鳥的位置回復原狀

                bird_movement = 0
                # 鳥的運動量歸零

                score = 0
        #         重置分數

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        #     延伸水管列表

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))
    # 放置背景圖片及位置

    if game_active:
        # 如果遊戲為False，這裡的函數無法使用

        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        # 將原本鳥的表面旋轉

        bird_rect.centery += bird_movement
        # 將鳥設置在矩形的中心點

        screen.blit(rotated_bird, bird_rect)
        # 放置鳥的圖片及位置，而這次使用的是矩形，意味著在鳥的周圍有一個矩形

        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        # 使管子移動，新的列表會覆寫舊的列表

        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)
        # 繪製列表

        score += 0.01
        score_display('main_game')
        # 顯示分數
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        # 遊戲結束時顯示的

        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    # 地板會持續向左移動

    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    #     當地板x位置等於或小於-576時，地板的x歸零

    pygame.display.update()
    # 顯示視窗

    clock.tick(120)
    # 限制幀速率在120
