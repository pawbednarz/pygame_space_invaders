import pygame

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

class Score_handler(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        pygame.font.init() 
        self.myfont = pygame.font.Font('Pixeled.ttf', 15)

    def draw_score(self):
        score_text = self.myfont.render('SCORE ' + str(self.score), False, (255, 255, 255))
        win.blit(score_text,(self.x, self.y))
        


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
        if self.x  - 20 - self.velocity >= 0:
            self.x -= self.velocity

    def move_right(self):
        if self.x + 20 + self.velocity <= WINDOW_WIDTH:
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
        self.HEIGHT = 5
        self.WIDTH = 2

    def draw(self):
        pygame.draw.line(win, (255, 255, 255), (self.x, self.y), (self.x, self.y - self.HEIGHT), self.WIDTH)
        self.y -= self.velocity

class Enemy(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = self.x + 10

    def draw(self):
        pygame.draw.line(win, (255, 255, 255), (self.x, self.y), (self.x + 30, self.y), 20)

    def hit(self):
        print('hit')
        

pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()
score_handler = Score_handler(10, 10)
player = Player(250, 470)
bullets = []
enemies = []
for i in range(1, 10):
    enemies.append(Enemy(30 + i * 40, 100))
print(pygame.font.get_fonts())

# score TODO find better way to display it?
score = 0

def redraw_game_window():
    win.fill((0, 0, 0))
    score_handler.draw_score()
    player.draw()
    for enemy in enemies:
        enemy.draw()
    for bullet in bullets:
        bullet.draw()
    pygame.display.update()

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        for enemy in enemies:
            if bullet.y - bullet.HEIGHT <= enemy.y and bullet.x >= enemy.x and bullet.x <= enemy.x + 30:
                enemy.hit()
                enemies.pop(enemies.index(enemy))
                bullets.pop(bullets.index(bullet))
                score_handler.score += 1
        if bullet.y - bullet.HEIGHT <= 0:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_SPACE]:
        player.shoot()

    redraw_game_window()

pygame.quit()
