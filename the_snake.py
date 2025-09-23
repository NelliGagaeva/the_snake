from random import randint
import pygame
import sys

# Константы размеров и параметров
WIDTH, HEIGHT = 640, 480  # размер окна
BLOCK = 20  # размер клетки
CELL_W, CELL_H = WIDTH // BLOCK, HEIGHT // BLOCK
SPEED = 10  # FPS
# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

UP = (0, -BLOCK)
DOWN = (0, BLOCK)
LEFT = (-BLOCK, 0)
RIGHT = (BLOCK, 0)
# Скорость движения змейки
SPEED = 10


class GameObject:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def draw(self, surface):
        raise NotImplementedError


class Apple(GameObject):
    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.place_random()

    def place_random(self):
        self.pos = (
            randint(0, CELL_W - 1) * BLOCK,
            randint(0, CELL_H - 1) * BLOCK
        )

    def draw(self, surface):
        rect = pygame.Rect(self.pos, (BLOCK, BLOCK))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        mid_x = (CELL_W // 2) * BLOCK
        mid_y = (CELL_H // 2) * BLOCK
        super().__init__((mid_x, mid_y), SNAKE_COLOR)
        self.body = [self.pos]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.grow = False

    def set_direction(self):
        rev = (-self.direction[0], -self.direction[1])
        if self.next_direction and self.next_direction != rev:
            self.direction = self.next_direction
        self.next_direction = None

    def grow_snake(self):
        self.grow = True

    def advance(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(segment, (BLOCK, BLOCK))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def head_pos(self):
        return self.body[0]

    def restart(self):
        mid_x = (CELL_W // 2) * BLOCK
        mid_y = (CELL_H // 2) * BLOCK
        self.body = [(mid_x, mid_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_input(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    # Инициализация PyGame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    while True:
        handle_input(snake)
        snake.set_direction()
        snake.advance()
        clock.tick(SPEED)  # Ограничиваем FPS

        # Проверка съедания яблока
        if snake.head_pos() == apple.pos:
            snake.length += 1
            apple.place_random()

        # Проверка столкновения с самим собой
        if snake.head_pos() in snake.body[1:]:
            snake.restart()

        screen.fill(BLACK)
        # Отрисовка объектов
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
