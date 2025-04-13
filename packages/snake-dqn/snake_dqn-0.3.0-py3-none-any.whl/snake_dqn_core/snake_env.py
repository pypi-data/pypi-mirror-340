import pygame
import random

class SnakeGameEnv:
    def __init__(self, width=10, height=10, render_mode=False):
        self.width = width
        self.height = height
        self.render_mode = render_mode
        self.cell_size = 20

        if render_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
            pygame.display.set_caption("Snake AI")
            self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (0, -1)
        self.spawn_food()
        self.done = False
        self.score = 0
        return self.get_state()

    def spawn_food(self):
        while True:
            self.food = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1)
            )
            if self.food not in self.snake:
                break

    def step(self, action):
        if self.done:
            return self.get_state(), 0, True, {}

        self.change_direction(action)

        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        reward = 0

        # 충돌 체크
        if (new_head in self.snake) or not (0 <= new_head[0] < self.width) or not (0 <= new_head[1] < self.height):
            self.done = True
            reward = -1
            return self.get_state(), reward, self.done, {}

        self.snake.insert(0, new_head)

        if new_head == self.food:
            reward = 1
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

        # 모든 칸을 채우면 종료
        if len(self.snake) == self.width * self.height:
            self.done = True
            reward += 100  # 추가 보상

        return self.get_state(), reward, self.done, {}

    def change_direction(self, action):
        dir_x, dir_y = self.direction
        if action == 1:  # 좌회전
            self.direction = (-dir_y, dir_x)
        elif action == 2:  # 우회전
            self.direction = (dir_y, -dir_x)

    def get_state(self):
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction

        # 상대적인 방향 계산
        left_dir = (-dir_y, dir_x)
        right_dir = (dir_y, -dir_x)
        forward_dir = self.direction

        def danger_in_direction(dx, dy):
            next_x, next_y = head_x + dx, head_y + dy
            return (
                next_x < 0 or next_x >= self.width or
                next_y < 0 or next_y >= self.height or
                (next_x, next_y) in self.snake
            )

        danger_left = int(danger_in_direction(*left_dir))
        danger_right = int(danger_in_direction(*right_dir))
        danger_forward = int(danger_in_direction(*forward_dir))

        # 사과 위치 (상대적)
        food_dx = self.food[0] - head_x
        food_dy = self.food[1] - head_y

        return [
            head_x, head_y, # 뱀 머리 위치
            danger_left, danger_forward, danger_right,  # 충돌 정보
            dir_x, dir_y,  # 현재 방향
            food_dx, food_dy  # 사과 상대 위치
        ]

    def render(self):
        if not self.render_mode:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.screen.fill((0, 0, 0))

        # Draw snake
        for x, y in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        # Draw food
        food_x, food_y = self.food
        pygame.draw.rect(self.screen, (255, 0, 0), (food_x * self.cell_size, food_y * self.cell_size, self.cell_size, self.cell_size))

        pygame.display.flip()
        self.clock.tick(10)  # FPS 조절
