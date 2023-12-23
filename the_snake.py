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

# Направления движения
UP: tuple = (0, -1)
DOWN: tuple = (0, 1)
LEFT: tuple = (-1, 0)
RIGHT: tuple = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR: tuple = (0, 0, 0)
APPLE_COLOR: tuple = (255, 0, 0)
SNAKE_COLOR: tuple = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


# Тут опишите все классы игры
class GameObject:
    """Родительский класс от которого наследуются классы: Apple, Snake"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

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
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Apple(GameObject):
    """Дочерний класс GameObject, описывающий змейку"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None
        self.randomize_position()

    def draw(self):
        """Отрисовывает яблоко в игре."""
        super().draw(screen)

    def randomize_position(self):
        """Устанавливает случайную позицию для яблок в игре."""
        self.position = (randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE
                         )


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

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, position):
        """Обновляет позицию змейки"""
        self.head = self.get_head_position(self.positions)

        if self.head[0] >= SCREEN_WIDTH:
            self.head = (-20, self.head[1])
        elif self.head[0] < 0:
            self.head = (SCREEN_WIDTH, self.head[1])

        if self.head[1] >= SCREEN_HEIGHT:
            self.head = (self.head[0], 0)
        elif self.head[1] < 0:
            self.head = (self.head[0], SCREEN_HEIGHT)

        if self.direction is UP:
            self.positions.insert(
                0, (self.head[0], self.head[1] - GRID_SIZE)
            )
        elif self.direction is RIGHT:
            self.positions.insert(
                0, (self.head[0] + GRID_SIZE, self.head[1])
            )
        elif self.direction is DOWN:
            self.positions.insert(
                0, (self.head[0], self.head[1] + GRID_SIZE)
            )
        elif self.direction is LEFT:
            self.positions.insert(
                0, (self.head[0] - GRID_SIZE, self.head[1])
            )

        self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    @staticmethod
    def get_head_position(positions) -> tuple:
        """Возвращает текущее положение головы змейки"""
        return positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой
        """
        self.direction = RIGHT
        self.length = 1
        self.positions = [self.position]
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описана основная логика игры"""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        apple.draw()
        snake.draw(screen)
        for match in snake.positions[2:]:
            if snake.positions[0] == match and snake.positions[0] == match:
                Snake.reset(snake)
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()
