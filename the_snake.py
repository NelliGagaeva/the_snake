import sys
import pygame
from random import randint

# Размеры окна
WIDTH, HEIGHT = 640, 480

# Размер клетки
BLOCK = 20

# Количество клеток по горизонтали и вертикали
CELL_W = WIDTH // BLOCK
CELL_H = HEIGHT // BLOCK

# Скорость игры (FPS)
SPEED = 10

# Направления движения
UP = (0, -BLOCK)
DOWN = (0, BLOCK)
LEFT = (-BLOCK, 0)
RIGHT = (BLOCK, 0)

# Цвета
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR = (93, 216, 228)
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Можно оставить, если понадобится

class GameObject:
    """Базовый класс для игровых объектов."""
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def draw(self, surface):
        """Метод рисования объекта. Реализуется в дочерних классах."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""
    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.place_random()

    def place_random(self):
        """Размещает яблоко в случайной позиции на игровом поле."""
        self.pos = (
            randint(0, CELL_W - 1) * BLOCK,
            randint(0, CELL_H - 1) * BLOCK
        )

    def draw(self, surface):
        """Рисование яблока."""
        rect = pygame.Rect(self.pos, (BLOCK, BLOCK))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""
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
        """Обновляет текущие направление движения змейки."""
        if self.next_direction:
            rev = (-self.direction[0], -self.direction[1])
            if self.next_direction != rev:
                self.direction = self.next_direction
        self.next_direction = None

    def grow_snake(self):
        """Увеличивает длину змейки."""
        self.grow = True

    def advance(self):
        """Двигает змейку вперед."""
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self, surface):
        """Рисование змейки."""
        for segment in self.body:
            rect = pygame.Rect(segment, (BLOCK, BLOCK))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def head_pos(self):
        """Возвращает позицию головы змейки."""
        return self.body[0]

    def restart(self):
        """Перезапуск змейки в начальную позицию."""
        mid_x = (CELL_W // 2) * BLOCK
        mid_y = (CELL_H // 2) * BLOCK
        self.body = [(mid_x, mid_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_input(snake):
    """Обработка событий пользовательского ввода."""
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
    """Основная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_input(snake)
        snake.set_direction()
        snake.advance()

        # Проверка съедания яблока
        if snake.head_pos() == apple.pos:
            snake.length += 1
            apple.place_random()

        # Проверка столкновения с самим собой
        if snake.head_pos() in snake.body[1:]:
            snake.restart()

        # Отрисовка
        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()

        clock.tick(SPEED)


if __name__ == '__main__':
    main()
