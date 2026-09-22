from pico2d import *
import math
open_canvas(800, 600)
grass = load_image('grass.png')
character = load_image('character.png')
x = 25
y = 80
c = 0
while c < 3:
    for i in range(0, 4):
        if i == 0:
            for j in range(0,380):
                clear_canvas()
                grass.draw(400,30)
                character.draw(x, y)
                update_canvas()
                x += 2
                delay(0.005)     
        elif i == 1:
            for j in range(0,250):
                clear_canvas()
                grass.draw(400,30)
                character.draw(x, y)
                update_canvas()
                y += 2
                delay(0.005) 
        elif i == 2:
            for j in range(0,380):
                clear_canvas()
                grass.draw(400,30)
                character.draw(x, y)
                update_canvas()
                x -= 2
                delay(0.005) 
        elif i == 3:
            for j in range(0,250):
                clear_canvas()
                grass.draw(400,30)
                character.draw(x, y)
                update_canvas()
                y -= 2
                delay(0.005)
    c += 1
#------ 원으로 움직이기----------
# import math
# open_canvas(800, 600)
# grass = load_image('grass.png')
# character = load_image('character.png')
# x = 0
# y = 0
# r = 150

# for i in range(0, 1440):
#     x = 400 + r * math.cos(math.radians(i))
#     y = 300 - r * math.sin(math.radians(i))
#     character.draw(x, y)
#     update_canvas()
#     delay(0.01)
#     clear_canvas()

# close_canvas()

