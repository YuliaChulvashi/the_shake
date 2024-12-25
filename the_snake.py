import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BLACK = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

class Apple:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)
        self.body_color = APPLE_COLOR

    def random_position(self, snake_positions):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                        random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if position not in snake_positions:
                return position

    def draw(self, screen):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.score = 0

    def update_direction(self):
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head = self.positions[0]
        new_head = (head[0] + self.direction[0] * GRID_SIZE, head[1] + self.direction[1] * GRID_SIZE)

        self.positions.insert(0, new_head)

        if (new_head in self.positions[1:]) or \
           (new_head[0] < 0) or (new_head[0] >= GRID_WIDTH * GRID_SIZE) or \
           (new_head[1] < 0) or (new_head[1] >= GRID_HEIGHT * GRID_SIZE):
            game_over_screen()

        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        self.length += 1
        self.score += 1

    def draw(self, screen):
        for position in self.positions:
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
    pygame.display.set_caption('Изгиб Питона')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    snake = Snake()
    apple = Apple(snake.positions)

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
            snake.grow()
            apple = Apple(snake.positions)

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)

        score_text = font.render(f"Score: {snake.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(SPEED)

    pygame.quit()

def game_over_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)

    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Game Over!', True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)
    screen.blit(game_over_surface, game_over_rect)

    pygame.display.flip()

    waiting_for_exit = True
    while waiting_for_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_exit = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

if __name__ == '__main__':
    main()
