import pygame
import pygame_menu
import random
import sys
import pygame.mixer

def init_game():
    pygame.init()
    pygame.mixer.init()

init_game()

eat_sound = pygame.mixer.Sound("apple_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")

snake_color1 = (160, 82, 45)
snake_color2 = (0, 255, 0)
food_colors = [(255, 0, 0), (255, 255, 0), (0, 0, 255), (128, 0, 128)]
text_color = (0, 0, 0)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake by dulkin')

clock = pygame.time.Clock()
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

snake_block_size = 20
snake_speed = 15
initial_snake_length = 1

food_size = 20

background_image = pygame.image.load("background_image.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

main_menu = pygame_menu.Menu('Snake by dulkin', screen_width, screen_height, theme=pygame_menu.themes.THEME_BLUE)

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def draw_snake(snake_block, snake_list, color):
    for segment in snake_list:
        pygame.draw.rect(screen, color, [segment[0], segment[1], snake_block, snake_block])

def display_message(msg, color, y_displacement=0):
    message = font_style.render(msg, True, color)
    screen.blit(message, [screen_width / 6, screen_height / 3 + y_displacement])

def generate_food(snake_list1, snake_list2=None):
    while True:
        food_x = round(random.randrange(0, screen_width - food_size) / 20.0) * 20.0
        food_y = round(random.randrange(0, screen_height - food_size) / 20.0) * 20.0
        if snake_list2:
            if (food_x, food_y) not in snake_list1 and (food_x, food_y) not in snake_list2:
                return food_x, food_y, random.choice(food_colors)
        else:
            if (food_x, food_y) not in snake_list1:
                return food_x, food_y, random.choice(food_colors)

def display_score(score, x_offset=0):
    value = score_font.render("Score: " + str(score), True, text_color)
    screen.blit(value, [screen_width - 150 + x_offset, 10])

def check_self_collision(x, y, snake_list):
    for segment in snake_list[:-1]:
        if round(segment[0]) == round(x) and round(segment[1]) == round(y):
            return True
    return False

def check_collision_with_other_snake(snake_list1, snake_list2):
    for segment in snake_list2:
        if round(segment[0]) == round(snake_list1[-1][0]) and round(segment[1]) == round(snake_list1[-1][1]):
            return True
    return False

def adventure_loop(single_player=False):
    adventure_over = False
    winner_message = ""

    # Snake 1 initial settings
    x1 = 3 * screen_width / 4 if not single_player else screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0
    snake_list1 = []
    for _ in range(initial_snake_length):
        snake_list1.append([x1, y1])
    score1 = 0

    # Snake 2 initial settings
    if not single_player:
        x2 = screen_width / 4
        y2 = screen_height / 2
        x2_change = 0
        y2_change = 0
        snake_list2 = []
        for _ in range(initial_snake_length):
            snake_list2.append([x2, y2])
        score2 = 0

    food_x, food_y, food_color = generate_food(snake_list1, snake_list2 if not single_player else None)

    while not adventure_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                adventure_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    adventure_over = True
                    break
                # Snake 1 controls
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block_size
                    x1_change = 0

                if not single_player:
                    # Snake 2 controls
                    if event.key == pygame.K_a and x2_change == 0:
                        x2_change = -snake_block_size
                        y2_change = 0
                    elif event.key == pygame.K_d and x2_change == 0:
                        x2_change = snake_block_size
                        y2_change = 0
                    elif event.key == pygame.K_w and y2_change == 0:
                        y2_change = -snake_block_size
                        x2_change = 0
                    elif event.key == pygame.K_s and y2_change == 0:
                        y2_change = snake_block_size
                        x2_change = 0

        if adventure_over:
            break

        # Move snakes
        x1 += x1_change
        y1 += y1_change
        if not single_player:
            x2 += x2_change
            y2 += y2_change

        # Check for collisions with the wall
        if x1 < 0 or x1 >= screen_width or y1 < 0 or y1 >= screen_height:
            adventure_over = True
            winner_message = "SNAKE2 WINNER!" if not single_player else "GAME OVER!"
        if not single_player and (x2 < 0 or x2 >= screen_width or y2 < 0 or y2 >= screen_height):
            adventure_over = True
            winner_message = "SNAKE1 WINNER!"

        # Check for self collisions
        if check_self_collision(x1, y1, snake_list1):
            adventure_over = True
            winner_message = "SNAKE2 WINNER!" if not single_player else "GAME OVER!"
        if not single_player and check_self_collision(x2, y2, snake_list2):
            adventure_over = True
            winner_message = "SNAKE1 WINNER!"

        # Check for collisions with the other snake
        if not single_player and check_collision_with_other_snake(snake_list1, snake_list2):
            adventure_over = True
            winner_message = "SNAKE2 WINNER!"
        if not single_player and check_collision_with_other_snake(snake_list2, snake_list1):
            adventure_over = True
            winner_message = "SNAKE1 WINNER!"

        # Update snake lists
        snake_head1 = [x1, y1]
        snake_list1.append(snake_head1)
        if len(snake_list1) > score1 + initial_snake_length:
            del snake_list1[0]

        if not single_player:
            snake_head2 = [x2, y2]
            snake_list2.append(snake_head2)
            if len(snake_list2) > score2 + initial_snake_length:
                del snake_list2[0]

        # Check for food collisions
        if x1 == food_x and y1 == food_y:
            score1 += 1
            eat_sound.play()
            food_x, food_y, food_color = generate_food(snake_list1, snake_list2 if not single_player else None)

        if not single_player and x2 == food_x and y2 == food_y:
            score2 += 1
            eat_sound.play()
            food_x, food_y, food_color = generate_food(snake_list1, snake_list2)

        # Draw everything
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, food_color, [food_x, food_y, food_size, food_size])
        draw_snake(snake_block_size, snake_list1, snake_color1)
        if not single_player:
            draw_snake(snake_block_size, snake_list2, snake_color2)
        display_score(score1)
        if not single_player:
            display_score(score2, x_offset=-150)
        pygame.display.update()

        clock.tick(snake_speed)

    if winner_message:
        game_over_sound.play()
        display_message(winner_message, text_color)
        pygame.display.update()
        pygame.time.delay(2000)
    go_to_main_menu(snake_list1, snake_list2 if not single_player else None)

def start_single_player_game():
    main_menu.disable()
    adventure_loop(single_player=True)

def start_two_player_game():
    main_menu.disable()
    adventure_loop(single_player=False)

def exit_the_game():
    pygame.quit()
    sys.exit()

def go_to_main_menu(snake_list1, snake_list2=None):
    snake_list1.clear()
    if snake_list2:
        snake_list2.clear()
    main_menu.enable()

main_menu.add.button('Играть одному', start_single_player_game)
main_menu.add.button('Играть вдвоем', start_two_player_game)
main_menu.add.button('Выйти из игры', exit_the_game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background_image, (0, 0))
    main_menu.mainloop(screen)
    pygame.display.flip()
