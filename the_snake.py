from random import choice, randint

import pygame

# Константы размеров экрана и сетки
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость обновления
SPEED = 20

# Инициализация Pygame
pygame.init()

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()

# Константный словарь для обработки клавиш
KEY_DIRECTION_MAP = {
    (pygame.K_UP,): UP,
    (pygame.K_DOWN,): DOWN,
    (pygame.K_LEFT,): LEFT,
    (pygame.K_RIGHT,): RIGHT,
}


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализация объекта"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта."""


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        """Инициализация яблока с рандомной позицией."""
        self.occupied_positions = occupied_positions or []
        position = self.randomize_position()
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self):
        """Генерирует случайную позицию для яблока."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (x, y)
            if new_position not in self.occupied_positions:
                return new_position

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи."""

    def __init__(self):
        """Инициализация змеи в центре экрана и установка атрибутов."""
        super().__init__(body_color=SNAKE_COLOR)  # Установка цвета змеи
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змею по текущему направлению."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.last = self.positions[-1]
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовка змеи и ее следов."""
        if hasattr(self, 'last') and self.last:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает параметры змеи."""
        self.length = 1
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        initial_position = (center_x, center_y)
        self.positions = [initial_position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обработка нажатий клавиш для изменения направления змеи."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            for keys, direction in KEY_DIRECTION_MAP.items():
                if event.key in keys:
                    snake.next_direction = direction
    return True


def main():
    """Основная функция запуска игры."""
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)
    running = True
    while running:
        clock.tick(SPEED)

        # Обработка событий
        if not handle_keys(snake):
            running = False

        snake.update_direction()
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(
                occupied_positions=snake.positions
            )

        # Проверка столкновения с телом
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position(
                occupied_positions=snake.positions
            )

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
