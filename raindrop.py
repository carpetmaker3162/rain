import pygame

GROUND = 600

class Raindrop(pygame.Rect):
    def __init__(self, x, y, wind, speed, acceleration):
        super().__init__(x, y, 5, 5)
        
        self.color = pygame.Color(0, 0, 0)
        self.x_speed = wind
        self.y_speed = speed
        self.killed = False
        self.on_ground = False
        self.acceleration = acceleration
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self)
    
    def update(self):
        if self.y > GROUND:
            self.killed = True
            self.on_ground = True

        self.y_speed += self.acceleration
        self.move_ip(self.x_speed, self.y_speed)