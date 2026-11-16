from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    image = None

    def __init__(self, x, y, direction=1, speed=10):
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y-20
        self.direction = 1
        self.speed = 0
        self.velocity = 0
        self.set_velocity(direction, speed)

    def set_velocity(self, direction, speed):
        """방향(-1: 왼쪽, 1: 오른쪽)과 속도 크기를 입력받아 설정하고 출력한다."""
        self.direction = 1 if direction >= 0 else -1
        self.speed = abs(speed)
        self.velocity = self.direction * self.speed

    def update(self):
        self.x += self.velocity
        if self.x < -10 or self.x > get_canvas_width() + 10:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
