import pygame
import sys
import random

# Константы размеров и параметров
WIDTH, HEIGHT = 640, 480  # размер окна
BLOCK = 20  # размер клетки
CELL_W, CELL_H = WIDTH // BLOCK, HEIGHT // BLOCK 
SPEED = 10  # FPS

# Цвета
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR = (93, 216, 228)

UP = (0, -BLOCK)
DOWN = (0, BLOCK)
LEFT = (-BLOCK, 0)
RIGHT = (BLOCK, 0)


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

    def place_random(self, snake_body=None):
        """Разместить яблоко в случайной клетке,
        не совпадающей с змейкой"""
        while True:
            x = random.randint(0, CELL_W - 1) * BLOCK
            y = random.randint(0, CELL_H - 1) * BLOCK
            if snake_body and (x, y) in snake_body:
                continue
            self.pos = (x, y)
            break

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

    def set_direction(self):
        if self.next_direction:
            # Не разрешаем двигаться в обратном направлении
            rev_dir = (-self.direction[0], -self.direction[1])
            if self.next_direction != rev_dir:
                self.direction = self.next_direction
            self.next_direction = None

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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка")
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
            apple.place_random(snake.body)  

        # Проверка столкновения с самим собой
        if snake.head_pos() in snake.body[1:]:
            snake.restart()

        # Отрисовка
        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()

        clock.tick(SPEED)


if __name__ == "__main__":
    main()
        
           



    
        
