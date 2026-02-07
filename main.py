import os
import pygame, random
pygame.init()
pygame.mixer.init()
score_sound = pygame.mixer.Sound("score.wav")
death_sound = pygame.mixer.Sound("death.wav")
music_file = "music.mp3"
try:
    pygame.mixer.music.load(music_file)
except pygame.error:
    music_file = "music.wav"
    pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1)
'''
Welcome to PA0 – Flappy Bird! Throughout this code, you are going to find a recreation of a game you have probably
heard of before. This is an introductory assignment designed to help you familiarize yourself with what you can expect 
in future PAs. In this PA, you will barely need to code—mostly just tweaking some variable values and implementing
fewer than five lines of new code. It is recommended that you read through the code and the comments explaining 
some of the game mechanics.
'''
# Setup the screen -->
screen = pygame.display.set_mode((400, 600))
bg = pygame.image.load("bg.png").convert()
bg = pygame.transform.scale(bg, screen.get_size())
ground = pygame.image.load("ground.png").convert_alpha()
ground_y = screen.get_height() - ground.get_height()
ground_x = 0
ground_width = ground.get_width()
ground_tiles = (screen.get_width() // ground_width) + 2
bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (50, 50))
bird_width, bird_height = bird_img.get_size()
pipe_top_img = pygame.image.load("pipe_top.png").convert_alpha()
pipe_bottom_img = pygame.image.load("pipe_bottom.png").convert_alpha()

pygame.display.set_caption("Flappy Birds")

HIGH_SCORE_FILE = "highscore.txt"
if os.path.exists(HIGH_SCORE_FILE):
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as high_score_file:
            high_score = int(high_score_file.read().strip() or 0)
    except ValueError:
        high_score = 0
else:
    high_score = 0

def save_high_score(value):
    with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as high_score_file:
        high_score_file.write(str(value))

# Colors -->
# NOTE: This is in the RGB (Red, Green, Blue) format
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PLAYER = (0, 128, 255)
SKY = (135, 206, 235)
SUN = (255, 223, 0)
CLOUD = (245, 245, 245)
GROUND = (110, 76, 35)
GROUND_HEIGHT = 70

# Font Size -->
big_font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 30)

# Text Coordinates -->
title_x = 50
title_y = 150

instruction_x = 80
instruction_y = 550

score_x = 200
score_y = 10

# Player Variables -->
player_count = 1
mode_selected = False

def setup_players(count):
    global player_count, bird_start_x, bird_start_y, bird_x, bird_y, bird_velocity, bird_alive, scores, passed_pipe
    player_count = count
    bird_start_x = [50, 110][:count]
    bird_start_y = [200, 200][:count]
    bird_x = bird_start_x[:]
    bird_y = bird_start_y[:]
    bird_velocity = [10] * count
    bird_alive = [True] * count
    scores = [0] * count
    passed_pipe = [False] * count

setup_players(player_count)
# TODO 1: Tweaking the physics
# Looks like the player is falling too quickly not giving a change to flap it's wing, maybe tweak around with the value of this variable
gravity = 0.5
jump = -8
# Pipe Variables -->
pipe_x = 200
pipe_width = 70
# TODO 2.1: A Little gap Problem
# You probably noticed when running the code that it's impossible the player to go through the gaps
# play around with the pipe_gap variable so that its big enough for the player to pass through
pipe_gap = 150
pipe_height = random.randint(100, 400)
# TODO 2.2: The too fast problem
# The pipes are moving way too fast! Play around with the pipe_speed variable until you find a good
# speed for the player to play in!
pipe_speed = 6

base_pipe_speed = pipe_speed
base_pipe_gap = pipe_gap
base_gravity = gravity
DIFFICULTY_SETTINGS = {
    "Easy": {
        "pipe_speed": max(3, base_pipe_speed - 1),
        "pipe_gap": base_pipe_gap + 20,
        "gravity": max(0.3, base_gravity - 0.1),
    },
    "Medium": {
        "pipe_speed": base_pipe_speed,
        "pipe_gap": base_pipe_gap,
        "gravity": base_gravity,
    },
    "Hard": {
        "pipe_speed": base_pipe_speed + 1,
        "pipe_gap": max(80, base_pipe_gap - 20),
        "gravity": base_gravity + 0.1,
    },
}

difficulty = "Easy"
pipe_speed = DIFFICULTY_SETTINGS[difficulty]["pipe_speed"]
pipe_gap = DIFFICULTY_SETTINGS[difficulty]["pipe_gap"]
gravity = DIFFICULTY_SETTINGS[difficulty]["gravity"]
next_pipe_gap = pipe_gap

death_sound_played = False
game_over = False
game_started = False

clock = pygame.time.Clock()

running = True
while running:
    restart_requested = False
    # TODO 6: Changing the name!
    # D'oh! This is not yout name isn't follow the detailed instructions on the PDF to complete this task.
    name = "Homer Simpson"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not mode_selected:
                if event.key == pygame.K_1:
                    setup_players(1)
                    mode_selected = True
                elif event.key == pygame.K_2:
                    setup_players(2)
                    mode_selected = True
                if mode_selected:
                    pipe_x = 200
                    pipe_height = random.randint(100, 400)
                    difficulty = "Easy"
                    pipe_speed = DIFFICULTY_SETTINGS[difficulty]["pipe_speed"]
                    pipe_gap = DIFFICULTY_SETTINGS[difficulty]["pipe_gap"]
                    gravity = DIFFICULTY_SETTINGS[difficulty]["gravity"]
                    next_pipe_gap = pipe_gap
                    death_sound_played = False
                    game_over = False
                    game_started = False
            else:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        restart_requested = True
                    else:
                        if game_started == False:
                            game_started = True
                        if bird_alive[0]:
                            bird_velocity[0] = jump
                if player_count > 1 and event.key == pygame.K_UP:
                    if game_over:
                        restart_requested = True
                    else:
                        if game_started == False:
                            game_started = True
                        if bird_alive[1]:
                            bird_velocity[1] = jump

    if restart_requested:
        setup_players(player_count)
        pipe_x = 700
        pipe_height = random.randint(100, 400)
        difficulty = "Easy"
        pipe_speed = DIFFICULTY_SETTINGS[difficulty]["pipe_speed"]
        pipe_gap = DIFFICULTY_SETTINGS[difficulty]["pipe_gap"]
        gravity = DIFFICULTY_SETTINGS[difficulty]["gravity"]
        next_pipe_gap = pipe_gap
        death_sound_played = False
        game_over = False
        game_started = False

    if mode_selected and game_started == True and game_over == False:
        max_score = max(scores) if scores else 0
        if max_score >= 10:
            difficulty = "Hard"
        elif max_score >= 5:
            difficulty = "Medium"
        else:
            difficulty = "Easy"

        pipe_speed = DIFFICULTY_SETTINGS[difficulty]["pipe_speed"]
        gravity = DIFFICULTY_SETTINGS[difficulty]["gravity"]
        next_pipe_gap = DIFFICULTY_SETTINGS[difficulty]["pipe_gap"]

        for i in range(player_count):
            if bird_alive[i]:
                bird_velocity[i] = bird_velocity[i] + gravity
                bird_y[i] = bird_y[i] + bird_velocity[i]

        pipe_x = pipe_x - pipe_speed
        for i in range(player_count):
            if bird_alive[i] and not passed_pipe[i] and pipe_x + pipe_width < bird_x[i]:
                scores[i] += 1
                score_sound.play()
                passed_pipe[i] = True
                if scores[i] > high_score:
                    high_score = scores[i]
                    save_high_score(high_score)

        if pipe_x < -70:
            pipe_x = 400
            pipe_height = random.randint(100, 400)
            pipe_gap = next_pipe_gap
            passed_pipe = [False] * player_count
            # TODO 4: Fixing the scoring
            # When you pass through the pipes the score should be updated to the current score + 1. Implement the
            # logic to accomplish this scoring system.

        for i in range(player_count):
            if bird_alive[i] and (bird_y[i] + bird_height > 600 or bird_y[i] < 0):
                bird_alive[i] = False

        if not any(bird_alive):
            game_over = True

    rotated_birds = []
    bird_rects = []
    for i in range(player_count):
        tilt = max(-45, min(25, -bird_velocity[i] * 3))
        rotated = pygame.transform.rotate(bird_img, tilt)
        rect = rotated.get_rect(center=(bird_x[i] + bird_width // 2, bird_y[i] + bird_height // 2))
        rotated_birds.append(rotated)
        bird_rects.append(rect)

    if mode_selected and game_started == True and game_over == False:
        top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe_rect = pygame.Rect(
            pipe_x,
            pipe_height + pipe_gap,
            pipe_width,
            screen.get_height() - (pipe_height + pipe_gap)
        )

        for i in range(player_count):
            if bird_alive[i] and (
                bird_rects[i].colliderect(top_pipe_rect)
                or bird_rects[i].colliderect(bottom_pipe_rect)
            ):
                bird_alive[i] = False

        if not any(bird_alive):
            game_over = True

    if game_over and not death_sound_played:
        death_sound.play()
        death_sound_played = True

    screen.fill(SKY)
    screen.blit(bg, (0, 0))

    for i in range(ground_tiles):
        screen.blit(ground, (ground_x + i * ground_width, ground_y))
    ground_x -= pipe_speed
    if ground_x <= -ground_width:
        ground_x += ground_width

    # TODO 5: A Bird's Color
    # The color of the player is currently white, let's change that a bit! You are free to change the bird's
    # to whatever you wish. You will need to head back to where the PLAYER variable was created and change the values.
    for i in range(player_count):
        screen.blit(rotated_birds[i], bird_rects[i].topleft) # Drawing the bird (You don't need to touch this line!)
    top_pipe_scaled = pygame.transform.scale(pipe_top_img, (pipe_width, pipe_height))
    bottom_pipe_height = screen.get_height() - (pipe_height + pipe_gap)
    if bottom_pipe_height > 0:
        bottom_pipe_scaled = pygame.transform.scale(
            pipe_bottom_img,
            (pipe_width, bottom_pipe_height)
        )
        screen.blit(bottom_pipe_scaled, (pipe_x, pipe_height + pipe_gap))
    screen.blit(top_pipe_scaled, (pipe_x, 0))
    if player_count == 1:
        score_text = small_font.render(f"Score: {scores[0]}", True, WHITE)
    else:
        score_text = small_font.render(f"P1: {scores[0]}  P2: {scores[1]}", True, WHITE)
    high_text = small_font.render(f"High: {high_score}  {difficulty}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 35))

    if mode_selected == False: # Start UI -->
        title_text = big_font.render("Flappy Bird", True, WHITE)
        instruction_text = small_font.render("Press 1 for Single Player", True, WHITE)
        instruction_text_2 = small_font.render("Press 2 for Multiplayer", True, WHITE)
        screen.blit(title_text, (title_x, title_y))
        screen.blit(instruction_text, (instruction_x, instruction_y - 30))
        screen.blit(instruction_text_2, (instruction_x, instruction_y))
    elif game_started == False:
        title_text = big_font.render("Flappy Bird", True, WHITE)
        instruction_text = small_font.render("Press Space to start", True, WHITE)
        screen.blit(title_text, (title_x, title_y))
        screen.blit(instruction_text, (instruction_x, instruction_y))
        if player_count > 1:
            instruction_text_2 = small_font.render("P2: Up Arrow", True, WHITE)
            screen.blit(instruction_text_2, (instruction_x, instruction_y + 30))

    if game_over: # GameOver UI -->
        loss_text = small_font.render("Press Space to restart...", True, WHITE)
        screen.blit(loss_text, (85, 200))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
