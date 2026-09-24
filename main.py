import pygame
import random

# ============================================================
# INITIALIZATION
# ============================================================

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

try:
    pygame.mixer.init()
    print("Audio system started successfully!")
except Exception as e:
    print("Audio error:", e)

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

clock = pygame.time.Clock()


# ============================================================
# AUDIO LOAD
# ============================================================

try:
    game_over_sound = pygame.mixer.Sound("failing.wav")
except Exception as e:
    print("Could not load failing.wav:", e)
    game_over_sound = None

try:
    hit_sound = pygame.mixer.Sound("hit.wav")
except Exception as e:
    print("Could not load hit.wav:", e)
    hit_sound = None


# ============================================================
# FONTS
# ============================================================

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)


# ============================================================
# PLAYER
# ============================================================

player_x = 375
player_y = 520

player_width = 50
player_height = 50

player_speed = 5


# ============================================================
# BULLETS
# ============================================================

bullets = []

bullet_speed = 7


# ============================================================
# ENEMIES
# ============================================================

enemies = []

enemy_width = 40
enemy_height = 40

enemy_speed = 3


# ============================================================
# SCORE AND LIVES
# ============================================================

score = 0
lives = 3


# ============================================================
# GAME STATE
# ============================================================

game_over = False


# ============================================================
# STARS
# ============================================================

stars = []

for i in range(80):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.randint(1, 3)

    stars.append([x, y, speed])


# ============================================================
# EXPLOSIONS
# ============================================================

explosions = []


# ============================================================
# RESTART FUNCTION
# ============================================================

def reset_game():
    global player_x, player_y, score, lives, game_over
    player_x = 375
    player_y = 520
    bullets.clear()
    enemies.clear()
    explosions.clear()
    score = 0
    lives = 3
    game_over = False


# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True

while running:

    # Button Rectangles for Game Over screen (160x50 pixels)
    restart_btn_rect = pygame.Rect(WIDTH // 2 - 170, 360, 150, 50)
    quit_btn_rect = pygame.Rect(WIDTH // 2 + 20, 360, 150, 50)

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:
            running = False

        # Mouse clicks on Game Over buttons
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if restart_btn_rect.collidepoint(mouse_pos):
                reset_game()
            elif quit_btn_rect.collidepoint(mouse_pos):
                running = False

        # Keyboard events
        if event.type == pygame.KEYDOWN:

            # Shoot bullet
            if event.key == pygame.K_SPACE and not game_over:
                bullet_x = player_x + player_width // 2 - 3
                bullet_y = player_y

                bullets.append([bullet_x, bullet_y])

            # Restart / Quit with keys on Game Over
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False


    # ========================================================
    # GAME LOGIC
    # ========================================================

    if not game_over:

        # ----------------------------------------------------
        # PLAYER MOVEMENT
        # ----------------------------------------------------

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Keep player inside screen
        if player_x < 0:
            player_x = 0

        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width


        # ----------------------------------------------------
        # MOVE STARS
        # ----------------------------------------------------

        for star in stars:
            star[1] += star[2]

            if star[1] > HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, WIDTH)


        # ----------------------------------------------------
        # CREATE ENEMIES
        # ----------------------------------------------------

        if random.randint(1, 50) == 1:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy_y = -enemy_height

            enemies.append([enemy_x, enemy_y])


        # ----------------------------------------------------
        # MOVE BULLETS
        # ----------------------------------------------------

        for bullet in bullets:
            bullet[1] -= bullet_speed

        bullets = [
            bullet
            for bullet in bullets
            if bullet[1] > 0
        ]


        # ----------------------------------------------------
        # INCREASE DIFFICULTY
        # ----------------------------------------------------

        current_enemy_speed = enemy_speed + score // 100


        # ----------------------------------------------------
        # MOVE ENEMIES
        # ----------------------------------------------------

        for enemy in enemies:
            enemy[1] += current_enemy_speed


        # ----------------------------------------------------
        # BULLET-ENEMY COLLISION
        # ----------------------------------------------------

        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(
                bullet[0],
                bullet[1],
                6,
                15
            )

            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(
                    enemy[0],
                    enemy[1],
                    enemy_width,
                    enemy_height
                )

                if bullet_rect.colliderect(enemy_rect):
                    if bullet in bullets:
                        bullets.remove(bullet)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 10

                    # PLAY HIT SOUND
                    if hit_sound:
                        hit_sound.play()

                    explosions.append([
                        enemy[0] + 20,
                        enemy[1] + 20,
                        1
                    ])

                    break


        # ----------------------------------------------------
        # PLAYER-ENEMY COLLISION
        # ----------------------------------------------------

        player_rect = pygame.Rect(
            player_x,
            player_y,
            player_width,
            player_height
        )

        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(
                enemy[0],
                enemy[1],
                enemy_width,
                enemy_height
            )

            if player_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                lives -= 1

                explosions.append([
                    player_x + 25,
                    player_y + 25,
                    1
                ])

                if lives <= 0:
                    game_over = True
                    if game_over_sound:
                        game_over_sound.play()


        # ----------------------------------------------------
        # ENEMIES THAT REACH THE BOTTOM
        # ----------------------------------------------------

        for enemy in enemies[:]:
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                lives -= 1

                if lives <= 0 and not game_over:
                    game_over = True
                    if game_over_sound:
                        game_over_sound.play()


        # ----------------------------------------------------
        # UPDATE EXPLOSIONS
        # ----------------------------------------------------

        for explosion in explosions[:]:
            explosion[2] += 2

            if explosion[2] > 25:
                explosions.remove(explosion)


    # ========================================================
    # DRAW BACKGROUND
    # ========================================================

    screen.fill((5, 5, 30))


    # ========================================================
    # DRAW STARS
    # ========================================================

    for star in stars:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (star[0], star[1]),
            2
        )


    # ========================================================
    # DRAW PLAYER
    # ========================================================

    if not game_over:
        pygame.draw.polygon(
            screen,
            (0, 200, 255),
            [
                (player_x + 25, player_y),
                (player_x, player_y + 50),
                (player_x + 50, player_y + 50)
            ]
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (player_x + 25, player_y + 30),
            7
        )


    # ========================================================
    # DRAW BULLETS
    # ========================================================

    for bullet in bullets:
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (
                bullet[0],
                bullet[1],
                6,
                15
            )
        )


    # ========================================================
    # DRAW ENEMIES
    # ========================================================

    for enemy in enemies:
        pygame.draw.circle(
            screen,
            (255, 50, 50),
            (
                enemy[0] + 20,
                enemy[1] + 20
            ),
            20
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (
                enemy[0] + 13,
                enemy[1] + 15
            ),
            4
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (
                enemy[0] + 27,
                enemy[1] + 15
            ),
            4
        )


    # ========================================================
    # DRAW EXPLOSIONS
    # ========================================================

    for explosion in explosions:
        pygame.draw.circle(
            screen,
            (255, 150, 0),
            (
                explosion[0],
                explosion[1]
            ),
            explosion[2]
        )


    # ========================================================
    # SCORE
    # ========================================================

    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        score_text,
        (10, 10)
    )


    # ========================================================
    # LIVES
    # ========================================================

    lives_text = font.render(
        f"Lives: {lives}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        lives_text,
        (WIDTH - 120, 10)
    )


    # ========================================================
    # GAME OVER SCREEN WITH RESTART AND QUIT BUTTONS
    # ========================================================

    if game_over:
        game_over_text = big_font.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        final_score_text = font.render(
            f"Final Score: {score}",
            True,
            (255, 255, 255)
        )

        # Draw Game Over and Final Score
        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, 200)
        )

        screen.blit(
            final_score_text,
            (WIDTH // 2 - final_score_text.get_width() // 2, 280)
        )

        # Draw Restart Button (Green)
        pygame.draw.rect(screen, (40, 180, 90), restart_btn_rect, border_radius=8)
        restart_lbl = font.render("Restart (R)", True, (255, 255, 255))
        screen.blit(
            restart_lbl,
            (
                restart_btn_rect.centerx - restart_lbl.get_width() // 2,
                restart_btn_rect.centery - restart_lbl.get_height() // 2
            )
        )

        # Draw Quit Button (Red)
        pygame.draw.rect(screen, (220, 60, 60), quit_btn_rect, border_radius=8)
        quit_lbl = font.render("Quit (Q)", True, (255, 255, 255))
        screen.blit(
            quit_lbl,
            (
                quit_btn_rect.centerx - quit_lbl.get_width() // 2,
                quit_btn_rect.centery - quit_lbl.get_height() // 2
            )
        )


    # ========================================================
    # UPDATE SCREEN
    # ========================================================

    pygame.display.update()

    clock.tick(60)


# ============================================================
# QUIT
# ============================================================

pygame.quit()