# Arcade-style space shooter inspired by Galaga and Spacer Invaders.
# Made for the purpose of teaching git version control to beginners.

import pygame as pg


### Setup ###
pg.init()
clock = pg.time.Clock()

screen = pg.display.set_mode((400,600))
pg.display.set_caption("Space Shooter")

# Spaceship character
ship_images = []
for i in range(3):
    img = pg.image.load(f"images/ship_{i}.png")
    ship_images.append(img)
ship_x = 200 
ship_y = 500

# Alien character
alien_images = []
for i in range(2):
    img = pg.image.load(f"images/alien_{i}.png")
    alien_images.append(img)
alien_x = 200 
alien_y = 0 

# Keypress status
left_pressed = False
right_pressed = False


### Game loop ###
running = True
tick = 0
while running:

    ## Event loop  (handle keypresses etc.) ##
    events = pg.event.get()
    for event in events:

        # Close window (pressing [x], Alt+F4 etc.)
        if event.type == pg.QUIT:
            running = False
        
        # Keypresses
        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                running = False

            elif event.key == pg.K_LEFT:
                left_pressed = True

            elif event.key == pg.K_RIGHT:
                right_pressed = True

        # Keyreleases
        elif event.type == pg.KEYUP:

            if event.key == pg.K_LEFT:
                left_pressed = False 

            elif event.key == pg.K_RIGHT:
                right_pressed = False 
    

    ## Updating (movement, collisions, etc.) ##
    
    # Alien
    alien_y += 1    

    # Spaceship
    if left_pressed:
        ship_x -= 4 

    if right_pressed:
        ship_x += 4 


    ## Drawing ##
    screen.fill((0,0,0)) 

    # 3 images --> tick % 3
    # 100% animation speed: tick % 3
    # 25% animation speed: int(tick/4) % 3
    r = int(tick/4) % 3 
    screen.blit(ship_images[r], (ship_x, ship_y))

    # Alien
    r = int(tick/8) % 2
    screen.blit(alien_images[r], (alien_x, alien_y))

    # Update window with newly drawn pixels
    pg.display.flip()

    # Limit/fix frame rate (fps)
    clock.tick(50)
    tick += 1