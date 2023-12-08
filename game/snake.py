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

snake_color = (160, 82, 45)
food_color = (255, 0, 0)
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

def draw_epic_snake(snake_block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, snake_color, [segment[0], segment[1], snake_block, snake_block])

def display_epic_message(msg, color, y_displacement=0):
    message = font_style.render(msg, True, color)
    screen.blit(message, [screen_width / 6, screen_height / 3 + y_displacement])

def generate_epic_food(snake_list):
    food_x = round(random.randrange(0, screen_width - food_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, screen_height - food_size) / 20.0) * 20.0
    if (food_x, food_y) not in snake_list:
        return food_x, food_y

def display_epic_score(score):
    value = score_font.render("Score: " + str(score), True, text_color)
    screen.blit(value, [screen_width - 150, 10])

def check_self_collision(x, y, snake_list):
    for segment in snake_list[:-1]:
        if round(segment[0]) == round(x) and round(segment[1]) == round(y):
            return True
    return False

def epic_adventure_loop():
    adventure_over = False
    x1 = screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    for _ in range(initial_snake_length):
        snake_list.append([x1, y1])

    food_x, food_y = generate_epic_food(snake_list)
    score = 0

    while not adventure_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                adventure_over = True
            if event.type == pygame.KEYDOWN:
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

        x1 += x1_change
        y1 += y1_change

        if x1 < 0 or x1 >= screen_width or y1 < 0 or y1 >= screen_height:
            adventure_over = True

        if check_self_collision(x1, y1, snake_list):
            adventure_over = True

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > score + initial_snake_length:
            del snake_list[0]

        if x1 == food_x and y1 == food_y:
            score += 1
            eat_sound.play()
            food_x, food_y = generate_epic_food(snake_list)

        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, food_color, [food_x, food_y, food_size, food_size])
        draw_epic_snake(snake_block_size, snake_list)
        display_epic_score(score)
        pygame.display.update()

        clock.tick(snake_speed)

    game_over_sound.play()
    go_to_main_menu(snake_list)

def start_the_game():
    main_menu.disable()
    epic_adventure_loop()

def exit_the_game():
    pygame.quit()
    sys.exit()

def go_to_main_menu(snake_list):
    snake_list.clear()
    main_menu.enable()

main_menu.add.button('Начать игру', start_the_game)
main_menu.add.button('Выйти из игры', exit_the_game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background_image, (0, 0))
    main_menu.mainloop(screen)
    pygame.display.flip()