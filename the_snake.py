import pygame
import random

# Инициализация PyGame и базовые константы
pygame.init()

# Размеры окна (например, 640x480)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20  # Размер клетки игрового поля
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Черный фон
SNAKE_COLOR = (0, 255, 0)  # Зеленый цвет змейки
APPLE_COLOR = (255, 0, 0)  # Красный цвет яблока

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для игровых объектов, включая позицию и цвет.
    """

    def __init__(self, position, body_color):
        """
        Инициализация объекта.

        :param position: кортеж (x, y) — позиция объекта
        :param body_color: цвет RGB
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Метод для отрисовки объекта.
        Переопределяется в дочерних классах.

        :param surface: поверхность для отрисовки
        """
        pass  # Базовый класс ничего не рисует


class Apple(GameObject):
    """
    Яблоко, наследующееся от GameObject.
    Представляет яблоко на игровом поле.
    """

    def __init__(self):
        """
        Инициализация яблока с случайной позицией.
        """
        super().__init__(position=(0, 0), body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает случайную позицию яблока, которая кратна GRID_SIZE и внутри экрана.
        """
        max_x = (SCREEN_WIDTH // GRID_SIZE) - 1
        max_y = (SCREEN_HEIGHT // GRID_SIZE) - 1
        self.position = (
            random.randint(0, max_x) * GRID_SIZE,
            random.randint(0, max_y) * GRID_SIZE
        )

    def draw(self, surface):
        """
        Отрисовка яблока в виде квадрата.

        :param surface: поверхность для отрисовки
        """
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """
    Класс змейки, управляет движением и отображением.
    """

    def __init__(self):
        """
        Инициализация змейки в центре.
        """
        start_x = (SCREEN_WIDTH // (2 * GRID_SIZE)) * GRID_SIZE
        start_y = (SCREEN_HEIGHT // (2 * GRID_SIZE)) * GRID_SIZE
        start_pos = (start_x, start_y)
        super().__init__(position=start_pos, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [start_pos]
        self.direction = random.choice([
            (GRID_SIZE, 0),   # вправо
            (-GRID_SIZE, 0),  # влево
            (0, GRID_SIZE),   # вниз
            (0, -GRID_SIZE)   # вверх
        ])
        self.next_direction = None
        self.last = None  # для хранения предыдущего конца

    def update_direction(self):
        """
        Обновляет направление движения, запрет разворота на 180°.
        """
        if self.next_direction:
            current_dx, current_dy = self.direction
            new_dx, new_dy = self.next_direction
            # Не позволяйте разворота на 180°
            if (current_dx + new_dx, current_dy + new_dy) != (0, 0):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки — добавляет новую голову, удаляет хвост при необходимости.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx) % SCREEN_WIDTH, (head_y + dy) % SCREEN_HEIGHT)

        # Сохраняем последний сегмент для очистки
        self.last = self.positions[-1]
        # Вставляем новую голову
        self.positions.insert(0, new_head)

        # Удаляем хвост, если длина больше текущей
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """
        Отрисовка змейки и затирание старых сегментов.
        """
        for segment in self.positions:
            rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
        # Затираем старый сегмент после перемещения
        if self.last:
            rect = pygame.Rect(self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)

    def get_head_position(self):
        """
        Возвращает текущую позицию головы.

        :return: кортеж (x, y)
        """
        return self.positions[0]

    def reset(self):
        """
        Сброс змейки в исходное состояние.
        """
        start_x = (SCREEN_WIDTH // (2 * GRID_SIZE)) * GRID_SIZE
        start_y = (SCREEN_HEIGHT // (2 * GRID_SIZE)) * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.length = 1
        self.direction = random.choice([
            (GRID_SIZE, 0), (-GRID_SIZE, 0),
            (0, GRID_SIZE), (0, -GRID_SIZE)
        ])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """
    Обработка нажатий клавиш для изменения направления змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (GRID_SIZE, 0)


def main():
    """
    Основная функция игры.
    """
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка — съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка — столкновение змейки с собой
        if len(snake.positions) != len(set(snake.positions)):
            # Змейка укусила себя — сбрасываем
            snake.reset()

        # Отрисовка элементов
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Контроль скорости
        clock.tick(20)


if __name__ == '__main__':
    main()
