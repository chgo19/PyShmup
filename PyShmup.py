"""
Module: shmup.py
Source: Learning pygame from http://kidscancode.org/lessons/

This is a shoot'em up game made from pygame.

Sound and Music
# Art from Kenney.nl at opengameart.org

"""

import pygame
import random
import os

# Define game constants
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 3000

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# reading high score each time a new game starts
high_score_file = open("shmup_highscore.txt", "r")
high_score = int(high_score_file.read())
high_score_file.close()

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("PyShmup")
pygame.mouse.set_pos([WIDTH/2, HEIGHT-30])

# import game graphics
game_dir = os.path.dirname(__file__)
img_dir = os.path.join(game_dir, "img")
sound_dir = os.path.join(game_dir, "sounds")

background_img = pygame.image.load(os.path.join(img_dir, "black.png")).convert()
background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_rect = background.get_rect()

player_img = pygame.image.load(os.path.join(img_dir, "playerShip1_orange.png")).convert()
player_lives_img = pygame.transform.scale(player_img, (25, 19))
player_lives_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(os.path.join(img_dir, "laserBlue01.png")).convert()

meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_med1.png", "meteorBrown_med3.png",
               "meteorBrown_small1.png", "meteorBrown_big4.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_dir, img)).convert())

# font to be used in draw_text function
font_name = pygame.font.match_font('arial')

explosion_animation = {}
explosion_animation['large'] = []
explosion_animation['small'] = []
explosion_animation['player'] = []
for i in range(9):
    image_name = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_dir, image_name)).convert()
    img.set_colorkey(BLACK)
    image_large = pygame.transform.scale(img, (70, 70))
    explosion_animation['large'].append(image_large)
    image_small = pygame.transform.scale(img, (35, 35))
    explosion_animation['small'].append(image_small)
    image_name = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_dir, image_name)).convert()
    img.set_colorkey(BLACK)
    explosion_animation['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(os.path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(os.path.join(img_dir, 'bolt_gold.png')).convert()

# import game sounds
shoot_sound = pygame.mixer.Sound(os.path.join(sound_dir, "pew.wav"))
shoot_sound.set_volume(0.6)

powerup_shield_sound = pygame.mixer.Sound(os.path.join(sound_dir, "pow4.wav"))
powerup_gun_sound = pygame.mixer.Sound(os.path.join(sound_dir, "pow5.wav"))

player_hit_sound = pygame.mixer.Sound(os.path.join(sound_dir, "sfx_shieldDown.ogg"))
player_hit_sound.set_volume(1)

player_die_sound = pygame.mixer.Sound(os.path.join(sound_dir, "rumble1.ogg"))

explosion_sounds = []
for sound in ["expl3.wav", "expl6.wav"]:
    explosion_sound = pygame.mixer.Sound(os.path.join(sound_dir, sound))
    explosion_sound.set_volume(0.5)
    explosion_sounds.append(explosion_sound)

pygame.mixer.music.load(os.path.join(sound_dir, "mad scientist.mp3"))
pygame.mixer.music.set_volume(1)


def draw_text(surface, text, size, x, y):
    # to draw text on a given surface
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def newmob():
    # to generate new mob
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, percent):
    # display the shield bar
    if percent < 0:
        percent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill_percent = (percent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill_percent, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 1)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_gameover_screen():
    # reading high score each time a new game start 
    high_score_file = open("shmup_highscore.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()

    screen.blit(background, background_rect)
    draw_text(screen, "pyShmup!", 64, WIDTH/2, HEIGHT/4 - 50)
    draw_text(screen, "Space to shoot and Move with arrow keys", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "OR use mouse instead", 22, WIDTH/2, HEIGHT/2+30)
    draw_text(screen, "Press SPACE to start", 16, WIDTH/2, HEIGHT * 3/4)
    draw_text(screen, "Press ESCAPE to quit", 16, WIDTH/2, HEIGHT * 3/4 + 30)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    waiting = False
                    pygame.mouse.set_visible(True)


def show_pause_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Paused", 64, WIDTH/2, HEIGHT * 1/4)
    draw_text(screen, "Press ESCAPE to resume..", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Press q to quit", 22, WIDTH/2, HEIGHT/2 + 40)
    pygame.display.flip()
    pygame.mouse.set_visible(True)
    waiting = True
    while waiting:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()


class Player(pygame.sprite.Sprite):
    # Player Sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 22
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        # check if powerup time is over
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1200:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_mov = pygame.mouse.get_rel()
        if not self.hidden:
            if mouse_mov[0] == 0:
                if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
                    self.speedx = -7
                if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
                    self.speedx = 7
                if keystate[pygame.K_SPACE] or mouse_state[0]:
                    self.shoot()
            else:
                self.rect.centerx = mouse_pos[0]

        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+200)


class Mob(pygame.sprite.Sprite):
    # Enemy sprites
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteor_images)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.8 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(3, 8)
        self.speedx = random.randrange(-3, 3)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_original, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 20 or self.rect.right < -30 or self.rect.left > WIDTH + 30:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(2, 8)
            self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):
    # Bullet sprites
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (4, 48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves of screen
        if self.rect.bottom < 0:
            self.kill()


class Power(pygame.sprite.Sprite):
    # Bullet sprites
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves of screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    # Sprites for animated explosions
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_gameover_screen()
        game_over = False
        # Initializing and adding sprites
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        pygame.mouse.set_pos([WIDTH/2, HEIGHT-30])
        pygame.mouse.set_visible(False)

        player = Player()
        all_sprites.add(player)

        for i in range(20):
            newmob()

        score = 0

    # Keep loop running at right speed
    clock.tick(FPS)
    # display_fps = "FPS: {:.2f}".format(clock.get_fps())
    pygame.display.set_caption("PyShmup - FPS: {:.2f}".format(clock.get_fps()))

    # Process inputs (events)
    for event in pygame.event.get():
        # check for closing windows
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                show_pause_screen()

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 45 - hit.radius
        random.choice(explosion_sounds).play()
        explosion = Explosion(hit.rect.center, 'large')
        all_sprites.add(explosion)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

        newmob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius
        player_hit_sound.play()
        explosion = Explosion(hit.rect.center, 'small')
        all_sprites.add(explosion)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
            pygame.mouse.set_pos([WIDTH/2, HEIGHT-30])

    # check to see if a player picked a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            powerup_shield_sound.play()
            player.shield += random.randrange(10, 40)
            if player.shield >= 100:
                player.shield = 100

        if hit.type == 'gun':
            powerup_gun_sound.play()
            player.powerup()

    # check if player lives are zero and if the explosion is going
    # alive is a pygame function just like kill
    if player.lives == 0 and not death_explosion.alive():
        score_screen = True
        while score_screen:
            clock.tick(FPS)
            screen.blit(background, background_rect)
            draw_text(screen, "Your Score", 64, WIDTH/2, HEIGHT/4 - 50)
            draw_text(screen, str(score), 26, WIDTH/2, HEIGHT/4 + 30)
            if score > high_score:
                draw_text(screen, "Yohoooo, New HIGH SCORE!", 32, WIDTH/2, HEIGHT/2)
                high_score_file = open("shmup_highscore.txt", "w")
                high_score_file.write(str(score))
                high_score_file.close()
            else:
                draw_text(screen, "Highscore", 32, WIDTH/2, HEIGHT/2)
                draw_text(screen, str(high_score), 22, WIDTH/2, HEIGHT/2+40)

            draw_text(screen, "Press SPACE to continue.", 22, WIDTH/2, HEIGHT*3/4)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        score_screen = False

        high_score = score
        game_over = True

    # Draw and Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 13)
    draw_shield_bar(screen, 15, 15, player.shield)
    draw_lives(screen, WIDTH-100, 15, player.lives, player_lives_img)

    # AFTER drawing everything flip the display
    pygame.display.flip()


# quit pygame and close everything
pygame.quit()
