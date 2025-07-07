import pygame ,random

pygame.init()

#display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Catch Mobile")

#set Fps and Clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 3
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

#Set colors
Green = (0,255,0)
DarkGreen = (10,50,10)
White = (255,255,255)
Black = (0,0,0)

#Set Font
font = pygame.font.Font('assets/AttackGraffiti.ttf',32)

#Set text
score_text = font.render("Score: "+str(score),True,Green,DarkGreen)
score_rect = score_text.get_rect()
score_rect.topleft = (10,16)

title_text = font.render('Catch The Book',True,Green,DarkGreen)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

lives_text = font.render("Lives: "+str(player_lives),True,Green,DarkGreen)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH,25)

game_over_text = font.render("GAME OVER",True,Green,DarkGreen)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play game again!",True,Green,DarkGreen)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2+32,WINDOW_HEIGHT//2+32)

#Set sound and music
coin_sound = pygame.mixer.Sound('assets/bonus.wav')
coin_sound.set_volume(3)
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(0.2)

bg_music = pygame.mixer.music.load('assets/ftd_background_music.wav')
pygame.mixer.music.set_volume(0.3)

#Set images
coin_image = pygame.image.load('assets/book.png')
coin_image = pygame.transform.scale(coin_image,(64,64))
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64,WINDOW_HEIGHT-32)

player_image = pygame.image.load('assets/teacher.png')
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2

nadu_image = pygame.image.load('assets/mobile.png')
nadu_image = pygame.transform.scale(nadu_image,(64,64))
nadu_image_rect = nadu_image.get_rect()
nadu_image_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2-50)


background = pygame.image.load('assets/bg.png')


#main game loop
pygame.mixer.music.play(-1,0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_rect.top >64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_s] and player_rect.bottom <WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY
    
    #Move the coin
    if coin_rect.x <0:
        #Player missed the coin
        player_lives-=1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH+BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WINDOW_HEIGHT-32)
    else:
        #Move the coin
        coin_rect.x -= coin_velocity
    
    #Check for collisons
    if player_rect.colliderect(coin_rect):
        score+=1
        coin_sound.play()
        coin_velocity+=COIN_ACCELERATION
        coin_rect.x = WINDOW_HEIGHT+BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WINDOW_HEIGHT-32)
    
    #Update Hud
    score_text = font.render("Score: "+str(score),True,Green,DarkGreen)
    lives_text = font.render("Lives: "+str(player_lives),True,Green,DarkGreen)

    #Check for game over
    if player_lives <=0:
        display_surface.blit(nadu_image,nadu_image_rect)
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        
        pygame.display.update()

        #Pause the game until player press key than reset game.
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #The player wants to play again?
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT//2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1)
                    is_paused = False
                #The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    #fill the display
    display_surface.fill((0,0,0))
    #background
    display_surface.blit(background,(0,0))

    #Blit Hud to the scree
    display_surface.blit(score_text,score_rect)
    display_surface.blit(lives_text,lives_rect)
    display_surface.blit(title_text,title_rect)
    pygame.draw.line(display_surface,White,(0,64),(WINDOW_WIDTH,64),2)

    #Blit assets
    display_surface.blit(player_image,player_rect)
    display_surface.blit(coin_image,coin_rect)

    #update display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()