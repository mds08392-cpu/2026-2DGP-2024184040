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

# hero_attack_left: 2048x256, 프레임마다 크기가 다름
# (x, y, w, h) - clip_draw용 좌표 (y는 이미지 아래쪽 기준)
ATTACK_LEFT_FRAMES = [
    (30, 178, 22, 23),
    (160, 178, 21, 23),
    (294, 178, 21, 21),
    (408, 178, 62, 23),
    (541, 178, 42, 23),
    (672, 177, 36, 22),
    (805, 185, 39, 23),
    (940, 190, 33, 22),
    (1082, 176, 32, 37),
    (1210, 175, 24, 27),
    (1330, 176, 26, 22),
    (1463, 177, 27, 22),
    (1596, 177, 43, 22),
    (1737, 177, 35, 22),
    (1868, 177, 34, 22),
    (1997, 177, 34, 22),
    (77, 49, 34, 22),
    (205, 49, 34, 22),
]

ATTACK_CELL = 128  # 프레임이 원래 놓여 있던 칸 크기 (128x128)
ATTACK_COLS = 16   # 한 줄에 16칸
ATTACK_SHEET_H = 256


def attack_frame_offset(frames, index):
    """프레임의 잘라낸 영역 중심이 원래 칸 중심에서 벗어난 정도(dx, dy)를 반환."""
    x, y, w, h = frames[index]
    col, row = index % ATTACK_COLS, index // ATTACK_COLS
    cell_cx = col * ATTACK_CELL + ATTACK_CELL / 2
    cell_cy = ATTACK_SHEET_H - (row + 1) * ATTACK_CELL + ATTACK_CELL / 2  # pico2d y (아래 기준)
    return x + w / 2 - cell_cx, y + h / 2 - cell_cy


def draw_attack(image, frames, index, cx, cy, scale):
    """크기가 다른 프레임을 칸 기준 위치를 유지한 채 (cx, cy)에 그린다.
    첫 프레임의 중심이 (cx, cy)에 오도록 기준점을 맞춘다."""
    x, y, w, h = frames[index]
    ref_dx, ref_dy = attack_frame_offset(frames, 0)
    dx, dy = attack_frame_offset(frames, index)
    image.clip_draw(x, y, w, h,
                    cx + (dx - ref_dx) * scale, cy + (dy - ref_dy) * scale,
                    w * scale, h * scale)


# 모든 공격 프레임이 캔버스(800x600) 안에 들어오도록 배율과 기준점을 정한다.
ATTACK_SCALE = 12


def calc_attack_anchor(frames, scale):
    """전체 프레임이 차지하는 범위의 중앙이 캔버스 중앙에 오도록 기준점 (cx, cy)을 계산."""
    ref_dx, ref_dy = attack_frame_offset(frames, 0)
    left, right, bottom, top = 0, 0, 0, 0
    for i, (x, y, w, h) in enumerate(frames):
        dx, dy = attack_frame_offset(frames, i)
        left = min(left, dx - ref_dx - w / 2)
        right = max(right, dx - ref_dx + w / 2)
        bottom = min(bottom, dy - ref_dy - h / 2)
        top = max(top, dy - ref_dy + h / 2)
    return 400 - (left + right) / 2 * scale, 300 - (bottom + top) / 2 * scale


ATTACK_RIGHT_CX, ATTACK_RIGHT_CY = calc_attack_anchor(ATTACK_RIGHT_FRAMES, ATTACK_SCALE)
ATTACK_LEFT_CX, ATTACK_LEFT_CY = calc_attack_anchor(ATTACK_LEFT_FRAMES, ATTACK_SCALE)

# hero_walk_right / hero_walk_left: 256x49, 4프레임(각 64x49)
WALK_FRAME_W, WALK_FRAME_H = 64, 49
WALK_FRAME_COUNT = 4
SCALE = 18

LOOP_REPEAT = 5  # 애니메이션 반복 횟수 (반복 후 1초 정지)


def draw_walk_right(index):
    hero_walk_right.clip_draw(index * WALK_FRAME_W, 0, WALK_FRAME_W, WALK_FRAME_H,
                              400, 300, WALK_FRAME_W * SCALE, WALK_FRAME_H * SCALE)


def draw_walk_left(index):
    hero_walk_left.clip_draw(index * WALK_FRAME_W, 0, WALK_FRAME_W, WALK_FRAME_H,
                             400, 300, WALK_FRAME_W * SCALE, WALK_FRAME_H * SCALE)


def draw_attack_right(index):
    draw_attack(hero_attack_right, ATTACK_RIGHT_FRAMES, index,
                ATTACK_RIGHT_CX, ATTACK_RIGHT_CY, ATTACK_SCALE)


def draw_attack_left(index):
    draw_attack(hero_attack_left, ATTACK_LEFT_FRAMES, index,
                ATTACK_LEFT_CX, ATTACK_LEFT_CY, ATTACK_SCALE)


# 재생할 모션 순서: (프레임 수, 그리기 함수, 프레임 간격(초))
motions = [
    (WALK_FRAME_COUNT, draw_walk_right, 0.15),
    (WALK_FRAME_COUNT, draw_walk_left, 0.15),
    (len(ATTACK_RIGHT_FRAMES), draw_attack_right, 0.1),
    (len(ATTACK_LEFT_FRAMES), draw_attack_left, 0.1),
]

running = True
motion_index = 0
frame = 0
loop_count = 0
while running:
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False

    frame_count, draw_motion, frame_delay = motions[motion_index]

    clear_canvas()
    background.draw(400, 300)
    draw_motion(frame)
    update_canvas()

    frame = (frame + 1) % frame_count
    if frame == 0:
        loop_count += 1
        if loop_count == LOOP_REPEAT:
            loop_count = 0
            delay(1)
            motion_index = (motion_index + 1) % len(motions)
    delay(frame_delay)

close_canvas()
