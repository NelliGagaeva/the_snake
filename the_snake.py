import pygame
import random
import sys
# Константы для размера экрана и клетки
WIDTH, HEIGHT = 640, 480
BLOCK = 20
CELL_W, CELL_H = WIDTH // BLOCK, HEIGHT // BLOCK
SPEED = 10  # частота обновлений 


class GameObject:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def draw(self, surface):
        raise NotImplementedError


class Apple(GameObject):
    def __init__(self):
        super().__init__((0, 0), (255, 0, 0))
        self.place_random()

    def place_random(self):
        x = random.randint(0, CELL_W - 1) * BLOCK
        y = random.randint(0, CELL_H - 1) * BLOCK
        self.pos = (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (*self.pos, BLOCK, BLOCK))


class Snake(GameObject):
    def __init__(self):
        start_x = (WIDTH // 2 // BLOCK) * BLOCK
        start_y = (HEIGHT // 2 // BLOCK) * BLOCK
        super().__init__((start_x, start_y), (0, 255, 0))
        self.body = [self.pos]
        self.length = 1
        self.vel = (BLOCK, 0)
        self.want_dir = None

    def set_direction(self):
        if self.want_dir:
            # Запрет на движение назад
            rev = (-self.vel[0], -self.vel[1])
            if self.want_dir != rev:
                self.vel = self.want_dir
            self.want_dir = None

    def advance(self):
        head_x, head_y = self.body[0]
        dx, dy = self.vel
        new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, (*segment, BLOCK, BLOCK))

    def head_pos(self):
        return self.body[0]

    def restart(self):
        mid_x = (WIDTH // 2 // BLOCK) * BLOCK
        mid_y = (HEIGHT // 2 // BLOCK) * BLOCK
        self.body = [(mid_x, mid_y)]
        self.length = 1
        self.vel = (BLOCK, 0)
        self.want_dir = None


def handle_input(snake):
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP:
                snake.want_dir = (0, -BLOCK)
            elif ev.key == pygame.K_DOWN:
                snake.want_dir = (0, BLOCK)
            elif ev.key == pygame.K_LEFT:
                snake.want_dir = (-BLOCK, 0)
            elif ev.key == pygame.K_RIGHT:
                snake.want_dir = (BLOCK, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    bg_color = (0, 0, 0)

    # Создаём змейку и яблоко
    snake = Snake()
    apple = Apple()

    while True:
        handle_input(snake)
        snake.set_direction()
        snake.advance()

        # Проверка на съедание яблока
        if snake.head_pos() == apple.pos:
            snake.length += 1
            apple.place_random()

        # Самоудар — рестарт
        if snake.head_pos() in snake.body[1:]:
            snake.restart()

        screen.fill(bg_color)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()

        clock.tick(SPEED)


if __name__ == '__main__':
    main()
