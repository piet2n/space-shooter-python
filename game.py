import pygame as pg
from moviepy import *
# GAME OVER YEEEEEEEEEEEAH
basespeed = 1
class Alien:
    def __init__(self, x, y, image,speed=basespeed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


def setup():

    pg.init()
    clock = pg.time.Clock()

    screen = pg.display.set_mode((400,600))
    pg.display.set_caption("Space Shooter")

    # Load images
    ship_images = [pg.image.load(f"images/ship_{i}.png") for i in range(3)]
    alien_images = [pg.image.load(f"images/alien_{i}.png") for i in range(2)]

    ship_x, ship_y = 200, 500
    ship_w, ship_h = ship_images[0].get_rect().size

    aliens = []
    wave = 0
    for i in range(5):
        aliens.append(Alien(50*i + 50, 0, alien_images[0],speed=1))
        aliens.append(Alien(50*i + 50, 50, alien_images[0],speed=1))

    alien_w, alien_h = alien_images[0].get_rect().size

    projectiles = []
    projectile_w, projectile_h = 4, 8

    left_pressed = False
    right_pressed = False
    projectile_fired = False

    sound_laser = pg.mixer.Sound("sounds/laser.wav")
    font_scoreboard = pg.font.Font("fonts/PressStart2P-Regular.ttf", 20)

    return (clock, screen, ship_images, alien_images, ship_x, ship_y, ship_w, ship_h,
            aliens, wave, alien_w, alien_h, projectiles, projectile_w, projectile_h,
            left_pressed, right_pressed, projectile_fired, sound_laser, font_scoreboard, False)

# Setup game variables
(clock, screen, ship_images, alien_images, ship_x, ship_y, ship_w, ship_h,
 aliens, wave, alien_w, alien_h, projectiles, projectile_w, projectile_h,
 left_pressed, right_pressed, projectile_fired, sound_laser, font_scoreboard, closedwindows) = setup()

score = 0
tick = 0
running = True

while running:
    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            closedwindows = True
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_LEFT:
                left_pressed = True
            elif event.key == pg.K_RIGHT:
                right_pressed = True
            elif event.key == pg.K_SPACE:
                projectile_fired = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                left_pressed = False
            elif event.key == pg.K_RIGHT:
                right_pressed = False

    # Update aliens
    for alien in aliens:
        alien.update()

    # Death detection
    ship_rect = pg.Rect(ship_x, ship_y, ship_w, ship_h)
    for alien in aliens:
        if ship_rect.colliderect(alien.rect):
            running = False
            break

    # Move ship
    if left_pressed:
        ship_x -= 8
        if ship_x < 0:
            ship_x = 0
    if right_pressed:
        ship_x += 8
        if ship_x > screen.get_width() - ship_w:
            ship_x = screen.get_width() - ship_w
    for alien in aliens:
        if alien.y > 600:
            running = False

    # Fire projectile
    if projectile_fired:
        sound_laser.play()
        projectiles.append({'x': ship_x + ship_w/2 - projectile_w/2, 'y': ship_y})
        projectile_fired = False

    # Update projectiles
    for projectile in reversed(projectiles):
        projectile['y'] -= 8
        if projectile['y'] < 0:
            projectiles.remove(projectile)

    # Projectile-alien collisions
    for projectile in reversed(projectiles):
        projectile_rect = pg.Rect(projectile['x'], projectile['y'], projectile_w, projectile_h)
        for alien in aliens:
            if alien.rect.colliderect(projectile_rect):
                projectiles.remove(projectile)
                aliens.remove(alien)
                score += 10
                break

    if not aliens:
        wave += 1
        total_aliens = 5 * (2**wave)
        for i in range(total_aliens):
            x = 40*(i % 10) + 15
            y = 40*(i // 10)
            aliens.append(Alien(x, y, alien_images[0],speed=basespeed + wave*0.5))

    # Drawing
    screen.fill((0, 0, 0))

    r_ship = (tick // 4) % 3
    screen.blit(ship_images[r_ship], (ship_x, ship_y))

    r_alien = (tick // 8) % 2
    for alien in aliens:
        alien.image = alien_images[r_alien]
        alien.draw(screen)

    for projectile in projectiles:
        pg.draw.rect(screen, (255, 0, 0), (projectile['x'], projectile['y'], projectile_w, projectile_h))

    text = font_scoreboard.render(f"{score:04d}", True, (255, 255, 255))
    screen.blit(text, (10, 560))

    pg.display.flip()
    clock.tick(50)
    tick += 1

def gameend():
    if not closedwindows:
        screen.fill((0, 0, 0))
        game_over_text = font_scoreboard.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
        screen.blit(game_over_text, text_rect)
        pg.display.flip()
        pg.time.wait(500)
        pg.quit()
        clip = VideoFileClip('images/gameover.mp4')
        clip.preview()
        exit()

gameend()
