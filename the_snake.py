from ctypes.wintypes import RGB
from random import choice, randint
import time
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Изгиб Питона')

# Настройка времени:
clock = pygame.time.Clock()

class Apple:
    def __init__(self):
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.body_color = APPLE_COLOR

    def draw(self, screen):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.score = 0

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head = self.positions[0]
        new_head = (head[0] + self.direction[0] * GRID_SIZE, head[1] + self.direction[1] * GRID_SIZE)

        # Обновление позиции головы змеи
        self.positions.insert(0, new_head)

        # Проверка столкновения с самим собой
        if (new_head in self.positions[1:]) or \
           (new_head[0] < 0) or (new_head[0] >= GRID_WIDTH * GRID_SIZE) or \
           (new_head[1] < 0) or (new_head[1] >= GRID_HEIGHT * GRID_SIZE):
            game_over_screen()

    def grow(self):
        self.positions.append(self.positions[-1])
        self.length += 1
        self.score += 1

    def draw(self, screen):
        for position in self.positions[:-self.length]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def check_collision(self, other):
        return self.positions[0] == other.position

def main():
    global apple
    global snake
    global font

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    apple = Apple()
    snake = Snake()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT

        snake.update_direction()
        snake.move()

        if snake.check_collision(apple):
            apple = Apple()
            snake.grow()

        apple.draw(screen)
        snake.draw(screen)

        score_text = font.render(f"Score: {snake.score}", True, RGB(255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(SPEED)

    pygame.quit()

def game_over_screen():
    screen.fill(BOARD_BACKGROUND_COLOR)

    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Game Over!', True, RGB(255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)
    screen.blit(game_over_surface, game_over_rect)

    pygame.display.flip()

    time.sleep(2)
    pygame.quit()

if __name__ == '__main__':
    main()
