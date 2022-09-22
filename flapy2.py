import pygame
import sys
from pygame.constants import K_ESCAPE, K_SPACE, KEYDOWN, QUIT
import random


def draw_base():
    SCREEN.blit(BASE, (base_x, 575))
    # for second upcoming base we add width of screen
    SCREEN.blit(BASE, (base_x + 386, 575))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    # newpipe = PIPE.get_rect(midtop = (700,random_pipe_pos))
    bottompipe = PIPE.get_rect(midtop=(700, random_pipe_pos))
    toppipe = PIPE.get_rect(midbottom=(700, random_pipe_pos - 220))
    # return tuple so unpack this tuple
    return bottompipe, toppipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes


def draw_pipes(pipes):
    # bottom pipe can cross screen height
    for pipe in pipes:
        if pipe.bottom >= 660:
            SCREEN.blit(PIPE, pipe)
        else:
            flip_pipe = pygame.transform.rotate(PIPE, 180)
            # or pygame.transform.flip(PIPE, T/F(flip in x direction -F) ,T/F(flip in y direction -T))
            SCREEN.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        # in build func to check for collision
        if BIRD_RECT.colliderect(pipe):
            #    print("collide")
            hit_sound.play()
            return False

    if BIRD_RECT.top <= -1 or BIRD_RECT.bottom >= 576:
        #   print("collide base")
        return False
    return True


def rotate_bird(bird):
    # negative to rotate in downword direction
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*1.8, 1)
    return new_bird


def display_score(game_status):  # pass string of gime is over or not
    if game_status == "main_game":
        SCORE = game_font.render(str(int(score)), True, (255, 255, 255))
        SCORE_RECT = SCORE.get_rect(center=(190, 100))
        SCREEN.blit(SCORE, SCORE_RECT)

    if game_status == "game_over":
        SCORE = game_font.render(
            f'Score : {int(score)}', True, (235, 235, 235))
        SCORE_RECT = SCORE.get_rect(center=(190, 50))
        SCREEN.blit(SCORE, SCORE_RECT)

        HIGH_SCORE = game_font.render(
            f'High Score : {int(high_score)}', True, (235, 235, 235))
        HIGH_SCORE_RECT = HIGH_SCORE.get_rect(center=(190, 600))
        SCREEN.blit(HIGH_SCORE, HIGH_SCORE_RECT)


def update_hi_score(scor, hi_score):
    if (scor) > (hi_score):
        hi_score = scor
    return hi_score

# it play sound late (after few mili sec of function call) so we make usable before init so it will not be late
#pygame.mixer.pre_init(frequency=44100 ,size= 16 ,channels= 1,buffer= 1024)


pygame.init()
SCREEN = pygame.display.set_mode((386, 660))
clock = pygame.time.Clock()
# print(clock)
game_font = pygame.font.Font('flappy game/04B_19.TTF', 35)

# --------------- game variables
gravity = 0.25
bird_movement = 0

game_active = False
game_first = True  # it is playing for first time so not show scores

score = -0.86
high_score = 0

HOMESCREEN = pygame.image.load(
    'flappy game/images/vishal_homescreenn.png').convert_alpha()

BGROUND = pygame.image.load('flappy game/images/background.png').convert()
# BGROUND = pygame.transform.scale2x(BGROUND)

BASE = pygame.image.load('flappy game/images/ground2.png').convert_alpha()
base_x = 0

BIRD = pygame.image.load(
    'flappy game/images/mini_ghost bird.png').convert_alpha()
BIRD_RECT = BIRD.get_rect(center=(120, 288))

PIPE = pygame.image.load('flappy game/images/pipe2.png').convert_alpha()

pipe_list = []
# USEREVENT is alse like even tin -event loop- it not trigger by mouse or keyboard
# its triggered by timer
SPAWNPIPE = pygame.USEREVENT
pipe_height = [500, 470, 450, 430, 400, 370, 350, 330, 300, 270, 250]

# create timer
# pygame.time.set_timer( -event- , - time (milisec))
pygame.time.set_timer(SPAWNPIPE, 1600)  # 1.2 sec


# ----------------------------- sounds
flap_sound = pygame.mixer.Sound('flappy game/sounds/lol/sfx_wing.wav')
die_sound = pygame.mixer.Sound('flappy game/sounds/lol/sfx_die.wav')
point_sound = pygame.mixer.Sound('flappy game/sounds/lol/sfx_point.wav')
hit_sound = pygame.mixer.Sound('flappy game/sounds/lol/sfx_hit.wav')
score_sound_time = 150

while True:
    for event in pygame.event.get():
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            # its work when game is active
            if event.key == K_SPACE and game_active:

                # it will fall down always by gravity so do bird movent 0
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()

        if event.type == KEYDOWN:
            # its work when game is not active
            if event.key == K_SPACE and game_active == False:
                game_active = True
                game_first = False
                score = -0.9  # re initilize from start
                base_x = 0
                score_sound_time = 150

                # reset pipes and bird positon and moment when you lose game
                pipe_list.clear()
                BIRD_RECT.center = (120, 288)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            # print(SPAWNPIPE)
            # to unpack use extend
            pipe_list.extend(create_pipe())
            # print(pipe_list)

    SCREEN.blit(HOMESCREEN, (0, 0))
    #SCREEN.blit(BGROUND, (0, 0))

# ---------------------- this logic run while game is not over  -------------------
    if game_active:
        # ----------------------- display screen
        SCREEN.blit(BGROUND, (0, 0))

        #-----------------------   bird
        # by add gravety in position in y birds go to down
        bird_movement += gravity

        rotated_bird = rotate_bird(BIRD)
        SCREEN.blit(rotated_bird, BIRD_RECT)

        BIRD_RECT.centery += bird_movement
        # now check for up key

        # SCREEN.blit(BIRD,BIRD_RECT)

        game_active = check_collision(pipe_list)

        #-----------------------   pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # ----------------------- score
        display_score("main_game")
        score += 0.01
        score_sound_time -= 1
        if score_sound_time <= -2:
            point_sound.play()
            score_sound_time = 120

    #-----------------------   base
        base_x -= 4
        # base_x += 50 # and frame rate decrease it moves in part

        # fuction to moved the base into left direction
        draw_base()
        # SCREEN.blit(BASE,(base_x,575))
        # after 2 base moved we re initilaized base_x
        if base_x <= -386:
            base_x = 0

    else:
        high_score = update_hi_score(score, high_score)
        if game_first == False:
            display_score("game_over")

    pygame.display.update()
    clock.tick(60)
    # clock.tick(1)
