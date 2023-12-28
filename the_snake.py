from typing import List, Tuple, Optional
from random import randint

import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
CENTER_POINT: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения
UP: tuple = (0, -1)
DOWN: tuple = (0, 1)
LEFT: tuple = (-1, 0)
RIGHT: tuple = (1, 0)

# Словарь для изменения направления
CONTROL_DICT = {
    (LEFT, pygame.K_UP): UP,
    (RIGHT, pygame.K_UP): UP,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_DOWN): DOWN,
    (UP, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_LEFT): LEFT,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_RIGHT): RIGHT
}

# Цвета фона - черный
BOARD_BACKGROUND_COLOR: tuple = (0, 0, 0)
APPLE_COLOR: tuple = (255, 0, 0)
SNAKE_COLOR: tuple = (0, 255, 0)
AROUND_BLOCK_COLOR: tuple = (93, 216, 228)

# Толщина линий
THICKNESS_COLOR: int = 1

# Скорость движения змейки
SPEED = 10

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


# Тут опишите все классы игры
class GameObject:
    """Родительский класс от которого наследуются классы: Apple, Snake"""

    def __init__(
        self, body_color=BOARD_BACKGROUND_COLOR, position=CENTER_POINT
    ):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Это абстрактный метод, который предназначен для переопределения
        в дочерних классах. Этот метод должен определять, как объект будет
        отрисовываться на экране
        """
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, AROUND_BLOCK_COLOR, rect, THICKNESS_COLOR)


class Apple(GameObject):
    """Дочерний класс GameObject, описывающий змейку"""

    def __init__(self, positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None
        self.randomize_position(positions)

    def draw(self):
        """Отрисовывает яблоко в игре."""
        super().draw(screen)

    def randomize_position(
        self, positions: Optional[List[Tuple[int, int]]] = None
    ) -> None:
        """Метод отвечающий за случайное появление яблока на экране."""
        positions = positions or []

        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in positions:
                break
        self.position = new_position


class Snake(GameObject):
    """Дочерний класс GameObject, описывающий змейку"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.head = []
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self, next_direction=None):
        """Метод обновления направления после нажатия на кнопку."""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Метод обновления позиции змейки."""
        head = self.get_head_position()
        new_width = (head[0] + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH
        new_height = (head[1] + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        self.positions.insert(0, (new_width, new_height))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(
                surface, AROUND_BLOCK_COLOR, rect, THICKNESS_COLOR
            )

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(
            surface, AROUND_BLOCK_COLOR, head_rect, THICKNESS_COLOR
        )

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает текущее положение головы змейки"""
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой
        """
        self.direction = RIGHT
        self.length = 1
        self.positions = [self.position]
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            return CONTROL_DICT.get(
                (game_object.direction, event.key),
                game_object.direction
            )


def main():
    """Описана основная логика игры"""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        snake.update_direction(handle_keys(snake))
        snake.move()
        apple.draw()
        snake.draw(screen)
        for match in snake.positions[2:]:
            if snake.positions[0] == match and snake.positions[0] == match:
                Snake.reset(snake)
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            apple = Apple(snake.positions)
        pygame.display.update()


if __name__ == '__main__':
    main()
