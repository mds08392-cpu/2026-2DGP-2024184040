from pico2d import *

open_canvas()

sheet = load_image('sonic-sprite.png')  # 399 x 525

# 프레임 좌표: (x, y, w, h) - clip_draw용 (y는 이미지 아래쪽 기준)
IDLE_FRAMES = [
    (1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 29, 39), (87, 447, 29, 38),
    (118, 447, 30, 38), (150, 447, 30, 38), (182, 447, 29, 38), (211, 448, 29, 38),
    (240, 448, 29, 38), (270, 448, 24, 32), (302, 448, 29, 26),
]

frame = 0
for _ in range(33):
    clear_canvas()
    x, y, w, h = IDLE_FRAMES[frame]
    sheet.clip_draw(x, y, w, h, 400, 300)
    update_canvas()
    frame = (frame + 1) % len(IDLE_FRAMES)
    delay(0.1)

close_canvas()
