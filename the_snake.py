
import pygame
import random

# Инициализация PyGame
pygame.init()

# Константы размеров окна и сетки
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для объектов с позицией и цветом."""

    def __init__(self, position, body_color):
        """
        :param position: Tuple[int, int], координаты (x, y)
        :param body_color: Tuple[int, int, int], цвет RGB
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Общий метод-отрисовка — переопределяется в наследниках."""
        pass


class Apple(GameObject):
    """Яблоко на поле."""

    def __init__(self):
        """Создает яблоко в случайной позиции."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию по сетке."""
        max_x = (SCREEN_WIDTH // GRID_SIZE) - 1
        max_y = (SCREEN_HEIGHT // GRID_SIZE) - 1
        self.position = (
            random.randint(0, max_x) * GRID_SIZE,
            random.randint(0, max_y) * GRID_SIZE
        )

    def draw(self, surface):
        """Рисует яблоко как квадрат."""
        rect = pygame.Rect(
            self.position[0], self.position[1], GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Змейка: управление, движение и отрисовка."""

    def __init__(self):
        """Инициализация змейки в центре экрана."""
        half_width = SCREEN_WIDTH // 2
        start_x = (half_width // GRID_SIZE) * GRID_SIZE
        half_height = SCREEN_HEIGHT // 2
        start_y = (half_height // GRID_SIZE) * GRID_SIZE
        super().__init__((start_x, start_y), SNAKE_COLOR)
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = random.choice([
            (GRID_SIZE, 0),
            (-GRID_SIZE, 0),
            (0, GRID_SIZE),
            (0, -GRID_SIZE)
        ])
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Меняет направление, запрещая разворот на 180°."""
        if not self.next_direction:
            return
        dx, dy = self.direction
        ndx, ndy = self.next_direction
        if (dx + ndx, dy + ndy) != (0, 0):
            self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        """Сдвигает змейку на один шаг по направлению."""
        head = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head[0] + dx) % SCREEN_WIDTH,
            (head[1] + dy) % SCREEN_HEIGHT
        )
        self.last = self.positions[-1]
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Рисует каждый сегмент змейки и «стирает» старый хвост."""
        for seg in self.positions:
            rect = pygame.Rect(seg[0], seg[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
        if self.last:
            rect = pygame.Rect(self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в исходное состояние."""
        half_width = SCREEN_WIDTH // 2
        start_x = (half_width // GRID_SIZE) * GRID_SIZE
        half_height = SCREEN_HEIGHT // 2
        start_y = (half_height // GRID_SIZE) * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.length = 1
        self.direction = random.choice([
            (GRID_SIZE, 0),
            (-GRID_SIZE, 0),
            (0, GRID_SIZE),
            (0, -GRID_SIZE)
        ])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия стрелок для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type != pygame.KEYDOWN:
            continue
        if event.key == pygame.K_UP:
            snake.next_direction = (0, -GRID_SIZE)
        elif event.key == pygame.K_DOWN:
            snake.next_direction = (0, GRID_SIZE)
        elif event.key == pygame.K_LEFT:
            snake.next_direction = (-GRID_SIZE, 0)
        elif event.key == pygame.K_RIGHT:
            snake.next_direction = (GRID_SIZE, 0)


def main():
    """Запуск основного цикла игры."""
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка на столкновение со своим хвостом
        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
