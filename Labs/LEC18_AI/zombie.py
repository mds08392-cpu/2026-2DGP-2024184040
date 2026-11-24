import random
import math

import py_trees
from py_trees.common import Access, Status
from pico2d import load_image, load_font, draw_rectangle, get_canvas_width, get_canvas_height

import common
import game_framework
import game_world

# 좀비 달리기 속력: km/h -> 픽셀/초
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 좀비 애니메이션 속도: 0.5초에 10프레임
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

ANIMATION_NAMES = ['Walk', 'Idle']


# ---------------- 행동 트리(BT) 노드 ----------------

class SetPatrolLocation(py_trees.behaviour.Behaviour):
    """행동 노드: 순찰 지점 patrol_locations[loc_no] 를 블랙보드 목적지로 기록하고 SUCCESS.
    지금 지점에 도착해 있을 때만 loc_no 를 1 늘린다(마지막 다음엔 0).
    그래서 순찰이 중간에 끊겼다가 다시 시작해도 지점을 건너뛰지 않는다."""

    def __init__(self, zombie, name='SetPatrolLocation'):
        super().__init__(name)
        self.zombie = zombie
        self.bb = self.attach_blackboard_client(name=name, namespace=zombie.bb_namespace)
        self.bb.register_key(key='target', access=Access.WRITE)

    def update(self):
        z = self.zombie
        if (z.x, z.y) == z.patrol_locations[z.loc_no]:  # 지금 지점에 도착했으면 다음 지점으로
            z.loc_no = (z.loc_no + 1) % len(z.patrol_locations)
        self.bb.target = z.patrol_locations[z.loc_no]
        return Status.SUCCESS


class MoveToTargetLocation(py_trees.behaviour.Behaviour):
    """행동 노드: 블랙보드의 목적지로 이동. 이동 중엔 RUNNING, 도착하면 SUCCESS."""

    def __init__(self, zombie, name='MoveToTargetLocation'):
        super().__init__(name)
        self.zombie = zombie
        self.bb = self.attach_blackboard_client(name=name, namespace=zombie.bb_namespace)
        self.bb.register_key(key='target', access=Access.READ)

    def update(self):
        z = self.zombie
        tx, ty = self.bb.target
        dx, dy = tx - z.x, ty - z.y
        distance = math.hypot(dx, dy)
        step = RUN_SPEED_PPS * game_framework.frame_time

        if distance <= step:  # 이번 프레임에 도착
            z.x, z.y = tx, ty
            z.speed = 0.0
            z.state = 'Idle'
            return Status.SUCCESS

        z.dir = math.atan2(dy, dx)
        z.speed = RUN_SPEED_PPS
        z.x += step * math.cos(z.dir)
        z.y += step * math.sin(z.dir)
        z.state = 'Walk'
        return Status.RUNNING

    # 중단(INVALID)되었을 때 따로 Idle 로 바꾸지 않는다.
    # Selector 가 Patrol 을 중단시키는 시점은 Chase 가 이미 이동한 뒤이므로, 여기서 Idle 로 바꾸면 덮어쓰게 된다.
    # 대신 Zombie.update() 에서 이번 tick 에 실제로 이동했는지(speed)로 Walk/Idle 을 정한다.


class IsBoyNearby(py_trees.behaviour.Behaviour):
    """조건 노드: 소년이 distance 미터 안에 있으면 SUCCESS, 아니면 FAILURE."""

    def __init__(self, zombie, distance=7.0, name='IsBoyNearby'):
        super().__init__(name)
        self.zombie = zombie
        self.range_px = distance * PIXEL_PER_METER  # 7m = 약 233px

    def update(self):
        boy = common.boy
        if boy is None:
            return Status.FAILURE
        if math.hypot(boy.x - self.zombie.x, boy.y - self.zombie.y) <= self.range_px:
            return Status.SUCCESS
        return Status.FAILURE


class MoveToBoy(MoveToTargetLocation):
    """행동 노드: 매 tick 소년의 현재 위치를 블랙보드 목적지로 기록하고 그쪽으로 이동."""

    def __init__(self, zombie, name='MoveToBoy'):
        super().__init__(zombie, name)
        self.bb.register_key(key='target', access=Access.WRITE)

    def update(self):
        self.bb.target = (common.boy.x, common.boy.y)  # 목표를 소년 위치로 갱신
        return super().update()  # 이동 코드는 MoveToTargetLocation 과 동일


class Zombie:
    images = None
    font = None
    marker_image = None
    count = 0  # 블랙보드 네임스페이스 구분용

    def load_images(self):
        if Zombie.images is None:
            Zombie.images = {
                name: [load_image(f'./zombie/{name} ({i}).png') for i in range(1, 11)]
                for name in ANIMATION_NAMES
            }
            Zombie.font = load_font('ENCR10B.TTF', 40)
            Zombie.marker_image = load_image('hand_arrow.png')

    def __init__(self, x=None, y=None):
        self.load_images()
        self.x = x if x is not None else random.randint(100, get_canvas_width() - 100)
        self.y = y if y is not None else random.randint(100, get_canvas_height() - 100)
        self.dir = 0.0  # 이동 방향 (라디안)
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0  # 주운 공의 개수

        # 순찰 지점: 1->5 로 갔다가 같은 길로 돌아온다 (마지막 다음엔 처음으로).
        self.patrol_locations = [(43, 274), (1118, 274), (1050, 494), (575, 804),
                                 (235, 991), (575, 804), (1050, 494), (1118, 274)]
        self.loc_no = 0  # 지금 가고 있는 순찰 지점 번호

        # 블랙보드: 좀비마다 별도의 네임스페이스를 사용한다.
        Zombie.count += 1
        self.bb_namespace = f'/zombie{Zombie.count}'
        self.bb = py_trees.blackboard.Client(name=f'Zombie{Zombie.count}', namespace=self.bb_namespace)
        self.bb.register_key(key='target', access=Access.READ)  # 목적지는 BT 노드가 기록한다.

        self.build_behavior_tree()

    def build_behavior_tree(self):
        # Selector 'ChaseOrPatrol' (memory=False): 왼쪽 자식부터 시도한다.
        #   1) Chase  - 소년이 근처에 있으면 추적 (우선순위 높음)
        #   2) Patrol - 추적이 FAILURE 일 때만 순찰 지점을 차례로 돈다
        # 매 tick 왼쪽(Chase)부터 다시 검사하므로, 순찰 중에 소년이 다가오면 순찰을 중단하고 바로 추적한다.
        root = py_trees.composites.Selector(name='ChaseOrPatrol', memory=False, children=[
            self.build_chase_sequence(),   # 왼쪽 = 우선순위 높음
            self.build_patrol_sequence(),
        ])
        self.bt = py_trees.trees.BehaviourTree(root)

    def build_patrol_sequence(self):
        # 순찰 지점 설정 -> 그 지점으로 이동 (memory=True: 이동 중엔 MoveTo 부터 이어서 실행)
        # 도착하면 시퀀스가 SUCCESS 로 끝나고, 다음 tick 에 다음 순찰 지점을 고른다.
        return py_trees.composites.Sequence(name='Patrol', memory=True, children=[
            SetPatrolLocation(self),
            MoveToTargetLocation(self),
        ])

    def build_chase_sequence(self):
        # 소년 추적: 소년이 근처에 있으면 -> 소년에게 이동
        # memory=False: 매 tick 조건부터 다시 검사하므로, 소년이 멀어지면 바로 추적을 멈춘다.
        return py_trees.composites.Sequence(name='Chase', memory=False, children=[
            IsBoyNearby(self, 7.0),
            MoveToBoy(self),
        ])

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION
        self.speed = 0.0  # 이번 tick 에 이동 노드가 실행되면 speed 가 설정된다.
        self.bt.tick()  # 행동 트리 실행
        self.state = 'Walk' if self.speed > 0 else 'Idle'

    def draw(self):
        image = Zombie.images[self.state][int(self.frame)]
        if math.cos(self.dir) < 0:  # 왼쪽을 향하고 있으면 좌우 반전
            image.composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            image.draw(self.x, self.y, 100, 100)
        Zombie.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        if self.bb.exists('target'):  # 블랙보드에 기록된 목적지
            tx, ty = self.bb.target
            Zombie.marker_image.draw(tx + 25, ty - 25)  # 목적지에 손가락 마커 표시
        draw_rectangle(*self.get_bb())

    # 바운딩 박스: (left, bottom, right, top)
    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.ball_count += 1


class BlackboardView:
    """좀비의 블랙보드 내용(목적지)을 칠판 이미지 위에 적어 보여주는 UI."""
    image = None
    title_font = None
    font = None

    def __init__(self, zombie, x=200, y=None):
        if BlackboardView.image is None:
            BlackboardView.image = load_image('blackboard.png')  # 360 x 170
            BlackboardView.title_font = load_font('ENCR10B.TTF', 24)
            BlackboardView.font = load_font('ENCR10B.TTF', 36)
        self.zombie = zombie
        self.x = x
        self.y = y if y is not None else get_canvas_height() - 100

    def update(self):
        pass

    def draw(self):
        BlackboardView.image.draw(self.x, self.y)
        left = self.x - 150
        BlackboardView.title_font.draw(left, self.y + 40, f'{self.zombie.bb_namespace}/target', (200, 230, 200))
        bb = self.zombie.bb
        text = f'({int(bb.target[0])}, {int(bb.target[1])})' if bb.exists('target') else '(none)'
        BlackboardView.font.draw(left, self.y - 15, text, (255, 255, 255))
