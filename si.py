import pygame
# TODO add ship collision with borders
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 8
        self.last_shoot_time = 0

    def draw(self):
        pygame.draw.line(win, (255, 255, 255), (self.x - 15, self.y), (self.x + 15, self.y), 15)
        pygame.draw.polygon(win, (255, 255, 255), [[self.x - 4, self.y - 8], [self.x, self.y - 13], [self.x + 4, self.y - 8]], 5)

    def move_left(self):
        self.x -= self.velocity

    def move_right(self):
        self.x += self.velocity

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shoot_time > 1000:
            bullets.append(Bullet(self.x, self.y - 13))
            self.last_shoot_time = pygame.time.get_ticks()

class Bullet(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 10

    def draw(self):
        pygame.draw.line(win, (255, 255, 255), (self.x, self.y), (self.x, self.y - 5), 2)
        self.y -= self.velocity

        

pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()
player = Player(250, 470)
bullets = []

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - 4 <= 0:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_SPACE]:
        player.shoot()

    win.fill((0, 0, 0))
    player.draw()
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()


pygame.quit()
