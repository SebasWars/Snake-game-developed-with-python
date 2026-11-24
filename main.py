import pygame
import random

pygame.init()

HEIGTH = 600
WIDTH = 600

CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGTH // CELL_SIZE

SNAKE = [(7, 5), (6, 5), (5, 5)]
FOOD_COOR = None

BACKGROUND_COLOR = (1, 50, 32)
GRID_COLOR = (0, 80, 0)
SNAKE_HEAD_COLOR = (144, 208, 144)
SNAKE_BODY_COLOR = (144, 238, 144)
FOOD_COLOR = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGTH = (1, 0)
CURRENT_DIRECTION = RIGTH
CURRENT_SCORE = 0
LAST_SCORE_REGISTER = CURRENT_SCORE
HIHGEST_SCORE = None

GAME_STATUS = "START"

screen = pygame.display.set_mode((HEIGTH, WIDTH))
surface_grid = pygame.Surface((WIDTH, HEIGTH))
font = pygame.font.Font(None, 30)
pygame.display.set_caption("SNAKE GAME")
clock = pygame.time.Clock()
running = True

last_movement = pygame.time.get_ticks()
MOVEMENT_INTERVAL = 150


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(surface_grid, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)


def draw_snake():
    for index, (x, y) in enumerate(SNAKE):
        position_x = x * CELL_SIZE
        position_y = y * CELL_SIZE
        piece_color = SNAKE_HEAD_COLOR if index == 0 else SNAKE_BODY_COLOR

        pygame.draw.rect(
            screen, piece_color, (position_x, position_y, CELL_SIZE, CELL_SIZE), 0
        )


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

    if event == pygame.K_RIGHT:
        if change_direction_validation(CURRENT_DIRECTION, RIGTH) == True:
            CURRENT_DIRECTION = RIGTH

    if event == pygame.K_LEFT:
        if change_direction_validation(CURRENT_DIRECTION, LEFT) == True:
            CURRENT_DIRECTION = LEFT

    if event == pygame.K_UP:
        if change_direction_validation(CURRENT_DIRECTION, UP) == True:
            CURRENT_DIRECTION = UP

    if event == pygame.K_DOWN:
        if change_direction_validation(CURRENT_DIRECTION, DOWN) == True:
            CURRENT_DIRECTION = DOWN


def check_wall_colition():
    snake_head = SNAKE[0]
    x_location = snake_head[0]
    y_location = snake_head[1]

    if x_location <= 0 or x_location == COLS - 1:
        return True
    if y_location <= 0 or y_location == ROWS - 1:
        return True


def check_self_colition():
    snake_head = SNAKE[0]

    for body_part in SNAKE[1:]:
        if body_part == snake_head:
            return True
    return False


def move_snake():
    snake_head = SNAKE[0]
    new_x = snake_head[0] + CURRENT_DIRECTION[0]
    new_y = snake_head[1] + CURRENT_DIRECTION[1]
    snake_head = (new_x, new_y)

    for body_part in range(len(SNAKE) - 1, 0, -1):
        SNAKE[body_part] = SNAKE[body_part - 1]
    SNAKE[0] = snake_head


def generate_food():
    coor_x = random.randint(0, COLS - 1)
    coor_y = random.randint(0, ROWS - 1)

    food_coor = (coor_x, coor_y)
    if food_coor in SNAKE:
        return generate_food()
    else:
        return food_coor


def create_food():
    position_x = FOOD_COOR[0] * CELL_SIZE
    position_y = FOOD_COOR[1] * CELL_SIZE
    pygame.draw.rect(
        screen, FOOD_COLOR, (position_x, position_y, CELL_SIZE, CELL_SIZE), 0
    )


def eat_food():
    global FOOD_COOR
    global CURRENT_SCORE

    snake_head = SNAKE[0]
    snake_tail = SNAKE[-1]

    if snake_head == FOOD_COOR:
        FOOD_COOR = generate_food()
        x_coor = snake_tail[0] + (CURRENT_DIRECTION[0] * -1)
        y_coor = snake_tail[1] + (CURRENT_DIRECTION[1] * -1)
        new_tail = (x_coor, y_coor)
        CURRENT_SCORE += 1
        SNAKE.append(new_tail)


def restart_game():
    global SNAKE, CURRENT_DIRECTION, CURRENT_SCORE, LAST_SCORE_REGISTER, FOOD_COOR, score_text, last_movement
    SNAKE = [(7, 5), (6, 5), (5, 5)]
    CURRENT_DIRECTION = RIGTH
    CURRENT_SCORE = 0
    LAST_SCORE_REGISTER = CURRENT_SCORE
    FOOD_COOR = generate_food()
    score_text = font.render(f"Score: {CURRENT_SCORE}", True, (225, 225, 225))
    last_movement = pygame.time.get_ticks()


FOOD_COOR = generate_food()
surface_grid.fill(BACKGROUND_COLOR)
score_text = font.render(f"Score: {CURRENT_SCORE}", True, (225, 225, 225))
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
                    restart_game()
                    GAME_STATUS = "PLAYING"

    if CURRENT_SCORE != LAST_SCORE_REGISTER:
        score_text = font.render(f"Score: {CURRENT_SCORE}", True, (225, 225, 225))
        LAST_SCORE_REGISTER = CURRENT_SCORE

    if GAME_STATUS == "PLAYING":
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - last_movement

        if elapsed_time >= MOVEMENT_INTERVAL:
            move_snake()
            eat_food()
            if check_self_colition() or check_wall_colition():
                GAME_STATUS = "GAME OVER"

            last_movement = current_time

    screen.fill(BACKGROUND_COLOR)
    screen.blit(surface_grid, (0, 0))
    screen.blit(score_text, (20, 20))

    create_food()
    draw_snake()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
