from pico2d import *

open_canvas()

background = load_image('background_black.png')

hero_walk_left = load_image('hero_walk_left.png')
hero_walk_right = load_image('hero_walk_right.png')
hero_attack_left = load_image('hero_attack_left.png')
hero_attack_right = load_image('hero_attack_right.png')

# hero_attack_right: 2048x256, 프레임마다 크기가 다름
# (x, y, w, h) - clip_draw용 좌표 (y는 이미지 아래쪽 기준)
ATTACK_RIGHT_FRAMES = [
    (76, 178, 22, 23),
    (203, 178, 21, 23),
    (325, 178, 21, 21),
    (426, 178, 62, 23),
    (569, 178, 42, 23),
    (700, 177, 36, 22),
    (820, 185, 39, 23),
    (947, 190, 33, 22),
    (1062, 176, 32, 37),
    (1198, 175, 24, 27),
    (1332, 176, 26, 22),
    (1454, 177, 27, 22),
    (1561, 177, 43, 22),
    (1684, 177, 35, 22),
    (1810, 177, 34, 22),
    (1937, 177, 34, 22),
    (17, 49, 34, 22),
    (145, 49, 34, 22),
]

# hero_walk_right / hero_walk_left: 256x49, 4프레임(각 64x49)
WALK_FRAME_W, WALK_FRAME_H = 64, 49
WALK_FRAME_COUNT = 4
SCALE = 14

LOOP_REPEAT = 5  # 애니메이션 반복 횟수 (반복 후 1초 정지)

hero_walk = hero_walk_right  # 현재 재생 중인 시트

running = True
frame = 0
loop_count = 0
while running:
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False

    clear_canvas()
    background.draw(400, 300)
    hero_walk.clip_draw(frame * WALK_FRAME_W, 0, WALK_FRAME_W, WALK_FRAME_H,
                        400, 300, WALK_FRAME_W * SCALE, WALK_FRAME_H * SCALE)
    update_canvas()

    frame = (frame + 1) % WALK_FRAME_COUNT
    if frame == 0:
        loop_count += 1
        if loop_count == LOOP_REPEAT:
            loop_count = 0
            delay(1)
            hero_walk = hero_walk_left if hero_walk is hero_walk_right else hero_walk_right
    delay(0.15)

close_canvas()