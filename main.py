import random
import sys
import pygame

# Global vars
FPS = 32
SCREENWIDTH = 300
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND_Y = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'resources/bird.png'
BACKGROUND = 'resources/background.png'
PIPE = 'resources/pipe.png'


def welcome_screen():
    player_x = int(SCREENWIDTH/5)
    player_y = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    message_x = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    message_y = int(SCREENHEIGHT*0.13)
    base_x = 0

    while True:
        for event in pygame.event.get():
            # Exit the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Start when player presses space
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
                SCREEN.blit(GAME_SPRITES['message'], (message_x, message_y))
                SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)


def main_game():
    # Init the game
    score = 0
    player_x = int(SCREENWIDTH / 5)
    player_y = int(SCREENWIDTH / 2)
    basex = 0

    # Create some pipes
    new_pipe1 = get_random_pipe()
    new_pipe2 = get_random_pipe()

    # Upper pipes
    upper_pipes = [
        {'x': SCREENWIDTH + 200, 'y': new_pipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe2[0]['y']},
    ]
    # Lower pipes
    lower_pipes = [
        {'x': SCREENWIDTH + 200, 'y': new_pipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe2[1]['y']},
    ]

    # Define speed/movement settings
    pipe_vel_x = -4

    player_vel_y = -9
    player_max_vel_y = 10
    player_acc_y = 1

    player_flap_acc_v = -8  # speed while flapping
    player_flapped = False

    while True:
        # Main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if player_y > 0:
                    player_vel_y = player_flap_acc_v
                    player_flapped = True

        # Check if player collides/crashes
        crash_test = is_collide(player_x, player_y, upper_pipes, lower_pipes)

        if crash_test:
            return

        # Check/update score
        player_mid_pos = player_x + GAME_SPRITES['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f"Your score is {score}")

        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False
        player_height = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(player_vel_y, GROUND_Y - player_y - player_height)

        # Move the pipes/playing field
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            upperPipe['x'] += pipe_vel_x
            lowerPipe['x'] += pipe_vel_x

        # Add a new pipe
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        # Remove a pipe if it's off-screen
        if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        # Blit the background and pipe sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def is_collide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > GROUND_Y - 25 or player_y < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upper_pipes:
        pipe_height = GAME_SPRITES['pipe'][0].get_height()
        if player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            return True

    for pipe in lower_pipes:
        if (player_y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            return True

    return False


def get_random_pipe():
    # Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREENWIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},  # upper Pipe
        {'x': pipe_x, 'y': y2}  # lower Pipe
    ]
    return pipe


if __name__ == '__main__':
    # Main
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    GAME_SPRITES['message'] = pygame.image.load('resources/title.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('resources/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha())

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome_screen()
        main_game()
