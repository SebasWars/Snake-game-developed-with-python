import random
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600


CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

BACK_GROUND_COLOR = (1, 50, 32)
GRID_COLOR = (0, 80, 0)
SNAKE_HEAD_COLOR = (144, 208, 144)
SNAKE_COLOR = (108, 187, 60)
FOOD_COLOR = (255, 0, 0)
FONT_COLOR = (255, 255, 255)

SNAKE = [(12, 10), (11, 10), (10, 10), (9, 10)]
FOOD_COOR = None

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)
CURRENT_DIRECTION = RIGHT
SCORE = 0
LAST_SCORE = SCORE
GAME_STATUS = "START"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
grid_surface = pygame.Surface((WIDTH, HEIGHT))
no_game_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE GAME")

last_movement = pygame.time.get_ticks()
MOVEMENT_INTERVAL = 100

running = True
start_game_text = font.render("Press 'Space' to start", True, FONT_COLOR)
game_over_text = font.render("Game over, press 'Space' to play again", True, FONT_COLOR)


def no_game_screen():
    game_text = start_game_text if GAME_STATUS == "START" else game_over_text
    no_game_surface.fill(BACK_GROUND_COLOR)
    screen.blit(no_game_surface, (0, 0))
    screen.blit(game_text, game_text.get_rect(center=(WIDTH // 2, HEIGHT / 2)))


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            position_x = col * CELL_SIZE
            position_y = row * CELL_SIZE

            pygame.draw.rect(
                grid_surface,
                GRID_COLOR,
                (position_x, position_y, CELL_SIZE, CELL_SIZE),
                1,
            )


def draw_snake():
    for index, (x, y) in enumerate(SNAKE):
        position_x = x * CELL_SIZE
        position_y = y * CELL_SIZE
        snake_color = SNAKE_HEAD_COLOR if index == 0 else SNAKE_COLOR

        pygame.draw.rect(
            screen, snake_color, (position_x, position_y, CELL_SIZE, CELL_SIZE), 0
        )


def move_snake():
    snake_head = SNAKE[0]
    new_x_position = snake_head[0] + CURRENT_DIRECTION[0]
    new_y_position = snake_head[1] + CURRENT_DIRECTION[1]
    snake_head = (new_x_position, new_y_position)

    for body_part in range(len(SNAKE) - 1, 0, -1):
        SNAKE[body_part] = SNAKE[body_part - 1]
    SNAKE[0] = snake_head


def change_direction_validation(
    current_direction: tuple[int, int], new_direction: tuple[int, int]
):
    if (
        current_direction[0] + new_direction[0] == 0
        and current_direction[1] + new_direction[1] == 0
    ):
        return False
    return True


def handle_input(event):
    global CURRENT_DIRECTION

    if event == pygame.K_UP:
        if change_direction_validation(CURRENT_DIRECTION, UP):
            CURRENT_DIRECTION = UP
    if event == pygame.K_DOWN:
        if change_direction_validation(CURRENT_DIRECTION, DOWN):
            CURRENT_DIRECTION = DOWN
    if event == pygame.K_RIGHT:
        if change_direction_validation(CURRENT_DIRECTION, RIGHT):
            CURRENT_DIRECTION = RIGHT
    if event == pygame.K_LEFT:
        if change_direction_validation(CURRENT_DIRECTION, LEFT):
            CURRENT_DIRECTION = LEFT


def check_collision():
    snake_head = SNAKE[0]
    if snake_head[0] < 0 or snake_head[0] >= COLS:
        return True
    if snake_head[1] < 0 or snake_head[1] >= ROWS:
        return True
    return False


def check_self_collision():
    snake_head = SNAKE[0]

    for snake_part in SNAKE[1:]:
        if snake_head == snake_part:
            return True
    return False


def generate_food():
    y_position = random.randint(0, ROWS - 1)
    x_position = random.randint(0, COLS - 1)

    food_coor = (x_position, y_position)
    if food_coor in SNAKE:
        return generate_food()
    return food_coor


def draw_food():
    food_x_position = FOOD_COOR[0] * CELL_SIZE
    food_y_position = FOOD_COOR[1] * CELL_SIZE

    pygame.draw.rect(
        screen, FOOD_COLOR, (food_x_position, food_y_position, CELL_SIZE, CELL_SIZE), 0
    )


def eat_food():
    global SCORE, FOOD_COOR
    snake_head = SNAKE[0]
    snake_pre_tail = SNAKE[-2]
    snake_tail = SNAKE[-1]

    if snake_head == FOOD_COOR:
        FOOD_COOR = generate_food()
        tail_coor_x = snake_tail[0] + (snake_tail[0] - snake_pre_tail[0])
        tail_coor_y = snake_tail[1] + (snake_tail[1] - snake_pre_tail[1])
        new_tail = (tail_coor_x, tail_coor_y)
        SNAKE.append(new_tail)
        SCORE += 1


def restart_game():
    global SNAKE, CURRENT_DIRECTION, SCORE, FOOD_COOR, last_movement, score_text
    SNAKE = [(12, 10), (11, 10), (10, 10), (9, 10)]
    CURRENT_DIRECTION = RIGHT
    SCORE = 0
    FOOD_COOR = generate_food()
    score_text = font.render(f"Score: {SCORE}", True, FONT_COLOR)
    last_movement = pygame.time.get_ticks()


FOOD_COOR = generate_food()
grid_surface.fill(BACK_GROUND_COLOR)
no_game_surface.fill(BACK_GROUND_COLOR)
score_text = font.render(f"Score: {SCORE}", True, FONT_COLOR)
draw_grid()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if GAME_STATUS == "START":
                if event.key == pygame.K_SPACE:
                    GAME_STATUS = "PLAYING"
            elif GAME_STATUS == "PLAYING":
                handle_input(event.key)
            elif GAME_STATUS == "GAME OVER":
                if event.key == pygame.K_SPACE:
                    GAME_STATUS = "PLAYING"
                    restart_game()

    if SCORE != LAST_SCORE:
        score_text = font.render(f"Score: {SCORE}", True, FONT_COLOR)
        LAST_SCORE = SCORE

    if GAME_STATUS == "PLAYING":
        current_movement = pygame.time.get_ticks()
        elapsed_time = current_movement - last_movement

        if elapsed_time >= MOVEMENT_INTERVAL:
            move_snake()
            last_movement = current_movement
            eat_food()

            if check_collision() or check_self_collision():
                IS_PLAYING = False
                GAME_STATUS = "GAME OVER"

    screen.fill(BACK_GROUND_COLOR)
    screen.blit(grid_surface, (0, 0))
    draw_snake()
    draw_food()
    screen.blit(score_text, (20, 20))
    if GAME_STATUS != "PLAYING":
        no_game_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
