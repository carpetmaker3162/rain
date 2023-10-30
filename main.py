import math
import random
import pygame
from raindrop import Raindrop

pygame.init()
pygame.font.init()
ARIAL = pygame.font.SysFont("arial", 60)
clock = pygame.time.Clock()

# ---------- parameters ----------
# ratio: 1px = 1cm
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
speed = 10
guy_height = 170 # 170px = 170cm (avg male height)
guy_width = 40 # 40px = 40cm (avg male shoulder width)
raindrops_per_frame = 9
raindrop_init_speed = 15 # 15px/s * 60 = 900px/s = 9m/s (avg raindrop terminal velocity)
raindrop_accel = 0.1
wind = -2
# --------------------------------

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SCALED, vsync=1)
guy = pygame.Rect(0, 600 - guy_height, guy_width, guy_height)
bg_color = (255, 255, 255)
guy_color = (255, 0, 0)
rain_color = (0, 0, 0)
running = True
count = 0
start_moving = False

a = 0.5 * raindrop_accel
b = raindrop_init_speed
c = -SCREEN_HEIGHT
discriminant = b**2 - 4*a*c
wind_offset = round(wind * ((-b + math.sqrt(discriminant)) / (2*a)))

def update():
    if guy.x < 850 and start_moving:
        guy.move_ip(speed, 0)

rain = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(bg_color)
    update()
    
    # add new raindrops
    for i in range(raindrops_per_frame):
        rain.append(Raindrop(
            x=random.randint(-wind_offset, SCREEN_WIDTH - 100 - wind_offset),
            y=random.randint(0, 50)-50,
            wind=wind,
            speed=raindrop_init_speed,
            acceleration=raindrop_accel,
            color=rain_color))
    
    # update raindrops
    for raindrop in rain:
        raindrop.update()

        # start when first raindrop hits the ground
        if raindrop.on_ground:
            start_moving = True
        
        trailing_hitbox = pygame.Rect(guy.left - speed, guy.top, guy.width + speed, guy.height)
        if raindrop.colliderect(guy) or (start_moving and raindrop.colliderect(trailing_hitbox)):
            raindrop.killed = True
            count += 1

        raindrop.draw(screen)

        if raindrop.killed:
            rain.remove(raindrop)
    
    count_text = ARIAL.render(str(count), False, guy_color, None)
    screen.blit(count_text, (10, 10))

    pygame.draw.rect(screen, guy_color, guy)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
