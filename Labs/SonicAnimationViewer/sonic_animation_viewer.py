from pico2d import *

open_canvas()

sheet = load_image('sonic-sprite.png')  # 399 x 525

# 동작 줄 위치를 확인하기 위해 시트를 4배로 그려 본다 (임시)
clear_canvas()
sheet.draw(399 * 4 // 2, 300, 399 * 4, 525 * 4)
update_canvas()
delay(1)

close_canvas()
