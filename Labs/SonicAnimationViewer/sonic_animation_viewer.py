from pico2d import *

open_canvas()

SCALE = 4  # 원본 크기의 4배

sheet = load_image('sonic-sprite.png')  # 399 x 525

# 프레임 좌표: (x, y, w, h) - clip_draw용 (y는 이미지 아래쪽 기준)
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


IDLE_BASE_Y = calc_base_y(IDLE_FRAMES)

frame = 0
for _ in range(33):
    clear_canvas()
    draw_frame(IDLE_FRAMES, frame, 400, IDLE_BASE_Y)
    update_canvas()
    frame = (frame + 1) % len(IDLE_FRAMES)
    delay(0.1)

close_canvas()
