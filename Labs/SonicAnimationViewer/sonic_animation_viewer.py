from pico2d import *

open_canvas()

SCALE = 4  # 원본 크기의 4배

sheet = load_image('sonic-sprite.png')  # 399 x 525

# 프레임 좌표: (x, y, w, h) - clip_draw용 (y는 이미지 아래쪽 기준)
# 동작마다 프레임 목록을 상수로 둔다.
IDLE_FRAMES = [
    (1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 29, 39), (87, 447, 29, 38),
    (118, 447, 30, 38), (150, 447, 30, 38), (182, 447, 29, 38), (211, 448, 29, 38),
    (240, 448, 29, 38), (270, 448, 24, 32), (302, 448, 29, 26),
]



def draw_frame(frames, index, cx, base_y):
    """프레임 가로 중심을 cx에, 프레임들이 공유하는 바닥선을 base_y에 맞춰 그린다.
    프레임마다 크기가 달라도 시트에서의 세로 위치를 유지해서 흔들리지 않는다."""
    x, y, w, h = frames[index]
    bottom = min(f[1] for f in frames)
    sheet.clip_draw(x, y, w, h,
                    cx, base_y + (y - bottom + h / 2) * SCALE,
                    w * SCALE, h * SCALE)


def calc_base_y(frames):
    """동작 전체 높이의 가운데가 캔버스 세로 중앙(300)에 오도록 바닥선을 계산."""
    bottom = min(f[1] for f in frames)
    top = max(f[1] + f[3] for f in frames)
    return 300 - (top - bottom) / 2 * SCALE


# 동작 2: 달리기 (12프레임)
RUN_FRAMES = [
    (8, 408, 26, 37), (37, 408, 27, 37), (65, 407, 31, 38), (97, 408, 37, 37),
    (135, 410, 32, 35), (170, 408, 32, 38), (206, 408, 26, 38), (238, 408, 24, 37),
    (263, 408, 30, 37), (295, 408, 36, 37), (334, 409, 32, 36), (370, 408, 29, 38),
]


# 동작 3: 대시 (6프레임)
DASH_FRAMES = [
    (1, 361, 33, 40), (39, 362, 35, 39), (89, 362, 35, 38), (130, 362, 34, 42),
    (181, 362, 34, 41), (228, 363, 33, 40),
]


# 동작 4: 회전 공 (9프레임)
SPIN_FRAMES = [
    (1, 326, 29, 30), (35, 327, 29, 31), (67, 327, 30, 29), (98, 327, 31, 29),
    (131, 327, 29, 30), (162, 326, 29, 31), (193, 326, 30, 29), (230, 326, 31, 29),
    (268, 325, 30, 30),
]


# 동작 5: 납작한 공 (6프레임)
SQUASH_FRAMES = [
    (1, 292, 30, 27), (36, 292, 29, 27), (70, 292, 29, 27), (105, 292, 29, 27),
    (139, 292, 29, 27), (174, 292, 29, 27),
]


# 동작 6: 붉은 잔상 달리기 시작 (6프레임)
PEEL_FRAMES = [
    (1, 251, 29, 35), (36, 251, 30, 35), (74, 251, 31, 35), (111, 251, 31, 36),
    (149, 251, 30, 35), (186, 251, 31, 36),
]


# 동작 7: 붉은 잔상 달리기 (6프레임)
SWIRL_FRAMES = [
    (1, 207, 29, 35), (36, 207, 30, 35), (72, 208, 39, 31), (123, 208, 39, 32),
    (172, 208, 39, 31), (218, 208, 38, 32),
]


# 동작 목록: (이름, 프레임 목록, 프레임 간격(초))
MOTIONS = [
    ('idle', IDLE_FRAMES, 0.1),
    ('run', RUN_FRAMES, 0.08),
    ('dash', DASH_FRAMES, 0.1),
    ('spin', SPIN_FRAMES, 0.06),
    ('squash', SQUASH_FRAMES, 0.08),
    ('peel', PEEL_FRAMES, 0.08),
    ('swirl', SWIRL_FRAMES, 0.08),
]

for name, frames, frame_delay in MOTIONS:
    base_y = calc_base_y(frames)
    for index in range(len(frames)):
        clear_canvas()
        draw_frame(frames, index, 400, base_y)
        update_canvas()
        delay(frame_delay)

close_canvas()
